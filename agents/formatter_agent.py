class FormatterAgent:
    @staticmethod
    def format(response: str, agent_type: str) -> str:
        """
        Formats the final response before displaying to the User.
        """
        # Remove common markdown clutter and asterisks
        cleaned = response.replace("**", "").replace("*", "")
        
        return cleaned.strip()
