import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { CityMap } from '../city/CityMap';
import './BaseLayout.css';
const DEMO_PROPOSALS = [
    {
        id: '32bc27d0-1044-4864-b17e-6e448ee92d20',
        title: 'Emergency Renewable Energy Initiative',
        description: 'Fast-track solar panel installation on all public buildings within 6 months.',
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
        description: 'Low-cost energy efficiency improvements to reduce city utility costs.',
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
        description: 'Upgrade city electrical grid with smart monitoring and renewable integration.',
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
        description: 'Provide free public transportation for one month to boost ridership.',
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
        description: 'Mandate that 30% of all new developments include affordable units.',
        proposedBy: 'ai_department_Housing',
        targetDepartment: 'Housing',
        sustainabilityImpact: 5,
        economicImpact: -10,
        politicalImpact: 30,
        bribeAmount: 0,
        createdAt: '2025-09-28T08:31:50.726199',
    },
];
export function BaseLayout() {
    const [activeProposalId, setActiveProposalId] = useState(null);
    const handleProposalOpen = (id) => {
        setActiveProposalId(id);
    };
    const handleProposalClose = () => {
        setActiveProposalId(null);
    };
    const handleProposalSelect = (proposal) => {
        console.log('Selected proposal', proposal.id);
    };
    const activeProposal = activeProposalId == null
        ? null
        : DEMO_PROPOSALS.find((proposal) => proposal.id === activeProposalId) ?? null;
    return (_jsxs("div", { className: "app-shell", children: [_jsxs("div", { className: "app-frame", children: [_jsxs("header", { className: "app-header", "aria-label": "Mailopolis city overview", children: [_jsxs("div", { className: "navbar-brand", children: [_jsx("span", { className: "navbar-logo", "aria-hidden": "true", children: "\u2709\uFE0F" }), _jsxs("div", { className: "navbar-text", children: [_jsx("span", { className: "navbar-title", children: "Mailopolis" }), _jsx("span", { className: "navbar-subtitle", children: "City Control Center" })] })] }), _jsxs("dl", { className: "city-stats", children: [_jsxs("div", { className: "city-stat city-stat--budget", children: [_jsx("dt", { children: "Budget" }), _jsx("dd", { children: "$2.3M" })] }), _jsxs("div", { className: "city-stat city-stat--sustainability", children: [_jsx("dt", { children: "Sustainability Score" }), _jsx("dd", { children: "68" })] }), _jsxs("div", { className: "city-stat city-stat--infrastructure", children: [_jsx("dt", { children: "Infrastructure Health" }), _jsx("dd", { children: "74%" })] }), _jsxs("div", { className: "city-stat city-stat--happiness", children: [_jsx("dt", { children: "Population Happiness" }), _jsx("dd", { children: "64%" })] }), _jsxs("div", { className: "city-stat city-stat--corruption", children: [_jsx("dt", { children: "Corruption Level" }), _jsx("dd", { children: "Low" })] })] })] }), _jsxs("div", { className: "app-content", children: [_jsxs("aside", { className: "proposal-sidebar", "aria-label": "Strategic proposals", children: [_jsxs("header", { className: "proposal-sidebar__header", children: [_jsx("h2", { className: "proposal-sidebar__title", children: "Strategic Proposals" }), _jsx("p", { className: "proposal-sidebar__subtitle", children: "Quick picks surfaced by city departments." })] }), _jsx("div", { className: "proposal-list", children: DEMO_PROPOSALS.map((proposal) => (_jsxs("article", { className: "proposal-card", children: [_jsxs("header", { className: "proposal-card__top", children: [_jsx("h3", { children: proposal.title }), _jsx("button", { type: "button", className: "proposal-card__select", onClick: () => handleProposalSelect(proposal), children: "Select" })] }), _jsxs("div", { className: "proposal-card__summary", children: [_jsx("span", { className: "proposal-card__department", children: proposal.targetDepartment }), _jsxs("button", { type: "button", className: "proposal-card__info", "aria-label": `View details for ${proposal.title}`, onClick: () => handleProposalOpen(proposal.id), children: [_jsx("span", { className: "proposal-card__info-text", children: "More info" }), _jsx("span", { className: "proposal-card__info-icon", "aria-hidden": "true", children: "\u2192" })] })] })] }, proposal.id))) })] }), _jsxs("main", { className: "app-stage", "aria-label": "Mailopolis strategic map", children: [_jsx("div", { className: "stage-toolbar", children: _jsxs("div", { children: [_jsx("h2", { className: "stage-title", children: "City Systems Map" }), _jsx("p", { className: "stage-subtitle", children: "Click a district to open its email thread or status dossier." })] }) }), _jsx("div", { className: "app-stage__canvas", children: _jsx(CityMap, {}) })] })] })] }), activeProposal && (_jsxs("div", { className: "proposal-modal", role: "dialog", "aria-modal": "true", "aria-labelledby": "proposal-modal-title", children: [_jsx("div", { className: "proposal-modal__backdrop", onClick: handleProposalClose }), _jsxs("div", { className: "proposal-modal__content", role: "document", children: [_jsxs("header", { className: "proposal-modal__header", children: [_jsx("h3", { id: "proposal-modal-title", children: activeProposal.title }), _jsx("button", { type: "button", className: "proposal-modal__close", onClick: handleProposalClose, children: "\u00D7" })] }), _jsx("p", { className: "proposal-modal__description", children: activeProposal.description }), _jsx("hr", { className: "proposal-modal__divider" }), _jsxs("div", { className: "proposal-modal__sections", children: [_jsxs("section", { className: "proposal-modal__section", children: [_jsx("h4", { children: "Overview" }), _jsxs("dl", { className: "proposal-modal__details", children: [_jsxs("div", { children: [_jsx("dt", { children: "Proposed by" }), _jsx("dd", { children: activeProposal.proposedBy })] }), _jsxs("div", { children: [_jsx("dt", { children: "Department" }), _jsx("dd", { children: activeProposal.targetDepartment })] }), _jsxs("div", { children: [_jsx("dt", { children: "Bribe" }), _jsxs("dd", { children: ["$", activeProposal.bribeAmount] })] })] })] }), _jsxs("section", { className: "proposal-modal__section", children: [_jsx("h4", { children: "Impact Scores" }), _jsxs("ul", { className: "proposal-modal__impacts", children: [_jsxs("li", { children: [_jsx("span", { children: "Sustainability" }), _jsx("strong", { children: activeProposal.sustainabilityImpact })] }), _jsxs("li", { children: [_jsx("span", { children: "Economic" }), _jsx("strong", { children: activeProposal.economicImpact })] }), _jsxs("li", { children: [_jsx("span", { children: "Political" }), _jsx("strong", { children: activeProposal.politicalImpact })] })] })] })] }), _jsxs("p", { className: "proposal-modal__timestamp", children: ["Created ", new Date(activeProposal.createdAt).toLocaleString()] }), _jsx("footer", { className: "proposal-modal__footer", children: _jsx("button", { type: "button", className: "proposal-modal__select", onClick: () => handleProposalSelect(activeProposal), children: "Select proposal" }) })] })] }))] }));
}
