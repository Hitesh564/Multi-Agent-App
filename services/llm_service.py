from groq import Groq
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.client = None
        self.model = settings.LLM_MODEL

    def _get_client(self):
        if self.provider == "groq":
            if not settings.GROQ_API_KEY:
                logger.warning("GROQ_API_KEY not found in environment!")
                return None
            if self.client is None:
                self.client = Groq(api_key=settings.GROQ_API_KEY)
            return self.client

        logger.error(f"Provider {self.provider} not fully supported yet.")
        return None
    
    def generate_response(self, prompt: str, system_prompt: str = "You are a helpful AI assistant.", history: list = None) -> str:
        """
        Generates a standard chat completion.
        """
        client = self._get_client()
        if self.provider != "groq" or not client:
            return "Error: LLM provider not correctly configured or unsupported."
            
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        
        if history:
            messages.extend(history)
            
        messages.append({
            "role": "user",
            "content": prompt,
        })
            
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            return "I'm sorry, I'm currently unable to connect to my AI service. Please try again later."
