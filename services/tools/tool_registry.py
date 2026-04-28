from typing import Dict, Any, Callable
from utils.logger import get_logger

logger = get_logger(__name__)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        
    def register(self, name: str, description: str, keywords: list[str], handler: Callable):
        """
        Registers a new tool in the registry.
        """
        self.tools[name] = {
            "description": description,
            "keywords": [kw.lower() for kw in keywords],
            "handler": handler
        }
        logger.info(f"Registered tool: {name}")

    def get_tool_for_query(self, query: str) -> str | None:
        """
        Identifies the tool to use based on keyword matching in the query.
        Returns the name of the tool, or None if no match.
        """
        query_lower = query.lower()
        for name, data in self.tools.items():
            for keyword in data["keywords"]:
                if keyword in query_lower:
                    return name
        return None

    def has_match(self, query: str) -> bool:
        return self.get_tool_for_query(query) is not None

    def execute_tool(self, tool_name: str, query: str) -> str:
        """
        Executes the registered handler for the tool.
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
            
        try:
            return self.tools[tool_name]["handler"](query)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return f"Error executing {tool_name}: {str(e)}"

# Global singleton registry instance
registry = ToolRegistry()
