import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './CityMap.css';
const Building = ({ id, type, position, size, agent, label, emoji, status, isActive, onClick, }) => {
    const handleClick = () => {
        onClick(agent);
    };
    return (_jsxs("div", { className: `building ${type} ${isActive ? 'active' : ''}`, "data-agent": agent, style: {
            left: position.x,
            top: position.y,
            width: size.width,
            height: size.height,
        }, onClick: handleClick, children: [emoji, _jsx("div", { className: "building-label", children: label }), status && _jsx("div", { className: `status-indicator status-${status}` })] }));
};
const ConnectionLine = ({ id, style, delay }) => (_jsx("div", { className: "connection-line", id: id, style: { ...style, animationDelay: `${delay}s` } }));
export const CityMap = ({ onOpenInbox }) => {
    const [activeBuilding, setActiveBuilding] = useState(null);
    const [buildings, setBuildings] = useState([]);
    const getBuildingConfig = (department, index, total) => {
        const departmentConfigs = {
            Energy: { type: 'power-plant', emoji: '⚡' },
            Mayor: { type: 'city-hall', emoji: '🏛️' },
            Transportation: { type: 'transit-hub', emoji: '🚌' },
            Housing: { type: 'commercial', emoji: '🏢' },
            Waste: { type: 'commercial', emoji: '♻️' },
            Water: { type: 'commercial', emoji: '💧' },
            EconomicDevelopment: { type: 'commercial', emoji: '💰' },
            Citizens: { type: 'house', emoji: '🏠' },
            BadActors: { type: 'commercial', emoji: '👹' },
        };
        const config = departmentConfigs[department] || { type: 'commercial', emoji: '🏢' };
        const cols = Math.ceil(Math.sqrt(total));
        const row = Math.floor(index / cols);
        const col = index % cols;
        const spacing = 180;
        const startX = 30;
        const startY = 30;
        const verticalVariation = (index * 23) % 60 - 30;
        const baseY = startY + row * spacing;
        const variedY = Math.max(30, Math.min(600, baseY + verticalVariation));
        const baseX = startX + col * spacing;
        const variedX = Math.max(30, Math.min(800, baseX));
        return {
            ...config,
            position: { x: variedX, y: variedY },
            size: {
                width: config.type === 'power-plant' ? 140 : config.type === 'city-hall' ? 120 : config.type === 'transit-hub' ? 110 : 80,
                height: config.type === 'power-plant' ? 120 : config.type === 'city-hall' ? 100 : config.type === 'transit-hub' ? 90 : 60,
            },
        };
    };
    useEffect(() => {
        const fetchPersonalities = async () => {
            try {
                const response = await apiService.getPersonalities();
                const entries = Object.entries(response.personalities);
                const generated = [];
                entries.forEach(([department, personality], index) => {
                    const config = getBuildingConfig(department, index, entries.length);
                    // Use the agent's human name; backend inboxes are keyed by this
                    const agentLookup = personality.name;
                    const { sustainability_focus, corruption_resistance } = personality.traits;
                    const status = sustainability_focus >= 80 && corruption_resistance >= 80
                        ? 'active'
                        : sustainability_focus >= 60 && corruption_resistance >= 60
                            ? 'warning'
                            : 'crisis';
                    generated.push({
                        id: `${department.toLowerCase()}-building`,
                        type: config.type,
                        position: config.position,
                        size: config.size,
                        agent: agentLookup,
                        label: personality.role.toUpperCase(),
                        emoji: config.emoji,
                        status,
                    });
                });
                // parks
                generated.push({
                    id: 'park1',
                    type: 'park',
                    position: { x: 600, y: 200 },
                    size: { width: 80, height: 80 },
                    agent: '',
                    label: 'CENTRAL PARK',
                    emoji: '🌳',
                }, {
                    id: 'park2',
                    type: 'park',
                    position: { x: 650, y: 480 },
                    size: { width: 60, height: 60 },
                    agent: '',
                    label: 'EAST PARK',
                    emoji: '🌲',
                });
                setBuildings(generated);
            }
            catch (e) {
                setBuildings([]);
            }
        };
        fetchPersonalities();
    }, []);
    const handleBuildingClick = async (agent, label) => {
        console.log('handleBuildingClick', agent, label);
        setActiveBuilding(agent);
        if (onOpenInbox && agent) {
            onOpenInbox(agent, label);
        }
        try {
            if (agent) {
                console.log('getAgentInbox', agent);
                await apiService.getAgentInbox(agent);
            }
        }
        catch (e) {
            console.error('Error fetching inbox:', e);
        }
    };
    return (_jsxs("div", { className: "city-map", children: [_jsx("div", { className: "road road-horizontal road-main-h" }), _jsx("div", { className: "road road-horizontal road-secondary-h1" }), _jsx("div", { className: "road road-horizontal road-secondary-h2" }), _jsx("div", { className: "road road-vertical road-main-v" }), _jsx("div", { className: "road road-vertical road-secondary-v1" }), _jsx("div", { className: "road road-vertical road-secondary-v2" }), _jsx(ConnectionLine, { id: "connection1", style: {
                    top: 240,
                    left: 340,
                    width: 140,
                    transform: 'rotate(15deg)',
                }, delay: 0 }), _jsx(ConnectionLine, { id: "connection2", style: {
                    top: 130,
                    left: 160,
                    width: 180,
                    transform: 'rotate(-10deg)',
                }, delay: 1 }), _jsx(ConnectionLine, { id: "connection3", style: {
                    top: 280,
                    left: 50,
                    width: 290,
                    transform: 'rotate(5deg)',
                }, delay: 2 }), buildings.map((building) => (_jsx(Building, { ...building, isActive: activeBuilding === building.agent, onClick: () => handleBuildingClick(building.agent, building.label) }, building.id)))] }));
};
