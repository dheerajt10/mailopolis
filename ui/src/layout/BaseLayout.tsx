import { useState } from 'react';
import { CityMap } from '../city/CityMap';
import './BaseLayout.css';

const DEMO_PROPOSALS = [
	{
		id: '32bc27d0-1044-4864-b17e-6e448ee92d20',
		title: 'Emergency Renewable Energy Initiative',
		description:
			'Fast-track solar panel installation on all public buildings within 6 months.',
		proposedBy: 'ai_department_Energy',
		targetDepartment: 'Energy',
		sustainabilityImpact: 25,
		economicImpact: -20,
		politicalImpact: 15,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726149',
	},
	{
		id: '15ed8d62-4b88-4da8-a819-bcec854b3d55',
		title: 'Energy Efficiency Retrofits',
		description:
			'Low-cost energy efficiency improvements to reduce city utility costs.',
		proposedBy: 'ai_department_Energy',
		targetDepartment: 'Energy',
		sustainabilityImpact: 15,
		economicImpact: 10,
		politicalImpact: 5,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726166',
	},
	{
		id: '57c3f3f2-9fe4-4554-87bb-261e32bb34f3',
		title: 'Smart Grid Modernization',
		description:
			'Upgrade city electrical grid with smart monitoring and renewable integration.',
		proposedBy: 'ai_department_Energy',
		targetDepartment: 'Energy',
		sustainabilityImpact: 20,
		economicImpact: -15,
		politicalImpact: 10,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726173',
	},
	{
		id: 'b872045e-a817-4b94-bde6-b25b5264a6c2',
		title: 'Electric Bus Fleet Conversion',
		description: 'Replace all diesel buses with electric vehicles over 18 months.',
		proposedBy: 'ai_department_Transportation',
		targetDepartment: 'Transportation',
		sustainabilityImpact: 30,
		economicImpact: -25,
		politicalImpact: 20,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726181',
	},
	{
		id: 'd6e39f46-c3b7-4108-bea4-9eff94e94db0',
		title: 'Free Public Transit Month',
		description:
			'Provide free public transportation for one month to boost ridership.',
		proposedBy: 'ai_department_Transportation',
		targetDepartment: 'Transportation',
		sustainabilityImpact: 10,
		economicImpact: -15,
		politicalImpact: 25,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726187',
	},
	{
		id: '15f20170-98b5-4ede-883c-198affd4fd39',
		title: 'Bike Lane Expansion Project',
		description: 'Add 20 miles of protected bike lanes throughout the city.',
		proposedBy: 'ai_department_Transportation',
		targetDepartment: 'Transportation',
		sustainabilityImpact: 15,
		economicImpact: -10,
		politicalImpact: 5,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726193',
	},
	{
		id: 'e64371c2-3408-4631-b55b-a490ca857673',
		title: 'Affordable Housing Guarantee',
		description:
			'Mandate that 30% of all new developments include affordable units.',
		proposedBy: 'ai_department_Housing',
		targetDepartment: 'Housing',
		sustainabilityImpact: 5,
		economicImpact: -10,
		politicalImpact: 30,
		bribeAmount: 0,
		createdAt: '2025-09-28T08:31:50.726199',
	},
] as const;


export function BaseLayout() {
	const [activeProposalId, setActiveProposalId] = useState<string | null>(null);

	const handleProposalOpen = (id: string) => {
		setActiveProposalId(id);
	};

	const handleProposalClose = () => {
		setActiveProposalId(null);
	};

	const handleProposalSelect = (proposal: (typeof DEMO_PROPOSALS)[number]) => {
		console.log('Selected proposal', proposal.id);
	};

	const activeProposal =
		activeProposalId == null
			? null
			: DEMO_PROPOSALS.find((proposal) => proposal.id === activeProposalId) ?? null;

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
							<dd>$2.3M</dd>
						</div>
						<div className="city-stat city-stat--sustainability">
							<dt>Sustainability Score</dt>
							<dd>68</dd>
						</div>
						<div className="city-stat city-stat--infrastructure">
							<dt>Infrastructure Health</dt>
							<dd>74%</dd>
						</div>
						<div className="city-stat city-stat--happiness">
							<dt>Population Happiness</dt>
							<dd>64%</dd>
						</div>
						<div className="city-stat city-stat--corruption">
							<dt>Corruption Level</dt>
							<dd>Low</dd>
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
								Quick picks surfaced by city departments.
							</p>
						</header>
						<div className="proposal-list">
							{DEMO_PROPOSALS.map((proposal) => (
								<article key={proposal.id} className="proposal-card">
									<header className="proposal-card__top">
										<h3>{proposal.title}</h3>
										<button
											type="button"
											className="proposal-card__select"
											onClick={() => handleProposalSelect(proposal)}
										>
											Select
										</button>
									</header>
									<div className="proposal-card__summary">
										<span className="proposal-card__department">
											{proposal.targetDepartment}
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
								</article>
							))}
						</div>
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
											<dd>{activeProposal.proposedBy}</dd>
										</div>
										<div>
											<dt>Department</dt>
											<dd>{activeProposal.targetDepartment}</dd>
										</div>
										<div>
											<dt>Bribe</dt>
											<dd>${activeProposal.bribeAmount}</dd>
										</div>
									</dl>
								</section>
								<section className="proposal-modal__section">
									<h4>Impact Scores</h4>
									<ul className="proposal-modal__impacts">
										<li>
											<span>Sustainability</span>
											<strong>{activeProposal.sustainabilityImpact}</strong>
										</li>
										<li>
											<span>Economic</span>
											<strong>{activeProposal.economicImpact}</strong>
										</li>
										<li>
											<span>Political</span>
											<strong>{activeProposal.politicalImpact}</strong>
										</li>
									</ul>
								</section>
							</div>
							<p className="proposal-modal__timestamp">
								Created {new Date(activeProposal.createdAt).toLocaleString()}
							</p>
							<footer className="proposal-modal__footer">
								<button
									type="button"
									className="proposal-modal__select"
									onClick={() => handleProposalSelect(activeProposal)}
								>
									Select proposal
								</button>
							</footer>
						</div>
					</div>
			)}
		</div>
	);
}
