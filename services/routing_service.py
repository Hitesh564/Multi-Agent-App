import json
from services.llm_service import LLMService

class RoutingService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.tool_keywords = ["weather", "forecast", "stock", "price", "live", "latest", "news", "update", "headlines"]
        self.rag_keywords = ["pdf", "document", "uploaded file", "page", "pages", "section", "chapter", "summarize document"]
        self.follow_up_keywords = ["what about", "explain more", "why", "how come", "tell me more", "elaborate", "details"]

    def evaluate_route(self, query: str, context: dict) -> dict:
        """
        Evaluates the best route using a hybrid scoring system.
        context: {
            "documents_indexed": bool,
            "previous_route": str ("TOOL", "RAG", "GENERAL", or None)
        }
        Returns: {
            "selected_route": str,
            "confidence": float,
            "reason": str,
            "llm_fallback_used": bool
        }
        """
        query_lower = query.lower()
        
        tool_score = 0
        rag_score = 0
        general_score = 0

        # Check explicit keywords
        if any(kw in query_lower for kw in self.tool_keywords):
            tool_score += 10
        
        if any(kw in query_lower for kw in self.rag_keywords):
            rag_score += 10

        # Check follow-ups
        is_follow_up = any(kw in query_lower for kw in self.follow_up_keywords)
        if is_follow_up:
            if context.get("previous_route") == "TOOL":
                tool_score += 5
            elif context.get("previous_route") == "RAG":
                rag_score += 5
            else:
                general_score += 5
                
        # Context bonuses
        if context.get("documents_indexed") and rag_score > 0:
            rag_score += 5 # Bonus if requesting rag and documents exist
            
        if tool_score == 0 and rag_score == 0 and not is_follow_up:
            general_score += 5

        scores = {"TOOL": tool_score, "RAG": rag_score, "GENERAL": general_score}
        max_route = max(scores, key=scores.get)
        max_score = scores[max_route]
        
        # Check if unambiguous
        scores_list = list(scores.values())
        scores_list.sort(reverse=True)
        
        if max_score >= 10 and (len(scores_list) < 2 or (max_score - scores_list[1]) >= 10):
            return {
                "selected_route": max_route,
                "confidence": max_score / 20.0,
                "reason": f"Rule-based clear winner (scores: {scores})",
                "llm_fallback_used": False
            }

        # LLM Fallback for ambiguous
        return self._llm_fallback_route(query, context, scores)

    def _llm_fallback_route(self, query: str, context: dict, scores: dict) -> dict:
        prompt = f"""You are a routing classification engine. 
Determine the best route for the user's query: 'TOOL', 'RAG', or 'GENERAL'.
Available Routes:
- TOOL: For real-time data like weather, stocks, or current prices.
- RAG: For questions requiring information from uploaded documents (PDFs) or summarizing large texts.
- GENERAL: For casual conversation, general knowledge, or when no documents/tools are needed.

Context: 
- Documents Indexed: {context.get('documents_indexed', False)}
- Previous Route: {context.get('previous_route', 'None')}

Query: "{query}"

Output ONLY a JSON object with this exact structure:
{{"selected_route": "ROUTE_NAME", "reason": "brief explanation"}}"""

        try:
            response_text = self.llm_service.generate_response(prompt, system_prompt="You are a JSON-only API. Respond with valid JSON.")
            # Basic cleanup if the LLM adds markdown formatting
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned)
            
            route = result.get("selected_route", "GENERAL").upper()
            if route not in ["TOOL", "RAG", "GENERAL"]:
                route = "GENERAL"
                
            return {
                "selected_route": route,
                "confidence": 0.8,
                "reason": f"LLM Routing: {result.get('reason', 'No reasoning provided')} (Initial ambiguity: {scores})",
                "llm_fallback_used": True
            }
        except Exception as e:
            # Absolute fallback
            sorted_routes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            return {
                "selected_route": sorted_routes[0][0],
                "confidence": 0.5,
                "reason": f"LLM fallback failed, relying on highest score. Error: {str(e)}",
                "llm_fallback_used": True
            }
