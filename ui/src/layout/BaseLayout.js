import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useMemo, useState } from 'react';
import { CityMap } from '../city/CityMap';
import { useGame } from '../contexts/GameContext';
import './BaseLayout.css';
import { LogsPanel } from '../components/LogsPanel';
const formatImpactValue = (value) => {
    if (value == null)
        return '0';
    return value >= 0 ? `+${value}` : `${value}`;
};
const formatDepartmentName = (department) => (department ?? '')
    .replace(/_/g, ' ')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/\s+/g, ' ')
    .trim();
const formatProposalTimestamp = (timestamp) => {
    if (!timestamp) {
        return 'just now';
    }
    try {
        return new Date(timestamp).toLocaleString(undefined, {
            dateStyle: 'medium',
            timeStyle: 'short',
        });
    }
    catch (error) {
        return timestamp;
    }
};
const formatCurrency = (value) => `$${(value ?? 0).toLocaleString()}`;
export function BaseLayout() {
    const [activeProposalId, setActiveProposalId] = useState(null);
    const [logsOpen, setLogsOpen] = useState(false);
    const { gameState, suggestions, isLoading, error, isGameActive, startGame, stopGame, refreshGameState, refreshSuggestions, playTurn, } = useGame();
    const proposals = useMemo(() => suggestions ?? [], [suggestions]);
    const activeProposal = activeProposalId == null
        ? null
        : proposals.find((proposal) => proposal.id === activeProposalId) ?? null;
    const activeEvents = gameState?.active_events ?? [];
    const hasActiveGame = isGameActive;
    const handleProposalOpen = (id) => {
        setActiveProposalId(id);
    };
    const handleProposalClose = () => {
        setActiveProposalId(null);
    };
    const handleProposalSelect = async (proposal) => {
        try {
            await playTurn({
                title: proposal.title,
                description: proposal.description,
                target_department: proposal.target_department,
                sustainability_impact: proposal.sustainability_impact,
                economic_impact: proposal.economic_impact,
                political_impact: proposal.political_impact,
            });
            setActiveProposalId(null);
        }
        catch (error) {
            console.error('Failed to play turn:', error);
            // Error is already handled by the playTurn function in GameContext
        }
    };
    const handleStartGame = async () => {
        await startGame();
        setActiveProposalId(null);
    };
    const handleStopGame = () => {
        stopGame();
        setActiveProposalId(null);
    };
    const handleRefreshSuggestions = async () => {
        await refreshSuggestions();
    };
    return (_jsxs("div", { className: "app-shell", children: [_jsxs("div", { className: "app-frame", children: [_jsxs("header", { className: "app-header", "aria-label": "Mailopolis city overview", children: [_jsxs("div", { className: "navbar-brand", children: [_jsx("span", { className: "navbar-logo", "aria-hidden": "true", children: "\u2709\uFE0F" }), _jsxs("div", { className: "navbar-text", children: [_jsx("span", { className: "navbar-title", children: "Mailopolis" }), _jsx("span", { className: "navbar-subtitle", children: "City Control Center" })] })] }), _jsxs("dl", { className: "city-stats", children: [_jsxs("div", { className: "city-stat city-stat--budget", children: [_jsx("dt", { children: "Budget" }), _jsx("dd", { children: gameState ? `$${(gameState.city_stats.budget / 1000000).toFixed(1)}M` : '--' })] }), _jsxs("div", { className: "city-stat city-stat--sustainability", children: [_jsx("dt", { children: "Sustainability" }), _jsx("dd", { children: gameState?.city_stats.sustainability_score ?? '--' })] }), _jsxs("div", { className: "city-stat city-stat--economy", children: [_jsx("dt", { children: "Economy" }), _jsx("dd", { children: gameState ? `${gameState.city_stats.economic_growth}%` : '--' })] }), _jsxs("div", { className: "city-stat city-stat--approval", children: [_jsx("dt", { children: "Approval" }), _jsx("dd", { children: gameState ? `${gameState.city_stats.public_approval}%` : '--' })] }), _jsxs("div", { className: "city-stat city-stat--infrastructure", children: [_jsx("dt", { children: "Infrastructure" }), _jsx("dd", { children: gameState ? `${gameState.city_stats.infrastructure_health}%` : '--' })] }), _jsxs("div", { className: "city-stat city-stat--happiness", children: [_jsx("dt", { children: "Happiness" }), _jsx("dd", { children: gameState ? `${gameState.city_stats.population_happiness}%` : '--' })] }), _jsxs("div", { className: "city-stat city-stat--corruption", children: [_jsx("dt", { children: "Corruption" }), _jsx("dd", { children: gameState ? `${gameState.city_stats.corruption_level}%` : '--' })] })] })] }), _jsxs("div", { className: "app-content", children: [_jsxs("aside", { className: "proposal-sidebar", "aria-label": "Strategic proposals", children: [_jsxs("div", { className: "simulation-controls", children: [_jsxs("header", { className: "simulation-controls__header", children: [_jsx("h2", { className: "simulation-controls__title", children: "Simulation Control" }), _jsxs("div", { className: `simulation-controls__status${isLoading ? ' simulation-controls__status--loading' : ''}`, children: [_jsx("span", { className: "simulation-controls__status-dot", "aria-hidden": "true" }), _jsx("span", { children: hasActiveGame
                                                                    ? `Turn ${gameState?.turn ?? 0}`
                                                                    : 'Simulation idle' }), activeEvents.length > 0 && (_jsxs("span", { className: "simulation-controls__events", children: [activeEvents.length, " active events"] })), gameState?.is_game_over && (_jsx("span", { className: "simulation-controls__badge", children: "Game over" }))] })] }), _jsx("div", { className: "simulation-controls__buttons", children: !hasActiveGame ? (_jsx("button", { className: "start-game-btn", onClick: handleStartGame, disabled: isLoading, children: isLoading ? 'Starting…' : 'Start Simulation' })) : (_jsxs(_Fragment, { children: [_jsx("button", { className: "refresh-btn", onClick: refreshGameState, disabled: isLoading, children: isLoading ? 'Refreshing…' : 'Refresh State' }), _jsx("button", { className: "refresh-btn", onClick: handleRefreshSuggestions, disabled: isLoading, children: isLoading ? 'Updating…' : 'Refresh Suggestions' }), _jsx("button", { className: "stop-game-btn", onClick: handleStopGame, disabled: isLoading, children: "Stop Simulation" })] })) }), error && (_jsx("div", { className: "simulation-controls__error", role: "alert", children: error }))] }), _jsxs("div", { className: "policy-proposals", children: [_jsxs("header", { className: "policy-proposals__header", children: [_jsx("h2", { className: "policy-proposals__title", children: "Strategic Proposals" }), _jsx("p", { className: "policy-proposals__subtitle", children: "Latest moves surfaced by the Maylopolis cabinet." })] }), _jsxs("div", { className: "proposal-list", children: [proposals.length === 0 && (_jsx("div", { className: "proposal-list__empty", children: hasActiveGame
                                                            ? 'No proposals available yet. Refresh suggestions to pull new ideas from departments.'
                                                            : 'Start the simulation to receive live proposals from departments.' })), proposals.map((proposal) => (_jsxs("article", { className: "proposal-card", children: [_jsxs("header", { className: "proposal-card__top", children: [_jsx("h3", { children: proposal.title }), _jsx("button", { type: "button", className: "proposal-card__select", onClick: () => handleProposalSelect(proposal), disabled: isLoading || !hasActiveGame, children: isLoading ? 'Working…' : hasActiveGame ? 'Select' : 'Start game first' })] }), _jsxs("div", { className: "proposal-card__summary", children: [_jsx("span", { className: "proposal-card__department", children: formatDepartmentName(proposal.target_department) || 'Unknown' }), _jsxs("button", { type: "button", className: "proposal-card__info", "aria-label": `View details for ${proposal.title}`, onClick: () => handleProposalOpen(proposal.id), children: [_jsx("span", { className: "proposal-card__info-text", children: "More info" }), _jsx("span", { className: "proposal-card__info-icon", "aria-hidden": "true", children: "\u2192" })] })] }), _jsxs("div", { className: "proposal-card__impacts", children: [_jsxs("span", { children: ["S ", formatImpactValue(proposal.sustainability_impact)] }), _jsxs("span", { children: ["E ", formatImpactValue(proposal.economic_impact)] }), _jsxs("span", { children: ["P ", formatImpactValue(proposal.political_impact)] })] })] }, proposal.id)))] })] })] }), _jsxs("main", { className: "app-stage", "aria-label": "Mailopolis strategic map", children: [_jsx("div", { className: "stage-toolbar", children: _jsxs("div", { children: [_jsx("h2", { className: "stage-title", children: "City Systems Map" }), _jsx("p", { className: "stage-subtitle", children: "Click a district to open its email thread or status dossier." })] }) }), _jsx("div", { className: "app-stage__canvas", children: _jsx(CityMap, {}) })] })] })] }), activeProposal && (_jsxs("div", { className: "proposal-modal", role: "dialog", "aria-modal": "true", "aria-labelledby": "proposal-modal-title", children: [_jsx("div", { className: "proposal-modal__backdrop", onClick: handleProposalClose }), _jsxs("div", { className: "proposal-modal__content", role: "document", children: [_jsxs("header", { className: "proposal-modal__header", children: [_jsx("h3", { id: "proposal-modal-title", children: activeProposal.title }), _jsx("button", { type: "button", className: "proposal-modal__close", onClick: handleProposalClose, children: "\u00D7" })] }), _jsx("p", { className: "proposal-modal__description", children: activeProposal.description }), _jsx("hr", { className: "proposal-modal__divider" }), _jsxs("div", { className: "proposal-modal__sections", children: [_jsxs("section", { className: "proposal-modal__section", children: [_jsx("h4", { children: "Overview" }), _jsxs("dl", { className: "proposal-modal__details", children: [_jsxs("div", { children: [_jsx("dt", { children: "Proposed by" }), _jsx("dd", { children: activeProposal.proposed_by || 'Unknown' })] }), _jsxs("div", { children: [_jsx("dt", { children: "Department" }), _jsx("dd", { children: formatDepartmentName(activeProposal.target_department) || 'Unknown' })] }), _jsxs("div", { children: [_jsx("dt", { children: "Bribe" }), _jsx("dd", { children: formatCurrency(activeProposal.bribe_amount) })] })] })] }), _jsxs("section", { className: "proposal-modal__section", children: [_jsx("h4", { children: "Impact Scores" }), _jsxs("ul", { className: "proposal-modal__impacts", children: [_jsxs("li", { children: [_jsx("span", { children: "Sustainability" }), _jsx("strong", { children: formatImpactValue(activeProposal.sustainability_impact) })] }), _jsxs("li", { children: [_jsx("span", { children: "Economic" }), _jsx("strong", { children: formatImpactValue(activeProposal.economic_impact) })] }), _jsxs("li", { children: [_jsx("span", { children: "Political" }), _jsx("strong", { children: formatImpactValue(activeProposal.political_impact) })] })] })] })] }), _jsxs("p", { className: "proposal-modal__timestamp", children: ["Created ", formatProposalTimestamp(activeProposal.created_at)] }), _jsx("footer", { className: "proposal-modal__footer", children: _jsx("button", { type: "button", className: "proposal-modal__select", onClick: () => handleProposalSelect(activeProposal), disabled: isLoading || !hasActiveGame, children: isLoading ? 'Working…' : hasActiveGame ? 'Select proposal' : 'Start game first' }) })] })] })), _jsx("button", { className: `logs-toggle ${logsOpen ? 'active' : ''}`, onClick: () => setLogsOpen(!logsOpen), style: {
                    position: 'fixed',
                    top: 20,
                    right: 20,
                    zIndex: 10000,
                    background: '#00ff88',
                    color: '#000',
                    border: 'none',
                    borderRadius: 8,
                    padding: '10px 15px',
                    cursor: 'pointer',
                    fontSize: 14,
                    fontWeight: 'bold',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
                }, children: logsOpen ? '📋 Hide Logs' : '📋 Show Logs' }), _jsx(LogsPanel, { isOpen: logsOpen, onClose: () => setLogsOpen(false) })] }));
}
