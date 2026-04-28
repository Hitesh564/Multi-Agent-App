import json
from pathlib import Path
import numpy as np
from typing import List, Tuple
import faiss

from config import settings
from services.embedding_service import EmbeddingService
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryService:
    def __init__(self, embedding_service: EmbeddingService, dimension: int = 384, llm_service=None):
        self.embedding = embedding_service
        self.llm_service = llm_service
        self.dimension = dimension
        self.max_items = settings.MAX_MEMORY_ITEMS
        self.max_item_chars = settings.MAX_MEMORY_ITEM_CHARS
        self.score_threshold = settings.MEMORY_SCORE_THRESHOLD
        self.storage_dir = Path(settings.MEMORY_DIR)
        self.items_path = self.storage_dir / "items.json"
        self.vectors_path = self.storage_dir / "vectors.npy"
        self.memory_items: List[str] = []
        self.memory_vectors: List[np.ndarray] = []
        self.index = faiss.IndexFlatIP(self.dimension)
        self._load()

    def _rebuild_index(self) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        if self.memory_vectors:
            vectors = np.asarray(self.memory_vectors, dtype=np.float32)
            self.index.add(vectors)

    def _persist(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.items_path.write_text(
            json.dumps(self.memory_items, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if self.memory_vectors:
            np.save(self.vectors_path, np.asarray(self.memory_vectors, dtype=np.float32))
        elif self.vectors_path.exists():
            self.vectors_path.unlink()

    def _load(self) -> None:
        try:
            if self.items_path.exists():
                self.memory_items = json.loads(self.items_path.read_text(encoding="utf-8"))
            if self.vectors_path.exists():
                loaded_vectors = np.load(self.vectors_path)
                self.memory_vectors = [row.astype(np.float32) for row in loaded_vectors]
            if len(self.memory_vectors) != len(self.memory_items):
                logger.warning("Memory store metadata and vectors were out of sync; resetting memory store.")
                self.memory_items = []
                self.memory_vectors = []
            self._rebuild_index()
        except Exception as e:
            logger.error(f"Failed to load persisted memory: {str(e)}")
            self.memory_items = []
            self.memory_vectors = []
            self._rebuild_index()

    def extract_and_save_memory(self, user_prompt: str, assistant_response: str) -> None:
        """Uses the LLM to extract durable facts, preferences, or tasks from the conversation turn."""
        if not self.llm_service:
            return
            
        turn_text = f"User: {user_prompt}\nAssistant: {assistant_response}"
        prompt = f"""Extract any durable memories from this conversation turn.
Only extract: user facts, preferences, or explicit tasks.
Ignore casual chatter, simple answers, or vague statements.

Conversation turn:
{turn_text}

Output ONLY a JSON array of strings representing the extracted short and concise memories. If none, output []."""

        try:
            response_text = self.llm_service.generate_response(prompt, system_prompt="You are a JSON-only API. Respond with valid JSON.")
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            extracted_memories = json.loads(cleaned)
            
            if isinstance(extracted_memories, list):
                for mem in extracted_memories:
                    if isinstance(mem, str):
                        self.remember(mem.strip())
        except Exception as e:
            logger.error(f"Memory extraction failed: {str(e)}")

    def remember(self, text: str) -> None:
        if not text or not text.strip():
            return

        cleaned_text = text.strip()[: self.max_item_chars]
        
        # Deduplication (exact match)
        if cleaned_text in self.memory_items:
            return

        try:
            embedding = self.embedding.embed_text([cleaned_text])[0]
            
            # Semantic Deduplication against recent/top matches
            if self.memory_items:
                query_embedding = embedding.reshape(1, -1).astype(np.float32)
                scores, indices = self.index.search(query_embedding, 1)
                if indices[0][0] != -1 and float(scores[0][0]) > 0.95:  # Very high similarity
                    logger.info("Skipped remembering semantically identical item.")
                    return

            self.memory_items.append(cleaned_text)
            self.memory_vectors.append(embedding.astype(np.float32))

            if len(self.memory_items) > self.max_items:
                self.memory_items = self.memory_items[-self.max_items :]
                self.memory_vectors = self.memory_vectors[-self.max_items :]
                self._rebuild_index()
            else:
                self.index.add(embedding.reshape(1, -1).astype(np.float32))

            self._persist()
            logger.info(f"Saved a new memory item: {cleaned_text}")
        except Exception as e:
            logger.error(f"Failed to save memory item: {str(e)}")

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        if not query or not self.memory_items or self.index.ntotal == 0:
            return []

        try:
            query_embedding = self.embedding.embed_text([query]).astype(np.float32)
            k = min(top_k, len(self.memory_items))
            scores, indices = self.index.search(query_embedding, k)

            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx == -1 or idx >= len(self.memory_items):
                    continue
                if float(score) < self.score_threshold:
                    continue
                results.append((self.memory_items[idx], float(score)))
            return results
        except Exception as e:
            logger.error(f"Memory retrieval failed: {str(e)}")
            return []

    def clear(self) -> None:
        self.memory_items = []
        self.memory_vectors = []
        self._rebuild_index()
        self._persist()
        logger.info("Cleared all memory items.")
