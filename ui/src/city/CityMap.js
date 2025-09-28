import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import './CityMap.css';
import { apiService } from '../services/api';

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

// Dynamic building configuration based on department type
const getBuildingConfig = (department, index, total) => {
    // Map department names to building types and emojis
    const departmentConfigs = {
        'Energy': { type: 'power-plant', emoji: '⚡' },
        'Mayor': { type: 'city-hall', emoji: '🏛️' },
        'Transportation': { type: 'transit-hub', emoji: '🚌' },
        'Housing': { type: 'commercial', emoji: '🏢' },
        'Waste': { type: 'commercial', emoji: '♻️' },
        'Water': { type: 'commercial', emoji: '💧' },
        'EconomicDevelopment': { type: 'commercial', emoji: '💰' },
        'Citizens': { type: 'house', emoji: '🏠' },
        'BadActors': { type: 'commercial', emoji: '👹' }
    };
    
    const config = departmentConfigs[department] || { type: 'commercial', emoji: '🏢' };
    
    // Dynamic positioning - arrange buildings in a grid-like pattern with more spacing
    const cols = Math.ceil(Math.sqrt(total));
    const rows = Math.ceil(total / cols);
    const col = index % cols;
    const row = Math.floor(index / cols);
    
    // Calculate position with increased spacing to prevent collision
    const spacing = 180; // Increased from 120 to 180
    const startX = 30;
    const startY = 30;
    
    // Add some vertical variation to make it look more natural
    const verticalVariation = (index * 23) % 60 - 30; // -30 to +30 pixel variation
    const baseY = startY + (row * spacing);
    const variedY = Math.max(30, Math.min(600, baseY + verticalVariation)); // Keep within bounds (30-600px)
    
    // Ensure X position stays within bounds too
    const baseX = startX + (col * spacing);
    const variedX = Math.max(30, Math.min(800, baseX)); // Keep within bounds (30-800px)
    
    return {
        ...config,
        position: { 
            x: variedX, 
            y: variedY 
        },
        size: { 
            width: config.type === 'power-plant' ? 140 : 
                   config.type === 'city-hall' ? 120 : 
                   config.type === 'transit-hub' ? 110 : 80, 
            height: config.type === 'power-plant' ? 120 : 
                    config.type === 'city-hall' ? 100 : 
                    config.type === 'transit-hub' ? 90 : 60 
        }
    };
};

export const CityMap = () => {
    const [activeBuilding, setActiveBuilding] = useState(null);
    const [buildingStatuses, setBuildingStatuses] = useState({});
    const [personalities, setPersonalities] = useState(null);
    const [buildings, setBuildings] = useState([]);

    // Function to generate building status based on personality traits
    const generateBuildingStatus = (personality) => {
        const { sustainability_focus, corruption_resistance, risk_tolerance } = personality.traits;
        
        // Determine status based on sustainability focus and corruption resistance
        if (sustainability_focus >= 80 && corruption_resistance >= 80) {
            return 'active'; // Green - highly sustainable and resistant to corruption
        } else if (sustainability_focus >= 60 && corruption_resistance >= 60) {
            return 'warning'; // Yellow - moderate performance
        } else {
            return 'crisis'; // Red - poor sustainability or high corruption risk
        }
    };

    // Fetch personalities and generate buildings
    useEffect(() => {
        const fetchPersonalities = async () => {
            try {
                const response = await apiService.getPersonalities();
                setPersonalities(response.personalities);
                
                // Generate buildings from personalities
                const generatedBuildings = [];
                const newBuildingStatuses = {};
                
                Object.entries(response.personalities).forEach(([department, personality], index) => {
                    const config = getBuildingConfig(department, index, Object.keys(response.personalities).length);
                    const agentEmail = `${department.toLowerCase()}@`;
                    const status = generateBuildingStatus(personality);
                    
                    generatedBuildings.push({
                        id: `${department.toLowerCase()}-building`,
                        type: config.type,
                        position: config.position,
                        size: config.size,
                        agent: agentEmail,
                        label: personality.role.toUpperCase(),
                        emoji: config.emoji,
                        status: status,
                    });
                    
                    newBuildingStatuses[agentEmail] = status;
                });
                
                // Add some static park buildings for visual appeal
                generatedBuildings.push(
                    {
                        id: 'park1',
                        type: 'park',
                        position: { x: 600, y: 200 },
                        size: { width: 80, height: 80 },
                        agent: '',
                        label: 'CENTRAL PARK',
                        emoji: '🌳',
                        status: null,
                    },
                    {
                        id: 'park2',
                        type: 'park',
                        position: { x: 650, y: 480 },
                        size: { width: 60, height: 60 },
                        agent: '',
                        label: 'EAST PARK',
                        emoji: '🌲',
                        status: null,
                    }
                );
                
                setBuildings(generatedBuildings);
                setBuildingStatuses(newBuildingStatuses);
            } catch (error) {
                console.error('Failed to fetch personalities:', error);
                // Fallback to empty buildings array
                setBuildings([]);
            }
        };

        fetchPersonalities();
    }, []);

    const handleBuildingClick = (agent) => {
        setActiveBuilding(agent);
        console.log(`Clicked on ${agent}`);
    };

    // Simulate random email activity - update building statuses based on personality changes
    useEffect(() => {
        if (!personalities) return;
        
        const interval = setInterval(() => {
            if (Math.random() < 0.3) {
                // 30% chance to update status based on current personality traits
                const newBuildingStatuses = {};
                Object.entries(personalities).forEach(([department, personality]) => {
                    const agentEmail = `${department.toLowerCase()}@`;
                    const status = generateBuildingStatus(personality);
                    newBuildingStatuses[agentEmail] = status;
                });
                setBuildingStatuses(newBuildingStatuses);
                
                // Update building objects with new statuses
                setBuildings(prevBuildings => 
                    prevBuildings.map(building => ({
                        ...building,
                        status: newBuildingStatuses[building.agent] || building.status
                    }))
                );
            }
        }, 5000);
        return () => clearInterval(interval);
    }, [personalities]);

    return (_jsxs("div", { className: "city-map", children: [
        _jsx("div", { className: "road road-horizontal road-main-h" }), 
        _jsx("div", { className: "road road-horizontal road-secondary-h1" }), 
        _jsx("div", { className: "road road-horizontal road-secondary-h2" }), 
        _jsx("div", { className: "road road-vertical road-main-v" }), 
        _jsx("div", { className: "road road-vertical road-secondary-v1" }), 
        _jsx("div", { className: "road road-vertical road-secondary-v2" }), 
        _jsx(ConnectionLine, { id: "connection1", style: {
            top: 240,
            left: 340,
            width: 140,
            transform: 'rotate(15deg)',
        }, delay: 0 }), 
        _jsx(ConnectionLine, { id: "connection2", style: {
            top: 130,
            left: 160,
            width: 180,
            transform: 'rotate(-10deg)',
        }, delay: 1 }), 
        _jsx(ConnectionLine, { id: "connection3", style: {
            top: 280,
            left: 50,
            width: 290,
            transform: 'rotate(5deg)',
        }, delay: 2 }), 
        buildings.map((building) => (_jsx(Building, { ...building, isActive: activeBuilding === building.agent, onClick: handleBuildingClick }, building.id)))
    ] }));
};