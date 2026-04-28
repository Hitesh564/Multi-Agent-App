import os
import hashlib
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import warnings
warnings.filterwarnings("ignore")
from transformers import logging
logging.set_verbosity_error()

from agents.formatter_agent import FormatterAgent
from config import settings
from services.app_factory import build_system
from utils.logger import get_logger
from utils.pdf_parser import extract_text_from_pdf
from utils.text_chunker import split_text

# Import the supabase memory functionality you added
from services.memory.supabase_memory import save_message, load_messages

logger = get_logger("api_server")

app = FastAPI(title="Adaptive Multi-Agent AI API")

# Setup CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since frontend is localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system instance
system = build_system()

# Models
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    role: str
    content: str
    route: str
    route_reason: str
    route_confidence: float

class MemoryItemRequest(BaseModel):
    text: str

@app.get("/api/status")
async def get_status():
    return {
        "memory_items": len(system["memory_service"].memory_items),
        "document_chunks": len(system["vector_store"].chunks),
        "indexed_docs": system["vector_store"].document_count(),
        "mode": "Multi-agent"
    }

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    history = load_messages(session_id)
    if not history:
        # Return initial message if empty
        welcome_msg = FormatterAgent.format(
            "Welcome to the Adaptive Multi-Agent assistant with persistent memory, document recall, and live tool access.",
            "GENERAL",
        )
        save_message(session_id, "assistant", welcome_msg)
        return [{"role": "assistant", "content": welcome_msg}]
    return history

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    prompt = req.message
    session_id = req.session_id
    
    # Load history
    history = load_messages(session_id)
    
    # Save user message
    save_message(session_id, "user", prompt)
    
    # Build memory context
    # DISABLED: recall = system["memory_service"].retrieve(prompt, top_k=3)
    recall = []
    memory_context = ""
    # DISABLED: if recall:
    #     context_lines = [f"- {text}" for text, _score in recall]
    #     memory_context = "Memory Context:\n" + "\n".join(context_lines) + "\n\n"
        
    last_route = "GENERAL"
    
    routing_context = {"previous_route": last_route}
    category, route_data = system["router"].classify(prompt, routing_context)
    
    # Extract last 4 messages for history context
    llm_history = [{"role": msg["role"], "content": msg["content"]} for msg in history[-4:]] if len(history) > 0 else []

    try:
        if category == "RAG":
            raw_response = system["rag_agent"].handle(prompt, memory_context, history=llm_history)
        elif category == "TOOL":
            raw_response = system["tool_agent"].handle(prompt, history=llm_history)
        else:
            combined_prompt = f"{memory_context}{prompt}" if memory_context else prompt
            raw_response = system["llm_agent"].handle(combined_prompt, history=llm_history)
            
        final_response = FormatterAgent.format(raw_response, category)
        
        # Save assistant message
        save_message(session_id, "assistant", final_response)
        
        # Auto-extract memory
        # DISABLED: system["memory_service"].extract_and_save_memory(prompt, raw_response)
        
        return ChatResponse(
            role="assistant",
            content=final_response,
            route=category,
            route_reason=route_data.get("reason", ""),
            route_confidence=route_data.get("confidence", 0.0)
        )
    except Exception as e:
        logger.error(f"Error handling chat: {e}")
        error_msg = f"Sorry, an error occurred processing your request: {str(e)}"
        save_message(session_id, "assistant", error_msg)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        max_size_bytes = settings.MAX_PDF_SIZE_MB * 1024 * 1024
        if len(pdf_bytes) > max_size_bytes:
            raise HTTPException(status_code=400, detail=f"File too large. Max allowed is {settings.MAX_PDF_SIZE_MB} MB.")
            
        doc_id = hashlib.sha1(pdf_bytes).hexdigest()
        text = extract_text_from_pdf(pdf_bytes)
        chunks = split_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text extracted from PDF.")
            
        embeddings = system["embedding"].embed_text(chunks)
        system["vector_store"].add_documents(
            doc_id=doc_id,
            source_name=file.filename,
            chunks=chunks,
            embeddings=embeddings,
        )
        return {"success": True, "message": f"Indexed {len(chunks)} chunks from '{file.filename}'"}
    except Exception as e:
        logger.error(f"Doc upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
async def get_documents():
    return {"documents": system["vector_store"].list_documents()}

@app.post("/api/documents/clear")
async def clear_documents():
    system["vector_store"].clear()
    return {"success": True, "message": "Indexed documents cleared."}

@app.get("/api/memory")
async def get_memory():
    # DISABLED: return {"items": system["memory_service"].memory_items}
    return {"items": []}

@app.post("/api/memory/add")
async def add_memory(req: MemoryItemRequest):
    # DISABLED global memory addition
    return {"success": True}

@app.post("/api/memory/clear")
async def clear_memory():
    # DISABLED global memory clearing
    return {"success": True, "message": "Memory cleared locally for current user."}
