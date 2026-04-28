import streamlit as st
import uuid

if "session_id" not in st.session_state:
    st.session_state.session_id = st.query_params.get("session_id", None)

    if not st.session_state.session_id:
        new_id = str(uuid.uuid4())
        st.session_state.session_id = new_id
        st.query_params["session_id"] = new_id

from services.memory.supabase_memory import save_message, load_messages
import hashlib
import warnings
warnings.filterwarnings("ignore")
from transformers import logging
logging.set_verbosity_error()

from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)


from agents.formatter_agent import FormatterAgent
from config import settings
from services.app_factory import build_system
from utils.logger import get_logger
from utils.pdf_parser import extract_text_from_pdf
from utils.text_chunker import split_text

warnings.filterwarnings("ignore", message=r"Accessing `__path__` from .*zoedepth.*")
logger = get_logger("app")


def configure_page() -> None:
    st.set_page_config(
        page_title="Adaptive Multi-Agent AI",
        page_icon="🤖",
        layout="wide",
    )
    st.markdown(
        """
        <style>
            .stApp { background: linear-gradient(180deg, #0b1620 0%, #111b27 100%); color: #f5f7fa; }
            .stSidebar { background: #101820; }
            .block-container { padding: 1.8rem 2rem 2rem 2rem; }
            .chat-message { background: rgba(255,255,255,0.08); border-radius: 18px; padding: 18px; margin-bottom: 12px; }
            .assistant-bubble { border-left: 4px solid #4f86ff; }
            .user-bubble { border-left: 4px solid #f5c242; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_system():
    return build_system()


def ensure_session_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        # 🔥 Load from Supabase instead of reset
        history = load_messages(st.session_state.session_id)

        if history:
            st.session_state.messages = history
        else:
            reset_conversation()

    if "auto_save_memory" not in st.session_state:
        st.session_state.auto_save_memory = True
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ""
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""
    if "last_route" not in st.session_state:
        st.session_state.last_route = "GENERAL"
    if "route_reason" not in st.session_state:
        st.session_state.route_reason = ""
    if "route_confidence" not in st.session_state:
        st.session_state.route_confidence = 0.0


def reset_conversation() -> None:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": FormatterAgent.format(
                "Welcome to the Adaptive Multi-Agent assistant with persistent memory, document recall, and live tool access.",
                "GENERAL",
            ),
        }
    ]


def append_message(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})

    # 🔥 Save to Supabase
    save_message(st.session_state.session_id, role, content)


def build_memory_context(memory_service, query: str) -> str:
    recall = memory_service.retrieve(query, top_k=3)
    if not recall:
        return ""

    context_lines = [f"- {text}" for text, _score in recall]
    return "Memory Context:\n" + "\n".join(context_lines) + "\n\n"


def generate_answer(system: dict, prompt: str) -> tuple[str, str]:
    memory_context = build_memory_context(system["memory_service"], prompt)
    
    # Provide context for hybrid routing
    routing_context = {
        "previous_route": st.session_state.get("last_route")
    }
    category, route_data = system["router"].classify(prompt, routing_context)
    
    # Save route metadata to session state for debugging
    st.session_state.last_route = category
    st.session_state.route_reason = route_data.get("reason", "")
    st.session_state.route_confidence = route_data.get("confidence", 0.0)

    # Prepare chat history context (excluding the current prompt and the initial system welcome)
    history = []
    if len(st.session_state.messages) > 2:
        # Get the last 4 turns before the current prompt
        history = st.session_state.messages[-5:-1]

    if category == "RAG":
        raw_response = system["rag_agent"].handle(prompt, memory_context, history=history)
    elif category == "TOOL":
        raw_response = system["tool_agent"].handle(prompt, history=history)
    else:
        combined_prompt = f"{memory_context}{prompt}" if memory_context else prompt
        raw_response = system["llm_agent"].handle(combined_prompt, history=history)

    return category, raw_response


def process_uploaded_pdf(system: dict, uploaded_file) -> None:
    max_size_bytes = settings.MAX_PDF_SIZE_MB * 1024 * 1024
    if uploaded_file.size and uploaded_file.size > max_size_bytes:
        st.error(f"File is too large. Maximum allowed size is {settings.MAX_PDF_SIZE_MB} MB.")
        return

    with st.spinner("Indexing your PDF..."):
        try:
            pdf_bytes = uploaded_file.read()
            doc_id = hashlib.sha1(pdf_bytes).hexdigest()
            text = extract_text_from_pdf(pdf_bytes)
            chunks = split_text(text)
            if not chunks:
                st.error("No text was extracted from that PDF.")
                return

            embeddings = system["embedding"].embed_text(chunks)
            system["vector_store"].add_documents(
                doc_id=doc_id,
                source_name=uploaded_file.name,
                chunks=chunks,
                embeddings=embeddings,
            )
            st.success(f"Indexed {len(chunks)} chunks from '{uploaded_file.name}'.")
        except Exception as e:
            st.error(f"Document processing failed: {str(e)}")
            logger.error(f"PDF processing error: {str(e)}")


def render_sidebar(system: dict) -> None:
    memory_service = system["memory_service"]
    vector_store = system["vector_store"]

    with st.sidebar:
        st.markdown("# 🚀 Workspace Dashboard")
        st.markdown("Manage persistent memory, indexed documents, and conversation state.")

        if st.button("Clear Conversation"):
            reset_conversation()
            st.rerun()

        if st.button("Clear Memory"):
            memory_service.clear()
            st.success("Persistent memory cleared.")

        if st.button("Clear Documents"):
            vector_store.clear()
            st.success("Indexed documents cleared.")

        st.checkbox("Auto save every exchange to memory", key="auto_save_memory")
        st.divider()

        st.subheader("Memory Notes")
        custom_memory = st.text_area("Capture a note for future context", value="", height=120)
        if st.button("Save Memory Note"):
            if custom_memory.strip():
                memory_service.remember(custom_memory)
                st.success("Saved note to memory.")
            else:
                st.warning("Enter a note before saving.")

        st.divider()
        st.subheader("Status Overview")
        st.metric("Memory Items", len(memory_service.memory_items))
        st.metric("Document Chunks", len(vector_store.chunks))
        st.metric("Indexed Docs", vector_store.document_count())
        st.metric("Chat Messages", len(st.session_state.messages))


def render_chat_tab(system: dict) -> None:
    left, right = st.columns([3, 1])

    with left:
        for msg in st.session_state.messages:
            role = msg.get("role")
            content = msg.get("content")

            bubble_type = "assistant-bubble" if role == "assistant" else "user-bubble"
            st.markdown(
                f"<div class='chat-message {bubble_type}'><strong>{role.title()}:</strong><br>{content}</div>",
                unsafe_allow_html=True,
            )

        prompt = st.chat_input("Ask a question, upload a document, or use a live tool query.")
        if prompt:
            append_message("user", prompt)
            st.session_state.last_prompt = prompt

            with st.spinner("Working through your request..."):
                category, raw_response = generate_answer(system, prompt)
                final_response = FormatterAgent.format(raw_response, category)
                append_message("assistant", final_response)
                st.session_state.last_response = final_response

                if st.session_state.auto_save_memory:
                    system["memory_service"].extract_and_save_memory(prompt, raw_response)

            st.rerun()

    with right:
        st.markdown("### Quick Actions")
        if st.button("Regenerate Last Answer"):
            if st.session_state.last_prompt:
                with st.spinner("Regenerating response..."):
                    category, raw_response = generate_answer(system, st.session_state.last_prompt)
                    final_response = FormatterAgent.format(raw_response, category)
                    append_message("assistant", final_response)
                    st.session_state.last_response = final_response
                st.rerun()
            else:
                st.warning("Ask a question first before regenerating.")

        if st.button("Recall Memory for Latest Query"):
            if st.session_state.last_prompt:
                recall = system["memory_service"].retrieve(st.session_state.last_prompt)
                if recall:
                    for item, score in recall:
                        st.markdown(f"- {item} _(score: {score:.3f})_")
                else:
                    st.info("No strong memory matches found.")
            else:
                st.warning("No previous query to recall from.")


def render_memory_tab(system: dict) -> None:
    memory_service = system["memory_service"]
    st.header("Memory Board")
    st.markdown("Persistent memory is capped and survives app restarts.")

    if memory_service.memory_items:
        for idx, item in enumerate(memory_service.memory_items, start=1):
            with st.expander(f"Memory {idx}"):
                st.write(item)
    else:
        st.info("Your memory board is empty.")

    if st.session_state.last_prompt:
        st.divider()
        st.subheader("Recall Preview")
        recall = memory_service.retrieve(st.session_state.last_prompt)
        if recall:
            for text, score in recall:
                st.markdown(f"**Memory match** _(score: {score:.3f})_\n\n{text}")
        else:
            st.info("No memory match for your most recent prompt.")


def render_documents_tab(system: dict) -> None:
    vector_store = system["vector_store"]
    st.header("PDF Document Intelligence")
    st.markdown("Upload PDFs to build a persistent document index for grounded answers.")
    uploaded_file = st.file_uploader("Upload one PDF file", type=["pdf"])
    if uploaded_file is not None and st.button("Process PDF Document"):
        process_uploaded_pdf(system, uploaded_file)

    documents = vector_store.list_documents()
    if documents:
        st.markdown("### Indexed documents")
        for document in documents:
            st.markdown(f"- **{document['source_name']}**: {document['chunks']} chunks")
    else:
        st.info("No PDF document is currently indexed.")


def render_settings_tab(system: dict) -> None:
    vector_store = system["vector_store"]
    memory_service = system["memory_service"]
    st.header("Settings & Control")
    st.write(
        {
            "Auto Save Memory": st.session_state.auto_save_memory,
            "Indexed Documents": vector_store.document_count(),
            "Indexed Chunks": len(vector_store.chunks),
            "Memory Items": len(memory_service.memory_items),
            "Memory Cap": settings.MAX_MEMORY_ITEMS,
            "Embedding Model": settings.EMBEDDING_MODEL,
        }
    )
    st.caption("Heavy models now load lazily on first use, which reduces startup time.")


def render_debug_tab(system: dict) -> None:
    st.header("Observability & Debugging")
    st.markdown("Inspect the hybrid routing decisions and active context.")
        
    left, right = st.columns(2)
    with left:
        st.subheader("Last Route Decision")
        st.write(f"**Selected Route**: `{st.session_state.get('last_route', 'N/A')}`")
        st.write(f"**Confidence**: `{st.session_state.get('route_confidence', 0.0):.2f}`")
        st.write(f"**Reason**: {st.session_state.get('route_reason', 'N/A')}")
        
    with right:
        st.subheader("Short-term Context")
        history = st.session_state.get("messages", [])
        if len(history) > 2:
            st.write(f"Passing last {min(4, len(history)-2)} messages to LLM.")
        else:
            st.write("No short-term history yet.")

    st.divider()
    st.subheader("Recalled Memory Context (For last prompt)")
    if st.session_state.last_prompt:
        recall = system["memory_service"].retrieve(st.session_state.last_prompt)
        if recall:
            for text, score in recall:
                st.markdown(f"- _(score: {score:.3f})_ {text}")
        else:
            st.info("No matching memories retrieved.")
    else:
        st.info("No prompt entered yet.")


def main() -> None:
    configure_page()
    system = get_system()
    ensure_session_state()
    render_sidebar(system)

    main_header, main_actions = st.columns([4, 1])
    with main_header:
        st.title("Adaptive Multi-Agent AI Portal")
        st.markdown(
            "### Faster startup, persistent memory, safer configuration, and better document handling."
        )
    with main_actions:
        st.markdown("### Live Status")
        st.metric("Memory", f"{len(system['memory_service'].memory_items)} items")
        st.metric("Docs", f"{system['vector_store'].document_count()} docs")
        st.metric("Mode", "Multi-agent")

    tabs = st.tabs(["💬 Chat", "🧠 Memory Board", "📚 Documents", "⚙️ Settings", "🐛 Debug"])
    with tabs[0]:
        render_chat_tab(system)
    with tabs[1]:
        render_memory_tab(system)
    with tabs[2]:
        render_documents_tab(system)
    with tabs[3]:
        render_settings_tab(system)
    with tabs[4]:
        render_debug_tab(system)

if __name__ == "__main__":
    main()
