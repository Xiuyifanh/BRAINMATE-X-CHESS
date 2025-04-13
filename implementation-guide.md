# BrainMate Chess: Implementation Guide

This guide provides detailed instructions for setting up and implementing the BrainMate Chess AI assistant for the AI + Crypto Gaming Hackathon on Starknet.

## Project Structure

```
brainmate-chess/
├── README.md
├── IMPLEMENTATION.md
├── setup.py
├── chess_agent/
│   ├── __init__.py
│   ├── main.py
│   └── hierarchical_agent/
│       ├── __init__.py
│       ├── agent.py
│       └── task_network.py
```

## Setup Instructions

### 1. Prerequisites

- Python 3.7 or higher
- Stockfish chess engine installed on your system
- Git (for version control)

### 2. Installing Stockfish

#### Windows:
1. Download Stockfish from [the official website](https://stockfishchess.org/download/)
2. Extract to a directory (e.g., `C:\stockfish\`)
3. Note the path to the executable (e.g., `C:\stockfish\stockfish-windows-x64.exe`)

#### macOS:
```bash
brew install stockfish
```

#### Linux:
```bash
sudo apt-get install stockfish  # Ubuntu/Debian
# or
sudo pacman -S stockfish        # Arch Linux
```

### 3. Setting Up the Project

```bash
# Clone the repository (or create it if it's a new project)
git clone https://github.com/yourusername/brainmate-chess.git
cd brainmate-chess

# Create the directory structure
mkdir -p chess_agent/hierarchical_agent

# Create empty __init__.py files
touch chess_agent/__init__.py
touch chess_agent/hierarchical_agent/__init__.py

# Install the package
pip install -e .
```

### 4. Adding the Code Files

1. Copy each of the code files to the appropriate location:
   - `setup.py` → Root directory
   - `chess_agent/__init__.py` → Update with version
   - `chess_agent/main.py` → Main application file
   - `chess_agent/hierarchical_agent/agent.py` → Agent implementation
   - `chess_agent/hierarchical_agent/task_network.py` → Task network implementation
   - `chess_agent/hierarchical_agent/__init__.py` → Module initialization

### 5. Running the Application

```bash
# Run directly using the module
python -m chess_agent.main

# Or if installed as a package
chess-ai
```

## Implementation Details

### Core Components

#### 1. Hierarchical Task Network (`task_network.py`)

The hierarchical task network is the brain of the system. It:

- Analyzes chess positions at different levels of abstraction
- Organizes goals into three levels:
  - **Long-term goals**: Overall game strategy
  - **Medium-term goals**: Positional advantages 
  - **Short-term goals**: Immediate tactical moves

Each goal has a priority, description, and optionally a sequence of moves to achieve it.

#### 2. Chess Agent (`agent.py`)

The chess agent acts as an interface between the user and the task network:

- Processes natural language queries
- Routes questions to the appropriate analysis functions
- Formats responses in a human-readable way

#### 3. Main Application (`main.py`)

The main application provides:

- Engine initialization and path detection
- Interactive command-line interface
- Board state management
- Error handling

### Key Algorithms

#### Position Analysis

1. **Phase Detection**: Determining if the position is in the opening, middlegame, or endgame
2. **Material Evaluation**: Counting the piece values for each side
3. **Tactical Opportunity Detection**: Finding checks, captures, and threats
4. **Position Type Classification**: Identifying if the position is open, closed, or tactical

#### Natural Language Processing

The system uses a simple keyword-based approach to classify user queries:

1. **Move Recommendation**: "best move", "what should i play", "recommend"
2. **Strategic Advice**: "strategy", "plan" 
3. **Tactical Analysis**: "tactic", "opportunity"
4. **Position Evaluation**: "evaluate", "assessment", "position"
5. **Move Explanation**: "explain" + "move"

## Starknet Integration Plan

The AI component developed during the hackathon will be integrated with Starknet in the post-hackathon phase. Here's how:

### 1. On-chain Game State

- Store chess positions using FEN notation in Cairo smart contracts
- Implement move validation logic to ensure legal chess moves
- Create a game history record with timestamps for each move

### 2. NFT Integration

- Each chess game can be minted as an NFT with complete game history
- Special games (tournaments, matches against top players) become more valuable
- Custom chess pieces and boards as collectible NFTs

### 3. Tournament System

- Smart contracts for tournament organization and prize distribution
- Rating system stored on-chain for transparent and verifiable rankings
- Automatic matchmaking based on ratings

### 4. Wallet Integration with Cartridge Controller

- Seamless authentication using Cartridge's embedded wallet
- Session tokens for continuous gameplay
- Gas-free user experience with Paymaster implementation

## Testing Strategy

1. **Unit Testing**: Test individual components like the task network and agent
2. **Integration Testing**: Test the full application flow with simulated user input
3. **Position Testing**: Use standard chess positions to verify analysis accuracy
4. **Natural Language Testing**: Test various phrasings of the same question

## Future Improvements

1. **Advanced NLP**: Implement more sophisticated natural language understanding
2. **Learning System**: Train the system to adapt to a player's style over time
3. **Graphical Interface**: Create a web or mobile interface 
4. **Expanded Opening Book**: Include a database of standard chess openings
5. **Multi-language Support**: Add support for multiple human languages

## Contributing

Contributions are welcome! Please see the README for more information on how to contribute to the project.
