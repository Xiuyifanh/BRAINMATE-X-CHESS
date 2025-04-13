# BrainMate Chess: AI-Powered Chess Assistant on Starknet

A hierarchical chess AI assistant that provides natural language analysis and recommendations for chess positions. Built for the AI + Crypto Gaming Hackathon on Starknet.


## Overview

BrainMate Chess combines the strategic depth of chess with AI assistance and blockchain technology on Starknet. The assistant helps players understand chess positions through natural language, providing strategic guidance, tactical analysis, and move recommendations.

## Features

- **Hierarchical Planning**: Uses long-term, medium-term, and short-term goals to analyze chess positions
- **Natural Language Interface**: Ask questions about positions in plain English
- **Strategic Analysis**: Get comprehensive position evaluations and strategic advice 
- **Move Explanations**: Understand the reasoning behind recommended moves
- **Starknet Integration**: Designed to integrate with Starknet blockchain (post-hackathon)

## Installation

### Prerequisites

- Python 3.7 or higher
- [Stockfish](https://stockfishchess.org/download/) chess engine installed on your system

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/brainmate-chess.git
cd brainmate-chess

# Install dependencies
pip install -e .

# Optional: Install with Lichess API support
pip install -e ".[lichess]"
```

## Usage

### Command Line Interface

```bash
# Start the interactive CLI
chess-ai

# Or run directly
python -m chess_agent.main
```

### Interactive Commands

Once the CLI is running, you can:

1. **Ask questions about the position**:
   - "What's the best move?"
   - "What's my strategic plan in this position?"
   - "Explain why e4 is good here"
   - "What's the evaluation of this position?"

2. **Change the position**:
   - Type `fen` to enter a new FEN string
   - Type `move e4` to make a move on the board

3. **Exit the program**:
   - Type `quit` to exit

### Example Session

```
Chess AI Assistant
=================
Type 'quit' to exit

Current position (FEN): rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

Enter a question: What's the best move?

I recommend: Play e4
Reasoning: This move supports our strategy to Develop pieces and control the center by making immediate progress.

Enter a question: What's my strategic plan?

Strategic advice: Develop pieces and control the center
Alternative strategies to consider:
1. Ensure king safety

Enter a question: move e4

rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1

Enter a question: What should black play now?

I recommend: Play e5
Reasoning: This move supports our strategy to Contest the center and develop pieces by making immediate progress.
```

## Project Structure

- **Hierarchical Agent**: The core AI that processes chess positions using a hierarchical task network
  - **Long-term goals**: Overall game strategy (attacking/defensive plans)
  - **Medium-term goals**: Positional advantages, piece development, king safety
  - **Short-term tactics**: Immediate moves, captures, threats

- **Natural Language Processing**: Converts player questions to specific analysis requests
  - Understands questions about moves, strategies, tactics, and position evaluation
  - Provides human-readable explanations for recommended moves

- **Chess Engine Integration**: Uses Stockfish to provide accurate position evaluation

## Starknet Integration Plan (Post-Hackathon)

- **On-Chain Game State**: Store chess positions and moves on Starknet blockchain
- **NFT Integration**: Create collectible chess pieces and memorable games as NFTs
- **Tournament System**: Implement verifiable, on-chain tournaments
- **Economic Layer**: Token rewards for achievements and tournaments
- **Cartridge Controller**: Wallet integration for seamless authentication

## Development Roadmap

1. ✅ **Core Chess Engine Integration**
2. ✅ **Hierarchical Agent Implementation**
3. ✅ **Natural Language Interface**
4. 🔄 **Simple UI for Testing** (current phase)
5. 🔜 **Starknet Integration** (post-hackathon)
6. 🔜 **Full UI Implementation** (post-hackathon)
7. 🔜 **Mobile Support** (future)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
