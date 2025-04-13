"""
Main application for BrainMate Chess AI Assistant.
"""

import chess
import chess.engine
import time
import os
import sys
from chess_agent.hierarchical_agent.agent import ChessAgent

def find_stockfish_path():
    """Find Stockfish engine path."""
    # Try some common paths
    common_paths = [
        "stockfish",  # If in PATH
        "./stockfish",
        "/usr/local/bin/stockfish",
        "/usr/bin/stockfish",
        "C:\\Program Files\\stockfish\\stockfish.exe",
        "C:\\stockfish\\stockfish.exe"
    ]
    
    for path in common_paths:
        try:
            # Try to run a simple command to see if Stockfish is available
            engine = chess.engine.SimpleEngine.popen_uci(path)
            engine.quit()
            return path
        except (FileNotFoundError, chess.engine.EngineTerminatedError):
            continue
    
    return None

def main():
    """Main function for the chess AI assistant."""
    print("BrainMate Chess AI Assistant")
    print("============================")
    
    # Find Stockfish path
    engine_path = os.environ.get("STOCKFISH_PATH")
    if not engine_path:
        engine_path = find_stockfish_path()
    
    if not engine_path:
        print("Error: Stockfish chess engine not found.")
        print("Please install Stockfish and either:")
        print("1. Add it to your PATH, or")
        print("2. Set the STOCKFISH_PATH environment variable, or")
        print("3. Provide the path when prompted.")
        
        # Ask for the path
        engine_path = input("\nEnter the path to Stockfish engine: ").strip()
        if not engine_path:
            print("No path provided. Exiting.")
            sys.exit(1)
    
    # Try to initialize the engine
    try:
        test_engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        test_engine.quit()
        print(f"Successfully connected to Stockfish at: {engine_path}")
    except Exception as e:
        print(f"Error initializing Stockfish: {e}")
        sys.exit(1)
    
    # Create the chess agent
    agent = ChessAgent(engine_path)
    
    # Run interactive mode
    run_interactive_mode(agent)

def run_interactive_mode(agent):
    """Run an interactive command-line interface for testing the agent."""
    print("\nInteractive Chess Assistant")
    print("=========================")
    print("Type 'quit' to exit")
    print("Type 'fen' to enter a new position (using FEN notation)")
    print("Type 'move [x]' to make a move (e.g., 'move e4')")
    print("Or ask any question about the position, such as:")
    print("  - What's the best move?")
    print("  - What's my strategic plan?")
    print("  - Evaluate this position")
    print("  - Explain why e4 is good here")
    print()
    
    # Default starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    
    print(f"Current position (FEN): {fen}")
    print(board)
    
    while True:
        # Get user input
        user_input = input("\nEnter your question: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            break
        
        elif user_input.lower() == 'fen':
            # Allow user to enter a new FEN
            new_fen = input("Enter FEN: ").strip()
            try:
                board = chess.Board(new_fen)
                fen = new_fen
                print(board)
            except ValueError as e:
                print(f"Invalid FEN: {e}")
                
        elif user_input.lower().startswith('move '):
            # Make a move on the board
            move_text = user_input[5:].strip()
            try:
                # Try as SAN notation (e.g., "e4", "Nf3")
                move = board.parse_san(move_text)
                board.push(move)
                fen = board.fen()
                print(board)
            except ValueError:
                try:
                    # Try as UCI notation (e.g., "e2e4")
                    move = chess.Move.from_uci(move_text)
                    if move in board.legal_moves:
                        board.push(move)
                        fen = board.fen()
                        print(board)
                    else:
                        print(f"Illegal move: {move_text}")
                except ValueError:
                    print(f"Invalid move: {move_text}. Use algebraic notation like 'e4' or 'Nf3'.")
        
        elif user_input:
            # Process the query through the agent
            try:
                print("Analyzing...")
                response = agent.process_request(user_input, fen)
                print("\n" + response["formatted"])
            except Exception as e:
                print(f"Error processing request: {e}")
    
    # Clean up
    agent.close()
    print("Exiting BrainMate Chess AI Assistant. Goodbye!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
