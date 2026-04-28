from services.llm_service import LLMService
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        
    def handle(self, query: str, history: list = None) -> str:
        """
        Handles general conversational queries.
        """
        system_prompt = """You are a helpful and intelligent AI assistant.
Provide clear, accurate, and concise answers.

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
- Use clean headings (plain text), bullet points where helpful, and short paragraphs.
- Be natural and helpful, not robotic.
- Avoid over-explaining simple things.
- Structure suggestions clearly."""
        try:
            logger.info("LLMAgent generating response.")
            return self.llm.generate_response(query, system_prompt=system_prompt, history=history)
        except Exception as e:
            logger.error(f"LLMAgent error: {str(e)}")
            return "I encountered an error trying to process your request."
