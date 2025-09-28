import { useMemo, useState } from 'react';
import { CityMap } from '../city/CityMap';
import { useGame } from '../contexts/GameContext';
import type { PolicyProposal } from '../services/api';
import './BaseLayout.css';

const formatImpactValue = (value: number | undefined) => {
  if (value == null) return '0';
  return value >= 0 ? `+${value}` : `${value}`;
};
const formatDepartmentName = (department: string | undefined) =>
  (department ?? '')
    .replace(/_/g, ' ')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/\s+/g, ' ')
    .trim();

const formatProposalTimestamp = (timestamp: string) => {
  if (!timestamp) {
    return 'just now';
  }
  try {
    return new Date(timestamp).toLocaleString(undefined, {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  } catch (error) {
    return timestamp;
  }
};

const formatCurrency = (value: number | undefined) => `$${(value ?? 0).toLocaleString()}`;

export function BaseLayout() {
	const [activeProposalId, setActiveProposalId] = useState<string | null>(null);
	const {
		gameState,
		suggestions,
		isLoading,
		error,
		isGameActive,
		startGame,
		stopGame,
		refreshGameState,
		refreshSuggestions,
		playTurn,
	} = useGame();

	const proposals = useMemo(() => suggestions ?? [], [suggestions]);
	const activeProposal =
		activeProposalId == null
			? null
			: proposals.find((proposal) => proposal.id === activeProposalId) ?? null;
	const activeEvents = gameState?.active_events ?? [];
	const hasActiveGame = isGameActive;

	const handleProposalOpen = (id: string) => {
		setActiveProposalId(id);
	};

	const handleProposalClose = () => {
		setActiveProposalId(null);
	};

	const handleProposalSelect = async (proposal: PolicyProposal) => {
		await playTurn({
			title: proposal.title,
			description: proposal.description,
			target_department: proposal.target_department,
			sustainability_impact: proposal.sustainability_impact,
			economic_impact: proposal.economic_impact,
			political_impact: proposal.political_impact,
		});
		setActiveProposalId(null);
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

	return (
		<div className="app-shell">
			<div className="app-frame">
				<header className="app-header" aria-label="Mailopolis city overview">
					<div className="navbar-brand">
						<span className="navbar-logo" aria-hidden="true">
							✉️
						</span>
						<div className="navbar-text">
							<span className="navbar-title">Mailopolis</span>
							<span className="navbar-subtitle">City Control Center</span>
						</div>
					</div>
					<dl className="city-stats">
						<div className="city-stat city-stat--budget">
							<dt>Budget</dt>
							<dd>{gameState ? `$${(gameState.city_stats.budget / 1000000).toFixed(1)}M` : '--'}</dd>
						</div>
						<div className="city-stat city-stat--sustainability">
							<dt>Sustainability Score</dt>
							<dd>{gameState?.city_stats.sustainability_score ?? '--'}</dd>
						</div>
						<div className="city-stat city-stat--economy">
							<dt>Economic Growth</dt>
							<dd>{gameState ? `${gameState.city_stats.economic_growth}%` : '--'}</dd>
						</div>
						<div className="city-stat city-stat--approval">
							<dt>Public Approval</dt>
							<dd>{gameState ? `${gameState.city_stats.public_approval}%` : '--'}</dd>
						</div>
						<div className="city-stat city-stat--infrastructure">
							<dt>Infrastructure Health</dt>
							<dd>{gameState ? `${gameState.city_stats.infrastructure_health}%` : '--'}</dd>
						</div>
						<div className="city-stat city-stat--happiness">
							<dt>Population Happiness</dt>
							<dd>{gameState ? `${gameState.city_stats.population_happiness}%` : '--'}</dd>
						</div>
						<div className="city-stat city-stat--corruption">
							<dt>Corruption Level</dt>
							<dd>{gameState ? `${gameState.city_stats.corruption_level}%` : '--'}</dd>
						</div>
					</dl>
				</header>

				<div className="app-content">
					<aside
						className="proposal-sidebar"
						aria-label="Strategic proposals"
					>
						<header className="proposal-sidebar__header">
							<h2 className="proposal-sidebar__title">Strategic Proposals</h2>
							<p className="proposal-sidebar__subtitle">
								Latest moves surfaced by the Maylopolis cabinet.
							</p>
						</header>
						<div className="proposal-list">
							{proposals.length === 0 && (
								<div className="proposal-list__empty">
									{hasActiveGame
										? 'No proposals available yet. Refresh suggestions to pull new ideas from departments.'
										: 'Start the simulation to receive live proposals from departments.'}
								</div>
							)}
							{proposals.map((proposal) => (
								<article key={proposal.id} className="proposal-card">
									<header className="proposal-card__top">
										<h3>{proposal.title}</h3>
										<button
											type="button"
											className="proposal-card__select"
											onClick={() => handleProposalSelect(proposal)}
											disabled={isLoading || !hasActiveGame}
										>
											{isLoading ? 'Working…' : hasActiveGame ? 'Select' : 'Start game first'}
										</button>
									</header>
									<div className="proposal-card__summary">
										<span className="proposal-card__department">
											{formatDepartmentName(proposal.target_department) || 'Unknown'}
										</span>
										<button
											type="button"
											className="proposal-card__info"
											aria-label={`View details for ${proposal.title}`}
											onClick={() => handleProposalOpen(proposal.id)}
										>
											<span className="proposal-card__info-text">More info</span>
											<span className="proposal-card__info-icon" aria-hidden="true">
												→
											</span>
										</button>
									</div>
									<div className="proposal-card__impacts">
										<span>S {formatImpactValue(proposal.sustainability_impact)}</span>
										<span>E {formatImpactValue(proposal.economic_impact)}</span>
										<span>P {formatImpactValue(proposal.political_impact)}</span>
									</div>
								</article>
							))}
						</div>
						<div className="game-controls">
							<div className="game-controls__buttons">
								{!hasActiveGame ? (
									<button
										className="start-game-btn"
										onClick={handleStartGame}
										disabled={isLoading}
									>
										{isLoading ? 'Starting…' : 'Start Simulation'}
									</button>
								) : (
									<>
										<button
											className="refresh-btn"
											onClick={refreshGameState}
											disabled={isLoading}
										>
											{isLoading ? 'Refreshing…' : 'Refresh State'}
										</button>
										<button
											className="refresh-btn"
											onClick={handleRefreshSuggestions}
											disabled={isLoading}
										>
											{isLoading ? 'Updating…' : 'Refresh Suggestions'}
										</button>
										<button
											className="stop-game-btn"
											onClick={handleStopGame}
											disabled={isLoading}
										>
											Stop Simulation
										</button>
									</>
								)}
							</div>
							<div
								className={`game-controls__meta${isLoading ? ' game-controls__meta--loading' : ''}`}
							>
								<span className="game-controls__status-dot" aria-hidden="true" />
								<span>
										{hasActiveGame
											? `Turn ${gameState?.turn ?? 0}`
											: 'Simulation idle'}
								</span>
								<span>Active events: {activeEvents.length}</span>
								{gameState?.is_game_over && (
									<span className="game-controls__badge">Game over</span>
								)}
							</div>
						</div>
						{error && (
							<div className="game-error" role="alert">
								{error}
							</div>
						)}
					</aside>

					<main
						className="app-stage"
						aria-label="Mailopolis strategic map"
					>
						<div className="stage-toolbar">
							<div>
								<h2 className="stage-title">
									City Systems Map
								</h2>
								<p className="stage-subtitle">
									Click a district to open its email thread or
									status dossier.
								</p>
							</div>
							{/* <div className="stage-toolbar__chips">
                <span className="chip chip--ambient">Ambient sync OK</span>
                <span className="chip chip--alert">2 crises flagged</span>
              </div> */}
						</div>
						<div className="app-stage__canvas">
							<CityMap />
						</div>
					</main>
				</div>
			</div>

			{activeProposal && (
				<div
					className="proposal-modal"
					role="dialog"
					aria-modal="true"
					aria-labelledby="proposal-modal-title"
				>
					<div className="proposal-modal__backdrop" onClick={handleProposalClose} />
						<div className="proposal-modal__content" role="document">
							<header className="proposal-modal__header">
								<h3 id="proposal-modal-title">{activeProposal.title}</h3>
								<button
									type="button"
									className="proposal-modal__close"
									onClick={handleProposalClose}
								>
									×
								</button>
							</header>
							<p className="proposal-modal__description">
								{activeProposal.description}
							</p>
							<hr className="proposal-modal__divider" />
							<div className="proposal-modal__sections">
								<section className="proposal-modal__section">
									<h4>Overview</h4>
									<dl className="proposal-modal__details">
										<div>
											<dt>Proposed by</dt>
										<dd>{activeProposal.proposed_by || 'Unknown'}</dd>
									</div>
									<div>
										<dt>Department</dt>
										<dd>{formatDepartmentName(activeProposal.target_department) || 'Unknown'}</dd>
									</div>
									<div>
										<dt>Bribe</dt>
										<dd>{formatCurrency(activeProposal.bribe_amount)}</dd>
									</div>
								</dl>
							</section>
							<section className="proposal-modal__section">
								<h4>Impact Scores</h4>
								<ul className="proposal-modal__impacts">
									<li>
										<span>Sustainability</span>
										<strong>{formatImpactValue(activeProposal.sustainability_impact)}</strong>
									</li>
									<li>
										<span>Economic</span>
										<strong>{formatImpactValue(activeProposal.economic_impact)}</strong>
									</li>
									<li>
										<span>Political</span>
										<strong>{formatImpactValue(activeProposal.political_impact)}</strong>
									</li>
								</ul>
							</section>
							</div>
								<p className="proposal-modal__timestamp">
									Created {formatProposalTimestamp(activeProposal.created_at)}
								</p>
							<footer className="proposal-modal__footer">
								<button
									type="button"
									className="proposal-modal__select"
									onClick={() => handleProposalSelect(activeProposal)}
									disabled={isLoading || !hasActiveGame}
								>
									{isLoading ? 'Working…' : hasActiveGame ? 'Select proposal' : 'Start game first'}
								</button>
							</footer>
						</div>
					</div>
			)}
		</div>
	);
}
