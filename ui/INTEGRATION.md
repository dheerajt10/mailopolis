# UI-Backend Integration

This document describes the integration between the Mailopolis UI and the backend API.

## What's Been Integrated

### 1. API Service Layer (`src/services/api.ts`)
- HTTP client using axios for backend communication
- TypeScript types for all API requests and responses
- Service functions for all game endpoints:
  - `startGame()` - Start a new game
  - `getGameState()` - Get current game state
  - `getSuggestions()` - Get proposal suggestions
  - `playTurn()` - Submit a proposal to play a turn

### 2. Game Context (`src/contexts/GameContext.tsx`)
- React context for global game state management
- State management using useReducer
- Automatic error handling and loading states
- Functions to interact with the backend API

### 3. UI Integration
- **Start Game**: Auto-starts game on app load, with manual start button
- **Real-time Stats**: City stats now pull from backend API
- **Proposal System**: Uses real proposals from API with fallback to demo data
- **Turn Submission**: Selecting proposals now submits turns to backend
- **Loading States**: UI shows loading indicators during API calls
- **Error Handling**: Displays error messages when API calls fail

## API Endpoints Used

- `POST /maylopolis/start` - Start new game
- `GET /maylopolis/state` - Get game state
- `GET /maylopolis/suggestions` - Get proposal suggestions  
- `POST /maylopolis/turn` - Submit proposal to play turn

## How to Use

1. Start the backend server (should be running on localhost:8000)
2. Start the UI with `npm run dev`
3. The game will auto-start when the UI loads
4. View real-time city stats in the header
5. Browse proposals from the backend API
6. Select proposals to submit turns and advance the game

## Configuration

The API base URL is configured in `src/services/api.ts`. Currently set to `http://localhost:8000`. Update this if your backend runs on a different port or host.

## Error Handling

- Network errors are caught and displayed in the UI
- Loading states prevent multiple simultaneous requests
- Fallback to demo data if API is unavailable
- User-friendly error messages for debugging
