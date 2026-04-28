from services.tools.tool_registry import ToolRegistry
from utils.logger import get_logger

logger = get_logger(__name__)

class ToolAgent:
    def __init__(self, registry: ToolRegistry, llm_service=None):
        self.registry = registry
        self.llm = llm_service
        
    def handle(self, query: str, history: list = None) -> str:
        """
        Dispatches the query to the correct tool with improved context + robustness
        """

        resolved_query = query

        if history and self.llm:
            logger.info("ToolAgent resolving context for query.")
            prompt = f"""
    Rewrite this query to be fully self-contained using conversation history.
    Resolve references like 'there', 'tomorrow', etc.

    Query: "{query}"

    Return ONLY the rewritten query.
    """
            try:
                res = self.llm.generate_response(
                    prompt,
                    system_prompt="You are a query resolver. Output only the final query.",
                    history=history[-4:]
                )
                if res and not res.startswith("Error"):
                    candidate = res.strip().replace('"', '')
                    if "query:" in candidate.lower() or "return only" in candidate.lower() or len(candidate) > 220:
                        logger.warning("Resolved query appears invalid, falling back to original query.")
                        candidate = query
                    resolved_query = candidate
                    logger.info(f"Resolved tool query: {resolved_query}")
            except Exception as e:
                logger.error(f"Context resolution failed: {e}")

        # 🔹 Step 2: Identify tool
        logger.info("ToolAgent analyzing query for tool dispatch.")
        tool_name = self.registry.get_tool_for_query(resolved_query) or self.registry.get_tool_for_query(query)

        if not tool_name:
            logger.warning("No suitable tool found.")
            return "I couldn't identify the right tool. Try asking for weather or news."

        # 🔹 Step 3: Execute tool safely
        try:
            logger.info(f"Dispatching to tool: {tool_name}")
            result = self.registry.execute_tool(tool_name, resolved_query)

            # 🔥 Step 4: Fallback handling
            if not result or "unable" in result.lower() or "error" in result.lower():
                logger.warning("Tool failed, triggering fallback.")

                if tool_name == "news":
                    return "Live news unavailable. I cannot provide news without a working news API at this time."

                if self.llm:
                    fallback_prompt = f"""
    The tool failed to fetch real-time data for this query:
    "{resolved_query}"

    Provide a helpful approximate or general answer.
    """
                    fallback = self.llm.generate_response(fallback_prompt)
                    return f"Live data unavailable.\n\n{fallback}"

            return result

        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return "Tool service is currently unavailable."
