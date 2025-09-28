import { useMemo, useState } from 'react';
import { CityMap } from '../city/CityMap';
import './BaseLayout.css';

const SIDEBAR_SECTIONS = [
	{
		id: 'inbox',
		label: 'Inbox',
		icon: '✉️',
		title: 'Priority Inbox',
		description:
			'Triaged conversations from departments and citizens. Focus on flagged threads to keep Mailopolis humming.',
		items: [
			{
				heading: 'Urgent Replies',
				body: 'Mayorʼs decree draft, Power Grid escalation, Karen vs HOA mediation.',
			},
			{
				heading: 'Waiting on You',
				body: 'Budget committee follow-up, Transit re-route approvals, Tourism newsletter copy.',
			},
		],
	},
	{
		id: 'situation',
		label: 'Situation',
		icon: '📈',
		title: 'City Situation Room',
		description:
			'Snapshot of power, finances, morale, and weather disruptions. Use as your pre-flight briefing each cycle.',
		items: [
			{
				heading: 'Stability Index',
				body: 'Power 73% (amber), Budget $2.3M (steady), Approval 64% (trending up).',
			},
			{
				heading: 'Watchlist',
				body: 'Email storm risk in Utilities, citizen rumblings in Midtown, stray storm cell approaching east ridge.',
			},
		],
	},
	{
		id: 'crisis',
		label: 'Crisis',
		icon: '⚠️',
		title: 'Crisis Response',
		description:
			'Timeline and countermeasures for active incidents. Each entry links to recommended email playbooks.',
		items: [
			{
				heading: 'Active Signals',
				body: 'Grid overload at Station 7, Transit strike warnings, Mayor press leak mitigation.',
			},
			{
				heading: 'Recommended Actions',
				body: 'Schedule emergency town hall, deploy calming statement to commuters, loop in Legal for leak briefing.',
			},
		],
	},
] as const;

export function BaseLayout() {
	const [activeSection, setActiveSection] =
		useState<(typeof SIDEBAR_SECTIONS)[number]['id']>('inbox');

	const section = useMemo(
		() =>
			SIDEBAR_SECTIONS.find((entry) => entry.id === activeSection) ??
			SIDEBAR_SECTIONS[0],
		[activeSection]
	);

	return (
		<div className="app-shell">
			<div className="app-frame">
				<header className="app-header">
					<div className="app-header__meta">
						<span className="app-badge">Mailopolis</span>
						<h1 className="app-title">City Email Control</h1>
					</div>
					<div className="app-header__status" aria-live="polite">
						<span className="status-dot" />
						<span>Network Link Stable</span>
					</div>
				</header>

				<div className="app-content">
					<aside
						className="app-sidebar"
						aria-label="Mailopolis briefing panels"
					>
						<nav className="sidebar-tabs" role="tablist">
							{SIDEBAR_SECTIONS.map((entry) => {
								const isActive = activeSection === entry.id;
								return (
									<button
										key={entry.id}
										type="button"
										className={`sidebar-tab${
											isActive ? ' is-active' : ''
										}`}
										role="tab"
										aria-selected={isActive}
										onClick={() =>
											setActiveSection(entry.id)
										}
									>
										<span
											aria-hidden="true"
											className="sidebar-tab__icon"
										>
											{entry.icon}
										</span>
										<span className="sidebar-tab__label">
											{entry.label}
										</span>
									</button>
								);
							})}
						</nav>

						<section
							className="sidebar-panel"
							role="tabpanel"
							aria-live="polite"
						>
							<header className="sidebar-panel__header">
								<h2 className="sidebar-panel__title">
									{section.title}
								</h2>
								<p className="sidebar-panel__description">
									{section.description}
								</p>
							</header>
							<ul className="sidebar-panel__list">
								{section.items.map((item) => (
									<li key={item.heading}>
										<strong>{item.heading}</strong>
										<span>{item.body}</span>
									</li>
								))}
							</ul>
						</section>
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
		</div>
	);
}
