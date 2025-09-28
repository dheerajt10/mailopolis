import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useReducer, useCallback } from 'react';
import { apiService } from '../services/api';
const initialState = {
    gameState: null,
    suggestions: [],
    isLoading: false,
    error: null,
    isActive: false,
};
// Reducer function
function gameReducer(state, action) {
    switch (action.type) {
        case 'SET_LOADING':
            return { ...state, isLoading: action.payload };
        case 'SET_ERROR':
            return { ...state, error: action.payload, isLoading: false };
        case 'SET_GAME_STATE':
            return { ...state, gameState: action.payload };
        case 'SET_SUGGESTIONS':
            return { ...state, suggestions: action.payload };
        case 'CLEAR_ERROR':
            return { ...state, error: null };
        case 'RESET_GAME':
            return { ...initialState };
        case 'SET_ACTIVE':
            return { ...state, isActive: action.payload };
        default:
            return state;
    }
}
// Create context
const GameContext = createContext(undefined);
// Provider component
export function GameProvider({ children }) {
    const [state, dispatch] = useReducer(gameReducer, initialState);
    const fetchGameState = useCallback(async () => {
        const gameState = await apiService.getGameState();
        dispatch({ type: 'SET_GAME_STATE', payload: gameState });
    }, []);
    const fetchSuggestions = useCallback(async () => {
        const response = await apiService.getSuggestions();
        dispatch({ type: 'SET_SUGGESTIONS', payload: response.suggestions });
    }, []);
    // Start a new game
    const startGame = useCallback(async () => {
        dispatch({ type: 'SET_LOADING', payload: true });
        dispatch({ type: 'CLEAR_ERROR' });
        try {
            await apiService.startGame();
            await Promise.all([fetchGameState(), fetchSuggestions()]);
            dispatch({ type: 'SET_ACTIVE', payload: true });
        }
        catch (error) {
            dispatch({
                type: 'SET_ERROR',
                payload: error instanceof Error ? error.message : 'Failed to start game',
            });
        }
        finally {
            dispatch({ type: 'SET_LOADING', payload: false });
        }
    }, [fetchGameState, fetchSuggestions]);
    // Refresh game state
    const refreshGameState = useCallback(async () => {
        dispatch({ type: 'SET_LOADING', payload: true });
        dispatch({ type: 'CLEAR_ERROR' });
        try {
            await fetchGameState();
        }
        catch (error) {
            dispatch({
                type: 'SET_ERROR',
                payload: error instanceof Error ? error.message : 'Failed to fetch game state',
            });
        }
        finally {
            dispatch({ type: 'SET_LOADING', payload: false });
        }
    }, [fetchGameState]);
    // Refresh suggestions
    const refreshSuggestions = useCallback(async () => {
        dispatch({ type: 'SET_LOADING', payload: true });
        dispatch({ type: 'CLEAR_ERROR' });
        try {
            await fetchSuggestions();
        }
        catch (error) {
            dispatch({
                type: 'SET_ERROR',
                payload: error instanceof Error ? error.message : 'Failed to fetch suggestions',
            });
        }
        finally {
            dispatch({ type: 'SET_LOADING', payload: false });
        }
    }, [fetchSuggestions]);
    // Stop the game
    const stopGame = useCallback(() => {
        dispatch({ type: 'RESET_GAME' });
    }, []);
    // Play a turn
    const playTurn = useCallback(async (proposal) => {
        dispatch({ type: 'SET_LOADING', payload: true });
        dispatch({ type: 'CLEAR_ERROR' });
        try {
            await apiService.playTurn({ proposal });
            await Promise.all([fetchGameState(), fetchSuggestions()]);
        }
        catch (error) {
            dispatch({
                type: 'SET_ERROR',
                payload: error instanceof Error ? error.message : 'Failed to play turn',
            });
        }
        finally {
            dispatch({ type: 'SET_LOADING', payload: false });
        }
    }, [fetchGameState, fetchSuggestions]);
    const contextValue = {
        gameState: state.gameState,
        suggestions: state.suggestions,
        isLoading: state.isLoading,
        error: state.error,
        isGameActive: state.isActive,
        startGame,
        stopGame,
        refreshGameState,
        refreshSuggestions,
        playTurn,
    };
    return _jsx(GameContext.Provider, { value: contextValue, children: children });
}
// Hook to use game context
export function useGame() {
    const context = useContext(GameContext);
    if (context === undefined) {
        throw new Error('useGame must be used within a GameProvider');
    }
    return context;
}
export default GameContext;
