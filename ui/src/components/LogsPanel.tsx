import React, { useEffect, useState } from 'react';
import './LogsPanel.css';

export type LogsPanelProps = {
	isOpen: boolean;
	onClose: () => void;
};

export type LogEntry = {
	id: number;
	message: string;
	timestamp: string;
};

export const LogsPanel: React.FC<LogsPanelProps> = ({ isOpen, onClose }) => {
	const [logs, setLogs] = useState<LogEntry[]>([]);
	const [websocket, setWebsocket] = useState<WebSocket | null>(null);

	useEffect(() => {
		let reconnectTimer: number | undefined;

		const connectWebSocket = () => {
			try {
				const ws = new WebSocket('ws://localhost:8000/maylopolis/ws/logs');
				ws.onopen = () => {
					setWebsocket(ws);
				};
				ws.onmessage = (event: MessageEvent<string>) => {
					const logMessage = event.data;
					setLogs(prevLogs => {
						const newLogs: LogEntry[] = [
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
			} catch {
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

	return (
		<div className={`logs-panel ${isOpen ? 'open' : ''}`}>
			{/* Backdrop overlay */}
			{isOpen && <div className="logs-backdrop" onClick={onClose} />}

			{/* Header with close button */}
			<div className="logs-header">
				<div className="logs-title-section">
					<h3 className="logs-title">📋 System Logs</h3>
					<div className="logs-status">
						<span className="connection-status">
							{websocket ? '🟢 Connected' : '🔴 Disconnected'}
						</span>
						<span className="message-count">{`${logs.length} messages`}</span>
					</div>
				</div>
				<button className="logs-close-btn" onClick={onClose}>✕</button>
			</div>

			{/* Logs content */}
			<div className="logs-content">
				{logs.length === 0 ? (
					<div className="logs-empty">Waiting for logs...</div>
				) : (
					logs.map((log) => (
						<div key={log.id} className="log-entry">
							<div className="log-timestamp">{log.timestamp}</div>
							<div className="log-message">{log.message}</div>
						</div>
					))
				)}
			</div>
		</div>
	);
};
