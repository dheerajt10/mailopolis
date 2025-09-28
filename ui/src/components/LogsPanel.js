import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import './LogsPanel.css';
export const LogsPanel = ({ isOpen, onClose }) => {
    const [logs, setLogs] = useState([]);
    const [websocket, setWebsocket] = useState(null);
    useEffect(() => {
        let reconnectTimer;
        const connectWebSocket = () => {
            try {
                const ws = new WebSocket('ws://localhost:8000/maylopolis/ws/logs');
                ws.onopen = () => {
                    setWebsocket(ws);
                };
                ws.onmessage = (event) => {
                    const logMessage = event.data;
                    setLogs(prevLogs => {
                        const newLogs = [
                            ...prevLogs,
                            {
                                id: Date.now() + Math.random(),
                                message: logMessage,
                                timestamp: new Date().toLocaleTimeString(),
                            },
                        ];
                        return newLogs.slice(-100);
                    });
                };
                ws.onclose = () => {
                    setWebsocket(null);
                    reconnectTimer = window.setTimeout(connectWebSocket, 3000);
                };
                ws.onerror = () => {
                    // swallow; connection retry will handle
                };
            }
            catch {
                // ignore connection errors; retry will handle
            }
        };
        connectWebSocket();
        return () => {
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
            if (websocket) {
                websocket.close();
            }
        };
    }, []);
    return (_jsxs("div", { className: `logs-panel ${isOpen ? 'open' : ''}`, children: [isOpen && _jsx("div", { className: "logs-backdrop", onClick: onClose }), _jsxs("div", { className: "logs-header", children: [_jsxs("div", { className: "logs-title-section", children: [_jsx("h3", { className: "logs-title", children: "\uD83D\uDCCB System Logs" }), _jsxs("div", { className: "logs-status", children: [_jsx("span", { className: "connection-status", children: websocket ? '🟢 Connected' : '🔴 Disconnected' }), _jsx("span", { className: "message-count", children: `${logs.length} messages` })] })] }), _jsx("button", { className: "logs-close-btn", onClick: onClose, children: "\u2715" })] }), _jsx("div", { className: "logs-content", children: logs.length === 0 ? (_jsx("div", { className: "logs-empty", children: "Waiting for logs..." })) : (logs.map((log) => (_jsxs("div", { className: "log-entry", children: [_jsx("div", { className: "log-timestamp", children: log.timestamp }), _jsx("div", { className: "log-message", children: log.message })] }, log.id)))) })] }));
};
