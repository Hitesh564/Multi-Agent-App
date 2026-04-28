import PyPDF2
import io
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_text_from_pdf(pdf_file_bytes: bytes) -> str:
    """
    Extracts text from a given PDF file bytes object.
    
    Args:
        pdf_file_bytes (bytes): The raw bytes of the PDF file.
        
    Returns:
        str: Extracted text from all pages.
    """
    try:
        pdf_file_obj = io.BytesIO(pdf_file_bytes)
        reader = PyPDF2.PdfReader(pdf_file_obj)
        text = ""
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {i + 1} ---\n{page_text}"
                
        # Remove null characters which can cause issues with embeddings
        text = text.replace('\\x00', '')
        
        logger.info(f"Successfully extracted {len(text)} characters from PDF ({len(reader.pages)} pages).")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise e
