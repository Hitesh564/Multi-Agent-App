from services.routing_service import RoutingService
from utils.logger import get_logger

logger = get_logger(__name__)

class RouterAgent:
    def __init__(self, routing_service: RoutingService, vector_store):
        self.routing_service = routing_service
        self.vector_store = vector_store

    def classify(self, query: str, context: dict = None) -> tuple[str, dict]:
        """
        Returns the category and the routing metadata.
        """
        if context is None:
            context = {}
            
        # Enrich context with vector store info
        context["documents_indexed"] = self.vector_store.document_count() > 0

        try:
            logger.info(f"Classifying query: '{query}'")
            route_data = self.routing_service.evaluate_route(query, context)
            logger.info(f"Route selected: {route_data['selected_route']} (Confidence: {route_data['confidence']})")
            return route_data["selected_route"], route_data
        except Exception as e:
            logger.error(f"Routing failed: {str(e)}")
            return "GENERAL", {"selected_route": "GENERAL", "confidence": 0.0, "reason": "Error fallback"}
