import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from 'react';
import './InboxPanel.css';
import { apiService } from '../services/api';
const extractEmails = (values) => {
    if (!values)
        return [];
    return values
        .map((v) => {
        const match = v.match(/<([^>]+)>/);
        return match ? match[1] : v;
    })
        .map((v) => v.trim().toLowerCase());
};
const extractFromEmail = (fromValue) => {
    if (!fromValue)
        return undefined;
    const match = fromValue.match(/<([^>]+)>/);
    return (match ? match[1] : fromValue).trim().toLowerCase();
};
const MessageCard = ({ message, myEmail }) => {
    const receivedAt = useMemo(() => {
        try {
            return new Date(message.received_at).toLocaleString();
        }
        catch {
            return message.received_at;
        }
    }, [message.received_at]);
    const toList = extractEmails(message.to);
    const ccList = extractEmails(message.cc);
    const bccList = extractEmails(message.bcc);
    const fromEmail = extractFromEmail(message.from);
    const direction = myEmail
        ? (fromEmail === myEmail
            ? 'outgoing'
            : (toList.includes(myEmail) || ccList.includes(myEmail) || bccList.includes(myEmail))
                ? 'incoming'
                : 'other')
        : 'other';
    // Use an iframe with srcDoc and a strict sandbox to safely render HTML
    return (_jsxs("article", { className: `inbox-message${direction !== 'other' ? ` inbox-message--${direction}` : ''}`, children: [_jsxs("header", { className: "inbox-message__header", children: [_jsx("div", { className: "inbox-message__subject", children: message.subject || '(no subject)' }), _jsxs("div", { className: "inbox-message__meta", children: [_jsx("span", { className: "inbox-message__from", children: message.from }), _jsx("span", { className: "inbox-message__time", children: receivedAt })] }), _jsxs("div", { className: "inbox-message__recipients", children: [_jsxs("div", { className: "inbox-message__line", children: [_jsx("strong", { children: "To:" }), " ", toList.join(', ') || '—'] }), ccList.length > 0 && (_jsxs("div", { className: "inbox-message__line", children: [_jsx("strong", { children: "CC:" }), " ", ccList.join(', ')] }))] })] }), message.html_content ? (_jsx("iframe", { className: "inbox-message__iframe", sandbox: "allow-popups", srcDoc: message.html_content, title: message.message_id })) : (_jsx("pre", { className: "inbox-message__text", children: message.text_content || '' }))] }));
};
export const InboxPanel = ({ isOpen, onClose, agentName, headerLabel, initialInbox }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [inbox, setInbox] = useState(null);
    // Adopt preloaded inbox if provided
    useEffect(() => {
        if (initialInbox) {
            setInbox(initialInbox);
        }
    }, [initialInbox]);
    useEffect(() => {
        let cancelled = false;
        const fetchInbox = async () => {
            if (!isOpen) {
                setInbox(null);
                setError(null);
                return;
            }
            if (!agentName) {
                setInbox(null);
                setError(null);
                return;
            }
            setLoading(true);
            setError(null);
            try {
                const data = await apiService.getAgentInbox(agentName);
                if (!cancelled) {
                    setInbox(data);
                }
            }
            catch (e) {
                if (!cancelled) {
                    setError(null); /* keep soft-empty */
                }
            }
            finally {
                if (!cancelled)
                    setLoading(false);
            }
        };
        fetchInbox();
        return () => { cancelled = true; };
    }, [isOpen, agentName]);
    // Poll while panel is open to keep messages fresh
    useEffect(() => {
        if (!isOpen || !agentName)
            return;
        let cancelled = false;
        const interval = window.setInterval(async () => {
            try {
                const data = await apiService.getAgentInbox(agentName);
                console.log('getAgentInbox', agentName);
                if (!cancelled) {
                    setInbox(prev => {
                        if (!prev || prev.message_count !== data.message_count)
                            return data;
                        return prev;
                    });
                }
            }
            catch { /* ignore polling errors */ }
        }, 15000);
        return () => { cancelled = true; clearInterval(interval); };
    }, [isOpen, agentName]);
    const myEmail = inbox?.email_address?.toLowerCase();
    const receivedMessages = [];
    const sentMessages = [];
    if (inbox?.recent_messages && myEmail) {
        for (const msg of inbox.recent_messages) {
            const toList = extractEmails(msg.to);
            const ccList = extractEmails(msg.cc);
            const bccList = extractEmails(msg.bcc);
            const fromEmail = extractFromEmail(msg.from);
            if (fromEmail === myEmail) {
                sentMessages.push(msg);
            }
            else if (toList.includes(myEmail) || ccList.includes(myEmail) || bccList.includes(myEmail)) {
                receivedMessages.push(msg);
            }
        }
    }
    return (_jsxs("div", { className: `inbox-panel ${isOpen ? 'open' : ''}`, children: [isOpen && _jsx("div", { className: "inbox-backdrop", onClick: onClose }), _jsxs("div", { className: "inbox-header", children: [_jsxs("div", { className: "inbox-title-wrap", children: [_jsx("h3", { className: "inbox-title", children: headerLabel || agentName || 'Agent Inbox' }), inbox && _jsxs("div", { className: "inbox-subtitle", children: [inbox.display_name, " \u00B7 ", inbox.email_address] })] }), _jsx("button", { className: "inbox-close-btn", onClick: onClose, children: "\u2715" })] }), _jsxs("div", { className: "inbox-content", children: [loading && _jsx("div", { className: "inbox-loading", children: "Loading inbox\u2026" }), !loading && !inbox && (_jsx("div", { className: "inbox-empty", children: "Select a department to view its inbox." })), !loading && inbox && inbox.recent_messages.length === 0 && (_jsx("div", { className: "inbox-empty", children: "No messages yet." })), !loading && inbox && inbox.recent_messages.length > 0 && (_jsxs("div", { className: "inbox-messages", children: [receivedMessages.length > 0 && (_jsxs("section", { children: [_jsx("h4", { style: { color: '#9adfbf', margin: '6px 0 8px 2px' }, children: "Incoming" }), receivedMessages.map((msg) => (_jsx(MessageCard, { message: msg, myEmail: myEmail }, msg.message_id)))] })), sentMessages.length > 0 && (_jsxs("section", { children: [_jsx("h4", { style: { color: '#9adfbf', margin: '12px 0 8px 2px' }, children: "Outgoing" }), sentMessages.map((msg) => (_jsx(MessageCard, { message: msg, myEmail: myEmail }, msg.message_id)))] })), receivedMessages.length === 0 && sentMessages.length === 0 && (_jsx("div", { className: "inbox-empty", children: "No messages yet." }))] }))] })] }));
};
export default InboxPanel;
