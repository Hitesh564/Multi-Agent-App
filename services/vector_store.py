import json
from collections import Counter
from pathlib import Path

import faiss
import numpy as np
from typing import Dict, List

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class VectorStore:
    def __init__(self, embedding_dimension: int = 384):
        self.dimension = embedding_dimension
        self.storage_dir = Path(settings.DOCUMENTS_DIR)
        self.index_path = self.storage_dir / "index.faiss"
        self.meta_path = self.storage_dir / "metadata.json"
        self.embeddings_path = self.storage_dir / "embeddings.npy"
        self.index = faiss.IndexFlatIP(self.dimension)
        self.records: List[Dict[str, str]] = []
        self.embeddings: List[np.ndarray] = []
        self._load()
        logger.info(f"Initialized FAISS index with dimension {self.dimension}")

    @property
    def chunks(self) -> List[str]:
        return [record["chunk"] for record in self.records]

    def has_documents(self) -> bool:
        return bool(self.records)

    def document_count(self) -> int:
        return len({record["doc_id"] for record in self.records})

    def list_documents(self) -> List[Dict[str, str | int]]:
        counts = Counter(record["source_name"] for record in self.records)
        doc_ids = {}
        for record in self.records:
            doc_ids[record["source_name"]] = record["doc_id"]
        return [
            {"doc_id": doc_ids[source_name], "source_name": source_name, "chunks": count}
            for source_name, count in counts.items()
        ]

    def _rebuild_index(self) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        if self.embeddings:
            matrix = np.asarray(self.embeddings, dtype=np.float32)
            self.index.add(matrix)

    def _persist(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.meta_path.write_text(
            json.dumps(self.records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if self.embeddings:
            np.save(self.embeddings_path, np.asarray(self.embeddings, dtype=np.float32))
            faiss.write_index(self.index, str(self.index_path))
        else:
            if self.embeddings_path.exists():
                self.embeddings_path.unlink()
            if self.index_path.exists():
                self.index_path.unlink()

    def _load(self) -> None:
        try:
            if self.meta_path.exists():
                self.records = json.loads(self.meta_path.read_text(encoding="utf-8"))
            if self.embeddings_path.exists():
                loaded_embeddings = np.load(self.embeddings_path)
                self.embeddings = [row.astype(np.float32) for row in loaded_embeddings]
            if self.records and self.index_path.exists() and len(self.records) == len(self.embeddings):
                self.index = faiss.read_index(str(self.index_path))
            elif self.records or self.embeddings:
                self._rebuild_index()
        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            self.records = []
            self.embeddings = []
            self._rebuild_index()

    def add_documents(self, doc_id: str, source_name: str, chunks: List[str], embeddings: np.ndarray) -> None:
        if doc_id in {record["doc_id"] for record in self.records}:
            self.remove_document(doc_id)

        embeddings = np.asarray(embeddings, dtype=np.float32)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        self.records.extend(
            {"doc_id": doc_id, "source_name": source_name, "chunk": chunk}
            for chunk in chunks
        )
        self.embeddings.extend(row for row in embeddings)
        self._rebuild_index()
        self._persist()
        logger.info(f"Added {len(chunks)} chunks from document '{source_name}' to Vector Store.")

    def remove_document(self, doc_id: str) -> None:
        kept_pairs = [
            (record, embedding)
            for record, embedding in zip(self.records, self.embeddings)
            if record["doc_id"] != doc_id
        ]
        self.records = [record for record, _ in kept_pairs]
        self.embeddings = [embedding for _, embedding in kept_pairs]
        self._rebuild_index()
        self._persist()

    def clear(self) -> None:
        self.records = []
        self.embeddings = []
        self._rebuild_index()
        self._persist()

    def search(self, query_embedding: np.ndarray, top_k: int = settings.TOP_K_RESULTS, threshold: float = None) -> List[Dict[str, str | float]]:
        if threshold is None:
            threshold = settings.SIMILARITY_THRESHOLD

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        query_embedding = np.asarray(query_embedding, dtype=np.float32)
        k = min(top_k, len(self.records))
        if k == 0:
            return []

        scores, indices = self.index.search(query_embedding, k)
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            record = self.records[idx]
            if float(score) < threshold:
                continue
            results.append(
                {
                    "chunk": record["chunk"],
                    "score": float(score),
                    "source_name": record["source_name"],
                    "doc_id": record["doc_id"],
                }
            )
        return results
