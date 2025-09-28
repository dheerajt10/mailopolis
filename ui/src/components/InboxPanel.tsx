import React, { useEffect, useMemo, useState } from 'react';
import './InboxPanel.css';
import { apiService, AgentInboxResponse, AgentMessage } from '../services/api';

export type InboxPanelProps = {
    isOpen: boolean;
    onClose: () => void;
    agentName?: string; // Full agent name to fetch inbox for
    headerLabel?: string; // Optional header, e.g., department or display label
    initialInbox?: AgentInboxResponse | null; // Optional preloaded data
};

const extractEmails = (values: string[] | undefined): string[] => {
    if (!values) return [];
    return values
        .map((v) => {
            const match = v.match(/<([^>]+)>/);
            return match ? match[1] : v;
        })
        .map((v) => v.trim().toLowerCase());
};

const extractFromEmail = (fromValue: string | undefined): string | undefined => {
    if (!fromValue) return undefined;
    const match = fromValue.match(/<([^>]+)>/);
    return (match ? match[1] : fromValue).trim().toLowerCase();
};

const MessageCard: React.FC<{ message: AgentMessage; myEmail?: string }> = ({ message, myEmail }) => {
    const receivedAt = useMemo(() => {
        try {
            return new Date(message.received_at).toLocaleString();
        } catch {
            return message.received_at;
        }
    }, [message.received_at]);

    const toList = extractEmails(message.to);
    const ccList = extractEmails(message.cc);
    const bccList = extractEmails(message.bcc);
    const fromEmail = extractFromEmail(message.from);
    const direction: 'incoming' | 'outgoing' | 'other' = myEmail
        ? (fromEmail === myEmail
            ? 'outgoing'
            : (toList.includes(myEmail) || ccList.includes(myEmail) || bccList.includes(myEmail))
                ? 'incoming'
                : 'other')
        : 'other';

    // Use an iframe with srcDoc and a strict sandbox to safely render HTML
    return (
        <article className={`inbox-message${direction !== 'other' ? ` inbox-message--${direction}` : ''}`}>
            <header className="inbox-message__header">
                <div className="inbox-message__subject">{message.subject || '(no subject)'}</div>
                <div className="inbox-message__meta">
                    <span className="inbox-message__from">{message.from}</span>
                    <span className="inbox-message__time">{receivedAt}</span>
                </div>
                <div className="inbox-message__recipients">
                    <div className="inbox-message__line"><strong>To:</strong> {toList.join(', ') || '—'}</div>
                    {ccList.length > 0 && (
                        <div className="inbox-message__line"><strong>CC:</strong> {ccList.join(', ')}</div>
                    )}
                </div>
            </header>
            {message.html_content ? (
                <iframe
                    className="inbox-message__iframe"
                    sandbox="allow-popups"
                    srcDoc={message.html_content}
                    title={message.message_id}
                />
            ) : (
                <pre className="inbox-message__text">{message.text_content || ''}</pre>
            )}
        </article>
    );
};

export const InboxPanel: React.FC<InboxPanelProps> = ({ isOpen, onClose, agentName, headerLabel, initialInbox }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [inbox, setInbox] = useState<AgentInboxResponse | null>(null);

    // Adopt preloaded inbox if provided
    useEffect(() => {
        if (initialInbox) {
            setInbox(initialInbox);
        }
    }, [initialInbox]);

    useEffect(() => {
        let cancelled = false;
        const fetchInbox = async () => {
            if (!isOpen) { setInbox(null); setError(null); return; }
            if (!agentName) { setInbox(null); setError(null); return; }
            setLoading(true);
            setError(null);
            try {
                const data = await apiService.getAgentInbox(agentName);
                if (!cancelled) { setInbox(data); }
            } catch (e: any) {
                if (!cancelled) { setError(null); /* keep soft-empty */ }
            } finally {
                if (!cancelled) setLoading(false);
            }
        };
        fetchInbox();
        return () => { cancelled = true; };
    }, [isOpen, agentName]);

    // Poll while panel is open to keep messages fresh
    useEffect(() => {
        if (!isOpen || !agentName) return;
        let cancelled = false;
        const interval = window.setInterval(async () => {
            try {
                const data = await apiService.getAgentInbox(agentName);
                if (!cancelled) {
                    setInbox(prev => {
                        if (!prev || prev.message_count !== data.message_count) return data;
                        return prev;
                    });
                }
            } catch { /* ignore polling errors */ }
        }, 15000);
        return () => { cancelled = true; clearInterval(interval); };
    }, [isOpen, agentName]);

    const myEmail = inbox?.email_address?.toLowerCase();
    const receivedMessages: AgentMessage[] = [];
    const sentMessages: AgentMessage[] = [];
    if (inbox?.recent_messages && myEmail) {
        for (const msg of inbox.recent_messages) {
            const toList = extractEmails(msg.to);
            const ccList = extractEmails(msg.cc);
            const bccList = extractEmails(msg.bcc);
            const fromEmail = extractFromEmail(msg.from);
            if (fromEmail === myEmail) {
                sentMessages.push(msg);
            } else if (toList.includes(myEmail) || ccList.includes(myEmail) || bccList.includes(myEmail)) {
                receivedMessages.push(msg);
            }
        }
    }

    return (
        <div className={`inbox-panel ${isOpen ? 'open' : ''}`}>
            {isOpen && <div className="inbox-backdrop" onClick={onClose} />}
            <div className="inbox-header">
                <div className="inbox-title-wrap">
                    <h3 className="inbox-title">{headerLabel || agentName || 'Agent Inbox'}</h3>
                    {inbox && <div className="inbox-subtitle">{inbox.display_name} · {inbox.email_address}</div>}
                </div>
                <button className="inbox-close-btn" onClick={onClose}>✕</button>
            </div>
            <div className="inbox-content">
                {loading && <div className="inbox-loading">Loading inbox…</div>}
                {/* When there's no data yet, show empty state, not an error */}
                {!loading && !inbox && (
                    <div className="inbox-empty">Select a department to view its inbox.</div>
                )}
                {!loading && inbox && inbox.recent_messages.length === 0 && (
                    <div className="inbox-empty">No messages yet.</div>
                )}
                {!loading && inbox && inbox.recent_messages.length > 0 && (
                    <div className="inbox-messages">
                        {receivedMessages.length > 0 && (
                            <section>
                                <h4 style={{ color: '#9adfbf', margin: '6px 0 8px 2px' }}>Incoming</h4>
                                {receivedMessages.map((msg) => (
                                    <MessageCard key={msg.message_id} message={msg} myEmail={myEmail} />
                                ))}
                            </section>
                        )}
                        {sentMessages.length > 0 && (
                            <section>
                                <h4 style={{ color: '#9adfbf', margin: '12px 0 8px 2px' }}>Outgoing</h4>
                                {sentMessages.map((msg) => (
                                    <MessageCard key={msg.message_id} message={msg} myEmail={myEmail} />
                                ))}
                            </section>
                        )}
                        {receivedMessages.length === 0 && sentMessages.length === 0 && (
                            <div className="inbox-empty">No messages yet.</div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default InboxPanel;


