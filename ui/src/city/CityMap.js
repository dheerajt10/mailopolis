import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
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
export const CityMap = () => {
    const [activeBuilding, setActiveBuilding] = useState(null);
    const [buildingStatuses, setBuildingStatuses] = useState({
        'power@': 'warning',
        'mayor@': 'crisis',
        'emergency@': 'active',
        'police@': 'active',
        'transit@': 'warning',
        'karen@': 'crisis',
        'bob@': 'active',
    });
    const buildings = [
        {
            id: 'power-plant',
            type: 'power-plant',
            position: { x: 20, y: 50 },
            size: { width: 140, height: 120 },
            agent: 'power@',
            label: 'POWER PLANT',
            emoji: '⚡',
            status: buildingStatuses['power@'],
        },
        {
            id: 'city-hall',
            type: 'city-hall',
            position: { x: 340, y: 200 },
            size: { width: 120, height: 100 },
            agent: 'mayor@',
            label: 'CITY HALL',
            emoji: '🏛️',
            status: buildingStatuses['mayor@'],
        },
        {
            id: 'hospital',
            type: 'hospital',
            position: { x: 480, y: 80 },
            size: { width: 100, height: 80 },
            agent: 'emergency@',
            label: 'HOSPITAL',
            emoji: '🏥',
            status: buildingStatuses['emergency@'],
        },
        {
            id: 'police',
            type: 'police',
            position: { x: 620, y: 200 },
            size: { width: 90, height: 70 },
            agent: 'police@',
            label: 'POLICE',
            emoji: '👮',
            status: buildingStatuses['police@'],
        },
        {
            id: 'transit-hub',
            type: 'transit-hub',
            position: { x: 50, y: 350 },
            size: { width: 110, height: 90 },
            agent: 'transit@',
            label: 'TRANSIT HUB',
            emoji: '🚌',
            status: buildingStatuses['transit@'],
        },
        {
            id: 'shop1',
            type: 'commercial',
            position: { x: 420, y: 360 },
            size: { width: 80, height: 60 },
            agent: 'business@',
            label: 'SHOP',
            emoji: '🏢',
        },
        {
            id: 'shop2',
            type: 'commercial',
            position: { x: 520, y: 360 },
            size: { width: 80, height: 60 },
            agent: 'business@',
            label: 'MALL',
            emoji: '🏪',
        },
        {
            id: 'office1',
            type: 'commercial',
            position: { x: 280, y: 350 },
            size: { width: 80, height: 60 },
            agent: 'business@',
            label: 'OFFICE',
            emoji: '🏢',
        },
        {
            id: 'house1',
            type: 'house',
            position: { x: 220, y: 60 },
            size: { width: 60, height: 50 },
            agent: 'karen@',
            label: "KAREN'S HOUSE",
            emoji: '🏠',
            status: buildingStatuses['karen@'],
        },
        {
            id: 'house2',
            type: 'house',
            position: { x: 300, y: 60 },
            size: { width: 60, height: 50 },
            agent: 'bob@',
            label: "BOB'S HOUSE",
            emoji: '🏠',
            status: buildingStatuses['bob@'],
        },
        {
            id: 'house3',
            type: 'house',
            position: { x: 520, y: 200 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house4',
            type: 'house',
            position: { x: 680, y: 120 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house5',
            type: 'house',
            position: { x: 220, y: 460 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house6',
            type: 'house',
            position: { x: 300, y: 460 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house7',
            type: 'house',
            position: { x: 480, y: 480 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house8',
            type: 'house',
            position: { x: 620, y: 320 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'house9',
            type: 'house',
            position: { x: 700, y: 400 },
            size: { width: 60, height: 50 },
            agent: 'citizen@',
            label: 'RESIDENCE',
            emoji: '🏠',
        },
        {
            id: 'park1',
            type: 'park',
            position: { x: 160, y: 200 },
            size: { width: 80, height: 80 },
            agent: '',
            label: 'CENTRAL PARK',
            emoji: '🌳',
        },
        {
            id: 'park2',
            type: 'park',
            position: { x: 650, y: 480 },
            size: { width: 60, height: 60 },
            agent: '',
            label: 'EAST PARK',
            emoji: '🌲',
        },
    ];
    const handleBuildingClick = (agent) => {
        setActiveBuilding(agent);
        console.log(`Clicked on ${agent}`);
    };
    // Simulate random email activity
    useEffect(() => {
        const interval = setInterval(() => {
            const agentsWithStatus = [
                'power@',
                'mayor@',
                'emergency@',
                'police@',
                'transit@',
                'karen@',
                'bob@',
            ];
            const randomAgent = agentsWithStatus[Math.floor(Math.random() * agentsWithStatus.length)];
            if (Math.random() < 0.3) {
                // 30% chance to change status
                const statuses = [
                    'active',
                    'warning',
                    'crisis',
                ];
                const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
                setBuildingStatuses((prev) => ({
                    ...prev,
                    [randomAgent]: newStatus,
                }));
            }
        }, 3000);
        return () => clearInterval(interval);
    }, []);
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
                }, delay: 2 }), buildings.map((building) => (_jsx(Building, { ...building, isActive: activeBuilding === building.agent, onClick: handleBuildingClick }, building.id))), _jsxs("div", { className: "legend", children: [_jsx("h4", { style: { margin: '0 0 10px 0', color: '#00ff88' }, children: "LEGEND" }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#ffaa00',
                                    borderColor: '#ffcc00',
                                } }), _jsx("span", { children: "Power/Infrastructure" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#4488ff',
                                    borderColor: '#66aaff',
                                } }), _jsx("span", { children: "Government" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#ff4444',
                                    borderColor: '#ff6666',
                                } }), _jsx("span", { children: "Emergency Services" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#00ccff',
                                    borderColor: '#00ffff',
                                } }), _jsx("span", { children: "Transit" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#88ff88',
                                    borderColor: '#aaffaa',
                                } }), _jsx("span", { children: "Residential" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#ff88ff',
                                    borderColor: '#ffaaff',
                                } }), _jsx("span", { children: "Commercial" })] }), _jsxs("div", { className: "legend-item", children: [_jsx("div", { className: "legend-color", style: {
                                    background: '#22aa22',
                                    borderColor: '#44cc44',
                                } }), _jsx("span", { children: "Parks" })] })] })] }));
};
