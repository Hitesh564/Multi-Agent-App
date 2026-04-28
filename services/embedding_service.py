from typing import List
from config import settings
from utils.logger import get_logger
import numpy as np

logger = get_logger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = None
        self._dimension = 384

    def _load_model(self):
        if self.model is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            if hasattr(self.model, "get_embedding_dimension"):
                self._dimension = self.model.get_embedding_dimension()
            else:
                self._dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Loaded embedding model: {settings.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            self.model = None

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, texts: List[str]) -> np.ndarray:
        """
        Generates embeddings for a list of text strings.
        
        Args:
            texts: List of strings to embed.
        Returns:
            np.ndarray: Embedding matrix.
        """
        if self.model is None:
            self._load_model()

        if not self.model:
            raise RuntimeError("Embedding model is not loaded.")
            
        try:
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            return np.asarray(embeddings, dtype=np.float32)
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise e
