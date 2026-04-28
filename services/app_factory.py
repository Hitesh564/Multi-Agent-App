from agents.llm_agent import LLMAgent
from agents.rag_agent import RAGAgent
from agents.router_agent import RouterAgent
from agents.tool_agent import ToolAgent
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.memory_service import MemoryService
from services.routing_service import RoutingService
from services.tools.tool_registry import registry as tool_registry
from services.tools.weather_tool import weather_tool
from services.tools.news_tool import news_tool
from services.vector_store import VectorStore


def build_system():
    if "weather" not in tool_registry.tools:
        tool_registry.register(
            name="weather",
            description="Get current weather",
            keywords=["weather", "temperature", "forecast", "rain", "sunny", "humid"],
            handler=weather_tool,
        )

    if "news" not in tool_registry.tools:
        tool_registry.register(
            name="news",
            description="Get latest news on topics",
            keywords=["news", "latest", "update", "headlines"],
            handler=news_tool,
        )

    llm = LLMService()
    embedding = EmbeddingService()
    vector_store = VectorStore(embedding_dimension=384)
    memory_service = MemoryService(embedding, llm_service=llm)

    routing_service = RoutingService(llm)
    router = RouterAgent(routing_service, vector_store)
    llm_agent = LLMAgent(llm)
    rag_agent = RAGAgent(llm, embedding, vector_store)
    tool_agent = ToolAgent(tool_registry, llm_service=llm)

    return {
        "llm": llm,
        "embedding": embedding,
        "vector_store": vector_store,
        "memory_service": memory_service,
        "router": router,
        "llm_agent": llm_agent,
        "rag_agent": rag_agent,
        "tool_agent": tool_agent,
    }
