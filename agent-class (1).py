"""
Chess agent that provides strategic analysis and move recommendations.
"""

from typing import Dict, List, Any, Optional
from .task_network import ChessTaskNetwork

class ChessAgent:
    """Agent for chess assistance."""
    
    def __init__(self, engine_path: str):
        self.name = "Chess Assistant"
        self.task_network = ChessTaskNetwork(engine_path)
        
    def process_request(self, request: str, fen: str) -> Dict[str, Any]:
        """Process a request related to chess."""
        if not fen:
            return {
                "type": "error",
                "content": "No chess position provided. Please provide a FEN string."
            }
        
        # Process natural language request
        response = self.task_network.process_natural_language(fen, request)
        
        # Format the response nicely
        formatted_response = self._format_response(response)
        
        return {
            "raw": response,
            "formatted": formatted_response
        }
    
    def _format_response(self, response: Dict[str, Any]) -> str:
        """Format the response in a human-readable way."""
        response_type = response.get("type", "")
        
        if response_type == "move_recommendation":
            result = f"I recommend: {response['content']}"
            if "reasoning" in response:
                result += f"\n\nReasoning: {response['reasoning']}"
            if "strategy" in response:
                result += f"\n\nThis supports the strategy: {response['strategy']}"
            return result
            
        elif response_type == "strategy_advice":
            result = f"Strategic advice: {response['content']}"
            if response.get("additional_options"):
                result += "\n\nAlternative strategies to consider:\n"
                for i, option in enumerate(response["additional_options"][:2], 1):
                    result += f"{i}. {option}\n"
            return result
            
        elif response_type == "tactical_advice":
            return f"Tactical opportunity: {response['content']}"
            
        elif response_type == "position_evaluation":
            return (f"Position evaluation: {response['evaluation']}\n"
                    f"Position type: {response['position_type']}\n\n"
                    f"Suggested approach: {response['suggested_approach']}")
            
        elif response_type == "move_explanation":
            return (f"Analysis of {response['move']}:\n\n"
                    f"{response['explanation']}\n\n"
                    f"Evaluation change: {response['evaluation_before']} → {response['evaluation_after']}")
            
        elif response_type == "error":
            return f"Error: {response.get('content', 'Unknown error')}"
            
        else:
            # Generic response
            return str(response.get("content", "No specific advice available for this query."))
    
    def analyze_position(self, fen: str) -> Dict[str, Any]:
        """Analyze a chess position."""
        analysis = self.task_network.analyze_position(fen)
        plan = self.task_network.get_best_plan()
        
        return {
            "analysis": analysis,
            "plan": plan
        }
    
    def close(self):
        """Clean up resources."""
        self.task_network.close()
