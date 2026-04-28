import re
from services.llm_service import LLMService
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from utils.logger import get_logger

logger = get_logger(__name__)

class RAGAgent:
    def __init__(self, llm_service: LLMService, embedding_service: EmbeddingService, vector_store: VectorStore):
        self.llm = llm_service
        self.embedding = embedding_service
        self.vector_store = vector_store
        
    def handle(self, query: str, memory_context: str = "", history: list = None) -> str:
        try:
            if not self.vector_store.has_documents():
                return "❌ No document found. Please upload a PDF first."

            # === 1. QUERY NORMALIZATION ===
            query_lower = query.lower()
            if "bellman" in query_lower and "ford" not in query_lower:
                query_lower += " bellman ford algorithm"

            # keywords
            raw_keywords = set(query_lower.split())
            stop_words = {"the", "a", "an", "is", "are", "what", "how", "explain", "describe"}
            keywords = {kw.strip("?!.,;:\"'") for kw in raw_keywords if kw not in stop_words and len(kw) > 2}

            query_embedding = self.embedding.embed_text([query_lower])[0]

            results = self.vector_store.search(query_embedding, top_k=10, threshold=0.1)

            if not results:
                return "❌ Answer not found in document"

            # === 2. FILTER + HYBRID SCORING ===
            filtered = []
            for r in results:
                text = r["chunk"]
                text_lower = text.lower()

                # REMOVE NOISE 🔥
                if "(" in text and ";" in text:
                    continue
                if "document snippet" in text_lower:
                    continue
                if len(text.strip()) < 50:
                    continue

                match_count = sum(1 for kw in keywords if kw in text_lower)

                if match_count > 0:
                    score = r["score"] + (match_count * 0.2)
                    r["hybrid_score"] = score
                    filtered.append(r)

            if not filtered:
                filtered = results[:2]
            else:
                filtered.sort(key=lambda x: x["hybrid_score"], reverse=True)

            # === 3. CLEAN CONTEXT ===
            final_chunks = []
            seen = set()

            for r in filtered:
                text = r["chunk"]

                # trim
                text = text.strip()
                text = text[:350]

                if text in seen:
                    continue
                seen.add(text)

                page_match = re.search(r'Page\s+(\d+)', r['chunk'], re.IGNORECASE)
                page = page_match.group(1) if page_match else "Unknown"

                final_chunks.append({
                    "text": text,
                    "source": r["source_name"],
                    "page": page
                })

                if len(final_chunks) >= 3:
                    break

            if not final_chunks:
                return "❌ Answer not found in document"

            # === 4. STRICT PROMPT (VERY IMPORTANT) ===
            system_prompt = """
    You are a helpful document-based assistant.

    Your job is to answer the user's question clearly using ONLY the provided context.

    GLOBAL RULES:
    1. Do NOT repeat the user's question.
    2. Avoid robotic phrases like "Let's analyze" or "Based on the context".
    3. Keep responses focused only on what the user asked.
    4. Maintain a natural, conversational tone.
    5. Start directly with the answer, adding a short explanation if needed (1-3 lines).
    6. Keep total response length balanced (typically 3-8 lines).

    FORMATTING RULES:
    - Do NOT use bold markdown or asterisks (*).
    - Do NOT use emojis.
    - Use clean headings (plain text) and short paragraphs.

    RAG STRICT RULES:
    - Answer strictly using retrieved content.
    - Provide a direct answer followed by a short explanation.
    - DO NOT mention documents.
    - DO NOT mention pages.
    - DO NOT mention sources.
    - If the answer is not found in the context, return exactly: "Answer not found in document"
    """

            # CLEAN CONTEXT FORMAT 🔥 (NO [Chunk 1])
            context = "\n\n".join([c["text"] for c in final_chunks])

            prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

            response = self.llm.generate_response(prompt, system_prompt=system_prompt)

            if not response or len(response.strip()) < 20:
                return "❌ Answer not found in document"

            return response

        except Exception as e:
            logger.error(f"RAGAgent error: {str(e)}")
            return "❌ Answer not found in document"
