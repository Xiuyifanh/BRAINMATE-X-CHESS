# BrainMate Chess: Starknet Integration Plan

This document outlines the plan for integrating the BrainMate Chess AI assistant with Starknet blockchain technology after the hackathon.

## Overview

After developing the AI components during the hackathon, we will integrate with Starknet to create a fully on-chain chess experience enhanced by AI. This integration will leverage Starknet's scalability, low-cost transactions, and developer tools to create a seamless chess gaming platform.

## Technical Components

### 1. Cairo Smart Contracts

#### Game State Contract

```cairo
#[contract]
mod ChessGame {
    // Game state storage
    struct Storage {
        games: LegacyMap::<u256, Game>,
        game_count: u256,
        player_games: LegacyMap::<(ContractAddress, u256), u256>,
        player_game_counts: LegacyMap::<ContractAddress, u256>,
    }

    // Game structure
    struct Game {
        white_player: ContractAddress,
        black_player: ContractAddress,
        current_fen: felt252,
        moves: Array<Move>,
        status: u8,  // 0: ongoing, 1: white wins, 2: black wins, 3: draw
        last_move_timestamp: u64,
        tournament_id: u256,
    }

    // Move structure
    struct Move {
        from_square: u8,
        to_square: u8,
        promotion_piece: u8,  // 0: none, 1: queen, 2: rook, 3: bishop, 4: knight
        timestamp: u64,
    }

    // Events
    #[event]
    fn GameCreated(game_id: u256, white_player: ContractAddress, black_player: ContractAddress) {}

    #[event]
    fn MoveMade(game_id: u256, from_square: u8, to_square: u8, promotion_piece: u8) {}

    #[event]
    fn GameEnded(game_id: u256, result: u8) {}

    // Functions
    #[external]
    fn create_game(white_player: ContractAddress, black_player: ContractAddress, tournament_id: u256) -> u256 {
        // Implementation details
    }

    #[external]
    fn make_move(game_id: u256, from_square: u8, to_square: u8, promotion_piece: u8) {
        // Implementation details
        // Includes move validation
    }

    #[view]
    fn get_game(game_id: u256) -> Game {
        // Implementation details
    }

    #[view]
    fn is_move_valid(game_id: u256, from_square: u8, to_square: u8) -> bool {
        // Implementation details
    }

    // Additional functions for game management, player stats, etc.
}
```

#### Chess NFT Contract

```cairo
#[contract]
mod ChessNFT {
    // ERC721 implementation
    use openzeppelin::token::erc721::ERC721;

    // Storage
    struct Storage {
        game_metadata: LegacyMap::<u256, GameMetadata>,
    }

    // Game metadata
    struct GameMetadata {
        game_id: u256,
        pgn: felt252,  // Portable Game Notation (compressed)
        white_player: ContractAddress,
        black_player: ContractAddress,
        timestamp: u64,
        tournament_id: u256,
    }

    // Events
    #[event]
    fn GameMinted(token_id: u256, game_id: u256) {}

    // Functions
    #[external]
    fn mint_game_nft(game_id: u256, recipient: ContractAddress) -> u256 {
        // Implementation details
    }

    #[view]
    fn get_game_metadata(token_id: u256) -> GameMetadata {
        // Implementation details
    }
}
```

#### Tournament Contract

```cairo
#[contract]
mod ChessTournament {
    // Storage
    struct Storage {
        tournaments: LegacyMap::<u256, Tournament>,
        tournament_count: u256,
        player_tournaments: LegacyMap::<(ContractAddress, u256), u256>,
        player_tournament_counts: LegacyMap::<ContractAddress, u256>,
    }

    // Tournament structure
    struct Tournament {
        name: felt252,
        start_time: u64,
        end_time: u64,
        entry_fee: u256,
        prize_pool: u256,
        participants: Array<ContractAddress>,
        games: Array<u256>,
        status: u8,  // 0: registration, 1: ongoing, 2: completed
        winner: ContractAddress,
    }

    // Events
    #[event]
    fn TournamentCreated(tournament_id: u256, name: felt252) {}

    #[event]
    fn PlayerRegistered(tournament_id: u256, player: ContractAddress) {}

    #[event]
    fn TournamentStarted(tournament_id: u256) {}

    #[event]
    fn TournamentEnded(tournament_id: u256, winner: ContractAddress) {}

    // Functions
    #[external]
    fn create_tournament(name: felt252, start_time: u64, end_time: u64, entry_fee: u256) -> u256 {
        // Implementation details
    }

    #[external]
    fn register_for_tournament(tournament_id: u256) {
        // Implementation details
    }

    #[external]
    fn start_tournament(tournament_id: u256) {
        // Implementation details
    }

    #[external]
    fn end_tournament(tournament_id: u256, winner: ContractAddress) {
        // Implementation details
    }
}
```

### 2. Cartridge Controller Integration

The Cartridge Controller will be used to provide a seamless wallet experience:

1. **Self-Custodial Wallets**: Allow players to create or import wallets directly in the app
2. **Passkey Authentication**: Secure and user-friendly authentication
3. **Session Tokens**: Enable continuous gameplay without requiring signatures for each move
4. **Paymaster Integration**: Subsidize gas fees for players to provide a gas-free experience

