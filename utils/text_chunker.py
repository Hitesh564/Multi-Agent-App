from typing import List
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def split_text(text: str, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP) -> List[str]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    """
    Splits text into smaller overlapping chunks.
    
    Args:
        text (str): The document text to split.
        chunk_size (int): Max size of each chunk.
        chunk_overlap (int): Overlap size between chunks.
        
    Returns:
        List[str]: List of text chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\\n\\n", "\\n", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        logger.info(f"Successfully split text into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}")
        raise e
