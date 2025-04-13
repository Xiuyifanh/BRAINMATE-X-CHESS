"""
Hierarchical task network for chess analysis and strategic planning.
"""

import chess
import chess.engine
from typing import Dict, List, Any, Optional, Tuple

class ChessGoal:
    """Represents a chess goal at different abstraction levels."""
    def __init__(self, description: str, priority: int, move_sequence: List[str] = None):
        self.description = description
        self.priority = priority  # Higher number = higher priority
        self.move_sequence = move_sequence or []
        self.completed = False
        self.progress = 0.0  # 0.0 to 1.0

class TaskNetwork:
    """Base class for hierarchical task networks."""
    def __init__(self):
        pass
        
    def analyze(self, state: Any) -> Dict[str, Any]:
        """Analyze a state and populate goals."""
        raise NotImplementedError
        
    def get_best_plan(self) -> Dict[str, Any]:
        """Get the best plan based on current goals."""
        raise NotImplementedError

class ChessTaskNetwork(TaskNetwork):
    """Hierarchical task network specifically for chess."""
    
    def __init__(self, engine_path: str):
        super().__init__()
        # Initialize chess engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        
        # Define hierarchical goals
        self.long_term_goals = []     # Overall game strategy
        self.medium_term_goals = []   # Positional advantages
        self.short_term_goals = []    # Immediate tactical considerations
    
    def analyze_position(self, fen: str) -> Dict[str, Any]:
        """Analyze a chess position and populate goal hierarchies."""
        board = chess.Board(fen)
        
        # Clear previous goals
        self.long_term_goals = []
        self.medium_term_goals = []
        self.short_term_goals = []
        
        # Get engine evaluation
        result = self.engine.analyse(board, chess.engine.Limit(time=0.2), multipv=3)
        
        # Populate short-term tactical goals (immediate moves)
        for i, pv_info in enumerate(result):
            move = pv_info["pv"][0]
            eval_score = pv_info["score"].relative
            
            # Create a short-term goal for this move
            move_san = board.san(move)
            self.short_term_goals.append(
                ChessGoal(
                    description=f"Play {move_san}",
                    priority=3-i,  # First move has highest priority
                    move_sequence=[move.uci()]
                )
            )
        
        # Populate medium-term goals (positional considerations)
        self._identify_medium_term_goals(board)
        
        # Populate long-term goals (strategic plans)
        self._identify_long_term_goals(board, str(result[0]["score"].relative))
        
        return {
            "long_term": [goal.__dict__ for goal in self.long_term_goals],
            "medium_term": [goal.__dict__ for goal in self.medium_term_goals],
            "short_term": [goal.__dict__ for goal in self.short_term_goals]
        }
    
    def _identify_medium_term_goals(self, board: chess.Board):
        """Identify medium-term positional goals."""
        # These are simplified examples - you can expand these
        
        # 1. Control the center
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        controlled_center = sum(1 for sq in center_squares 
                             if board.piece_at(sq) and board.piece_at(sq).color == board.turn)
        
        if controlled_center < 2:
            self.medium_term_goals.append(
                ChessGoal(
                    description="Control the center with pawns or pieces",
                    priority=5
                )
            )
        
        # 2. Develop pieces
        if board.fullmove_number <= 10:
            developed_pieces = 0
            
            # Check knights and bishops
            starting_squares = {
                chess.WHITE: [chess.B1, chess.G1, chess.C1, chess.F1],
                chess.BLACK: [chess.B8, chess.G8, chess.C8, chess.F8]
            }
            
            for piece_type in [chess.KNIGHT, chess.BISHOP]:
                for piece_square in board.pieces(piece_type, board.turn):
                    if piece_square not in starting_squares[board.turn]:
                        developed_pieces += 1
            
            if developed_pieces < 4:
                self.medium_term_goals.append(
                    ChessGoal(
                        description="Develop minor pieces",
                        priority=4
                    )
                )
        
        # 3. Castle if king is in center
        king_square = board.king(board.turn)
        if ((board.turn == chess.WHITE and king_square == chess.E1) or 
            (board.turn == chess.BLACK and king_square == chess.E8)):
            if board.has_castling_rights(board.turn):
                self.medium_term_goals.append(
                    ChessGoal(
                        description="Castle to safety",
                        priority=6
                    )
                )
    
    def _identify_long_term_goals(self, board: chess.Board, evaluation: str):
        """Identify long-term strategic goals."""
        
        # Determine game phase
        total_pieces = bin(board.occupied).count('1')
        if total_pieces > 24:
            phase = "opening"
        elif total_pieces > 10:
            phase = "middlegame"
        else:
            phase = "endgame"
        
        # Add phase-specific goals
        if phase == "opening":
            self.long_term_goals.append(
                ChessGoal(
                    description="Develop pieces and control the center",
                    priority=8
                )
            )
            self.long_term_goals.append(
                ChessGoal(
                    description="Ensure king safety",
                    priority=7
                )
            )
        
        elif phase == "middlegame":
            # Check material balance
            white_material = self._count_material(board, chess.WHITE)
            black_material = self._count_material(board, chess.BLACK)
            
            advantage = white_material - black_material
            advantage = advantage if board.turn == chess.WHITE else -advantage
            
            if advantage > 3:  # Significant material advantage
                self.long_term_goals.append(
                    ChessGoal(
                        description="Trade pieces to simplify into a winning endgame",
                        priority=8
                    )
                )
            elif advantage < -3:  # Material disadvantage
                self.long_term_goals.append(
                    ChessGoal(
                        description="Create complications and tactical opportunities",
                        priority=8
                    )
                )
            else:  # Roughly equal
                self.long_term_goals.append(
                    ChessGoal(
                        description="Improve piece positioning and create weaknesses in opponent's camp",
                        priority=7
                    )
                )
        
        else:  # Endgame
            # Add endgame-specific goals
            self.long_term_goals.append(
                ChessGoal(
                    description="Activate king and create passed pawns",
                    priority=8
                )
            )
            
            # If up material, aim to trade
            try:
                eval_value = int(evaluation)
                if eval_value > 200:  # Significant advantage
                    self.long_term_goals.append(
                        ChessGoal(
                            description="Exchange pieces but not pawns",
                            priority=7
                        )
                    )
            except ValueError:
                # Handle non-integer evaluations (mate scores, etc.)
                pass
    
    def _count_material(self, board: chess.Board, color: chess.Color) -> int:
        """Count material value for a side."""
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        return sum(len(board.pieces(piece_type, color)) * values[piece_type] 
                  for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN])
    
    def get_best_plan(self) -> Dict[str, Any]:
        """Get the best plan based on the current goals."""
        # Combine all goals and sort by priority
        all_goals = self.long_term_goals + self.medium_term_goals + self.short_term_goals
        sorted_goals = sorted(all_goals, key=lambda g: g.priority, reverse=True)
        
        if not sorted_goals:
            return {"description": "No clear plan identified", "moves": []}
        
        # The highest priority short-term goal determines the immediate move
        immediate_moves = [g for g in self.short_term_goals if g.move_sequence]
        if immediate_moves:
            top_move = sorted(immediate_moves, key=lambda g: g.priority, reverse=True)[0]
            
            # Find the related long-term strategy
            strategy = self.long_term_goals[0].description if self.long_term_goals else "No specific strategy"
            
            return {
                "description": strategy,
                "immediate_action": top_move.description,
                "moves": top_move.move_sequence,
                "reasoning": self._generate_reasoning(strategy, top_move.description)
            }
        
        return {"description": "No clear moves identified", "moves": []}
    
    def _generate_reasoning(self, strategy: str, move: str) -> str:
        """Generate reasoning that connects the strategy to the specific move."""
        # This can be expanded for more sophisticated reasoning
        return f"This move supports our strategy to {strategy.lower()} by making immediate progress."
    
    def process_natural_language(self, fen: str, query: str) -> Dict[str, Any]:
        """Process a natural language query about the chess position."""
        board = chess.Board(fen)
        query = query.lower()
        
        # First analyze the position to populate goals
        self.analyze_position(fen)
        
        # Handle different query types
        if "best move" in query or "what should i play" in query or "recommend" in query:
            plan = self.get_best_plan()
            return {
                "type": "move_recommendation",
                "content": plan["immediate_action"],
                "reasoning": plan["reasoning"],
                "strategy": plan["description"]
            }
        
        elif "strategy" in query or "plan" in query:
            # Return long-term strategic advice
            if not self.long_term_goals:
                return {
                    "type": "strategy_advice",
                    "content": "No clear strategic goals identified for this position."
                }
            
            # Sort goals by priority
            strategies = sorted(self.long_term_goals, key=lambda g: g.priority, reverse=True)
            return {
                "type": "strategy_advice",
                "content": strategies[0].description,
                "additional_options": [g.description for g in strategies[1:]]
            }
        
        elif "tactic" in query or "opportunity" in query:
            # Look for tactical opportunities
            tactics = self._identify_tactics(board)
            if not tactics:
                return {
                    "type": "tactical_advice",
                    "content": "No immediate tactical opportunities found."
                }
            
            return {
                "type": "tactical_advice",
                "content": tactics[0]["description"],
                "moves": tactics[0]["moves"]
            }
        
        elif "evaluate" in query or "assessment" in query or "position" in query:
            # Provide position evaluation
            result = self.engine.analyse(board, chess.engine.Limit(time=0.2))
            eval_score = result["score"].relative
            
            # Determine position character
            position_type = self._determine_position_type(board)
            
            return {
                "type": "position_evaluation",
                "evaluation": str(eval_score),
                "position_type": position_type,
                "suggested_approach": self._suggest_approach(eval_score, position_type)
            }
        
        elif "explain" in query and "move" in query:
            # Extract the move if it's in the query
            # This is a simplified extraction - would need more robust parsing
            moves = [word for word in query.split() if len(word) >= 2 and any(c.isalpha() for c in word) and any(c.isdigit() for c in word)]
            
            if moves:
                try:
                    move = chess.Move.from_uci(moves[0]) if len(moves[0]) == 4 else board.parse_san(moves[0])
                    return self._explain_move(board, move)
                except ValueError:
                    pass
            
            # If no specific move found, explain the best move
            result = self.engine.analyse(board, chess.engine.Limit(time=0.2))
            best_move = result["pv"][0]
            return self._explain_move(board, best_move)
            
        else:
            # Default to providing the best move recommendation
            plan = self.get_best_plan()
            return {
                "type": "move_recommendation",
                "content": plan["immediate_action"],
                "reasoning": plan["reasoning"]
            }
    
    def _identify_tactics(self, board: chess.Board) -> List[Dict[str, Any]]:
        """Identify tactical opportunities in the position."""
        tactics = []
        
        # Check for checks
        for move in board.legal_moves:
            board_copy = board.copy()
            board_copy.push(move)
            
            if board_copy.is_check():
                tactics.append({
                    "description": f"Check with {board.san(move)}",
                    "moves": [move.uci()],
                    "priority": 5
                })
        
        # Check for captures
        for move in board.legal_moves:
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    piece_value = {
                        chess.PAWN: 1,
                        chess.KNIGHT: 3,
                        chess.BISHOP: 3,
                        chess.ROOK: 5,
                        chess.QUEEN: 9,
                        chess.KING: 0
                    }.get(captured_piece.piece_type, 0)
                    
                    attacker = board.piece_at(move.from_square)
                    attacker_value = {
                        chess.PAWN: 1,
                        chess.KNIGHT: 3,
                        chess.BISHOP: 3,
                        chess.ROOK: 5,
                        chess.QUEEN: 9,
                        chess.KING: 0
                    }.get(attacker.piece_type, 0)
                    
                    # Check if this is a favorable exchange
                    if piece_value >= attacker_value:
                        tactics.append({
                            "description": f"Capture {self._piece_name(captured_piece)} with {board.san(move)}",
                            "moves": [move.uci()],
                            "priority": piece_value
                        })
        
        # Sort tactics by priority
        return sorted(tactics, key=lambda t: t["priority"], reverse=True)
    
    def _determine_position_type(self, board: chess.Board) -> str:
        """Determine the character of the position (open, closed, tactical, etc.)."""
        # Count center pawns to determine if position is open or closed
        center_pawns = 0
        for square in [chess.D4, chess.E4, chess.D5, chess.E5]:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                center_pawns += 1
        
        # Count total pieces to determine game phase
        total_pieces = bin(board.occupied).count('1')
        
        if center_pawns <= 1:
            return "Open position"
        elif center_pawns >= 3:
            return "Closed position"
        elif total_pieces <= 10:
            return "Endgame position"
        else:
            # Count recent captures to see if position is tactical
            if board.fullmove_number > 10 and board.halfmove_clock < 3:
                return "Tactical position"
            return "Semi-open position"
    
    def _suggest_approach(self, evaluation, position_type: str) -> str:
        """Suggest an approach based on evaluation and position type."""
        eval_str = str(evaluation)
        # Convert to integer if possible
        try:
            eval_int = int(eval_str)
        except ValueError:
            # Handle mate scores
            if "#" in eval_str:
                return "There's a forced mate. Follow the tactical sequence."
            eval_int = 0
        
        if abs(eval_int) < 30:
            # Equal position
            if "Open" in position_type:
                return "The position is roughly equal and open. Focus on piece activity and creating imbalances."
            elif "Closed" in position_type:
                return "The position is roughly equal but closed. Consider a positional maneuver or breakthrough."
            elif "Tactical" in position_type:
                return "The position is balanced but tactical. Look for combinations and tactical opportunities."
            else:
                return "The position is balanced. Focus on improving your worst-placed piece."
                
        elif eval_int > 200:
            # Significant advantage
            return "You have a significant advantage. Simplify the position and avoid unnecessary complications."
            
        elif eval_int < -200:
            # Significant disadvantage
            return "You are at a disadvantage. Create complications and look for tactical chances."
            
        elif eval_int > 0:
            # Slight advantage
            return "You have a slight advantage. Focus on incrementally improving your position."
            
        else:
            # Slight disadvantage
            return "You have a slight disadvantage. Focus on equalizing the position through careful defense."
    
    def _explain_move(self, board: chess.Board, move: chess.Move) -> Dict[str, Any]:
        """Generate an explanation for a specific move."""
        move_san = board.san(move)
        
        # Check move characteristics
        is_capture = board.is_capture(move)
        
        # Make the move to see its effects
        board_copy = board.copy()
        board_copy.push(move)
        gives_check = board_copy.is_check()
        
        # Determine piece type
        piece = board.piece_at(move.from_square)
        piece_type = self._piece_name(piece) if piece else "Unknown"
        
        # Basic explanation
        explanation = f"The move {move_san} "
        
        if is_capture:
            captured = board.piece_at(move.to_square)
            explanation += f"captures a {self._piece_name(captured)}. "
        else:
            explanation += "repositions your " + piece_type + ". "
        
        if gives_check:
            explanation += "It gives check to the opponent's king. "
        
        # Add positional context
        if piece and piece.piece_type == chess.PAWN:
            if move.to_square in [chess.D4, chess.E4, chess.D5, chess.E5]:
                explanation += "This move helps control the center. "
            
            promotion_rank = 7 if piece.color == chess.WHITE else 0
            if chess.square_rank(move.to_square) == promotion_rank - 1:
                explanation += "This pawn is now one step away from promotion. "
                
        elif piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            if move.from_square in [chess.B1, chess.G1, chess.B8, chess.G8, chess.C1, chess.F1, chess.C8, chess.F8]:
                explanation += "This develops a piece from its starting position. "
        
        # Analyze tactical implications
        result = self.engine.analyse(board_copy, chess.engine.Limit(time=0.1))
        eval_after = result["score"].relative
        
        # Compare with evaluation before the move
        result_before = self.engine.analyse(board, chess.engine.Limit(time=0.1))
        eval_before = result_before["score"].relative
        
        return {
            "type": "move_explanation",
            "move": move_san,
            "explanation": explanation.strip(),
            "evaluation_before": str(eval_before),
            "evaluation_after": str(eval_after)
        }
    
    def _piece_name(self, piece: chess.Piece) -> str:
        """Get the name of a chess piece."""
        if not piece:
            return "empty square"
            
        names = {
            chess.PAWN: "pawn",
            chess.KNIGHT: "knight",
            chess.BISHOP: "bishop",
            chess.ROOK: "rook",
            chess.QUEEN: "queen",
            chess.KING: "king"
        }
        color = "white" if piece.color == chess.WHITE else "black"
        return f"{color} {names[piece.piece_type]}"
    
    def close(self):
        """Close the engine."""
        if self.engine:
            self.engine.quit()