```javascript
// Example front-end integration with Cartridge
import { CartridgeController } from '@cartridge/controller';

const cartridge = new CartridgeController({
  appName: 'BrainMate Chess',
  chains: [{
    id: 'SN_MAIN',
    rpcUrl: 'https://starknet.infura.io/v3/your-project-id'
  }]
});

// Initialize wallet
async function initWallet() {
  try {
    const account = await cartridge.connect();
    console.log('Connected account:', account.address);
    return account;
  } catch (error) {
    console.error('Failed to connect wallet:', error);
  }
}

// Make a move on-chain
async function makeMove(gameId, fromSquare, toSquare, promotionPiece = 0) {
  const account = await cartridge.getAccount();
  
  // Prepare the transaction
  const tx = {
    contractAddress: CHESS_GAME_CONTRACT_ADDRESS,
    entrypoint: 'make_move',
    calldata: [gameId, fromSquare, toSquare, promotionPiece]
  };
  
  // Send the transaction with paymaster to cover gas
  const result = await account.execute([tx], {
    paymaster: {
      entrypoint: 'sponsor_txn',
      // Additional paymaster configuration
    }
  });
  
  return result;
}
```

### 3. DayDreams AI Integration

The DayDreams framework will be used to connect the AI system with blockchain interactions:

```javascript
// Example integration of AI with blockchain
import { DayDreams, AgentTask } from 'daydreams';

// Create a chess AI agent
const chessAgent = new DayDreams.Agent({
  name: 'ChessAdvisor',
  tasks: [
    new AgentTask({
      name: 'analyzePosition',
      async execute(fen) {
        // Call the AI analysis
        const analysis = await aiService.analyzePosition(fen);
        return analysis;
      }
    }),
    new AgentTask({
      name: 'suggestMove',
      async execute(fen) {
        // Get AI move recommendation
        const suggestion = await aiService.getBestMove(fen);
        return suggestion;
      }
    }),
    new AgentTask({
      name: 'executeMove',
      async execute(gameId, move) {
        // Translate chess notation to contract parameters
        const { fromSquare, toSquare, promotion } = translateMove(move);
        
        // Execute the move on-chain
        return await makeMove(gameId, fromSquare, toSquare, promotion);
      }
    })
  ]
});

// Example agent usage
async function getAndPlayAIMove(gameId, fen) {
  // First get AI suggestion
  const suggestion = await chessAgent.execute('suggestMove', fen);
  
  // Then execute it on-chain
  const result = await chessAgent.execute('executeMove', gameId, suggestion.move);
  
  return {
    suggestion,
    transactionResult: result
  };
}
```

## Integration Architecture

The complete system will have the following components:

1. **Frontend Application**:
   - React-based web application
   - Chessboard visualization
   - AI assistant interface
   - Wallet integration

2. **Backend Services**:
   - AI engine for chess analysis
   - Game state management
   - Tournament handling
   - Player statistics

3. **Blockchain Layer**:
   - Smart contracts on Starknet
   - NFT management
   - On-chain game verification
   - Tournament prize distribution

4. **AI Components**:
   - Hierarchical task network
   - Natural language processing
   - Move recommendation engine
   - Strategic analysis

## Data Flow

1. **Player Initiates Game**:
   - Connect wallet via Cartridge
   - Create game or join existing game
   - Transaction recorded on Starknet

2. **During Gameplay**:
   - Player requests AI assistance
   - AI analyzes current position
   - Player makes move
   - Move validated and recorded on-chain
   - Opponent notified

3. **Game Completion**:
   - Result recorded on-chain
   - Game available to mint as NFT
   - Player ratings updated
   - Tournament standings updated (if applicable)

## Implementation Timeline

### Phase 1: Post-Hackathon (Weeks 1-2)
- Set up Cairo development environment
- Implement basic game state contract
- Create simple frontend for testing

### Phase 2: Smart Contract Development (Weeks 3-4)
- Develop full game contract with validation
- Implement NFT contract
- Create tournament contract

### Phase 3: Frontend Integration (Weeks 5-6)
- Integrate Cartridge Controller
- Connect AI components with frontend
- Implement game visualization

### Phase 4: Testing & Optimization (Weeks 7-8)
- Test on Starknet testnet
- Optimize gas usage
- Security audits

### Phase 5: Launch & Marketing (Weeks 9-10)
- Deploy to Starknet mainnet
- Organize initial tournaments
- Community building

## Resources

- [Starknet Documentation](https://docs.starknet.io/documentation/)
- [Cairo Book](https://book.cairo-lang.org/)
- [Starknet By Example](https://starknet-by-example.voyager.online/)
- [Cartridge Controller Documentation](https://www.cartridge.gg/)
- [Dojo Game Engine](https://www.dojoengine.org/)

## Conclusion

The integration of BrainMate Chess with Starknet will create a unique gaming experience that combines the strategic depth of chess with the transparency and ownership benefits of blockchain technology. The AI components developed during the hackathon will be seamlessly connected to on-chain functionality, providing players with an enhanced chess experience that includes strategic guidance, verifiable gameplay, and economic incentives.
