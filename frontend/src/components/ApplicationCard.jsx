import { useState, useEffect } from "react";
import "./ApplicationCard.css";

export default function ApplicationCard({ application, onClose }) {
    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        async function fetchHistory() {
            try {
                const response = await fetch(`http://localhost:8000/applications/${application.id}/history`);
                if (response.ok) {
                    const data = await response.json();
                    setHistory(data);
                }
            } catch (error) {
                console.error("Error fetching application history:", error);
            } finally {
                setIsLoading(false);
            }
        }

        fetchHistory();
    }, [application.id, application.status]);

    return (
        <div className="card-overlay" onClick={onClose}>
            <div className="card-box" onClick={e => e.stopPropagation()}>

                <div className="card-header">
                    <h2>Job Application #{application.id} — {application.company}</h2>
                    <button className="card-close-button" onClick={onClose}>✕</button>
                </div>

                <div className="card-body">
                    <div className="card-field">
                        <span className="card-label">Company</span>
                        <span className="card-value">{application.company}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Job Title</span>
                        <span className="card-value">{application.jobTitle}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Date Applied</span>
                        <span className="card-value">{application.dateApplied}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Platform</span>
                        <span className="card-value">{application.platform || "N/A"}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Link</span>
                        <span className="card-value">
                            {application.link 
                                ? <a href={application.link} target="_blank" rel="noreferrer">{application.link}</a>
                                : "N/A"
                            }
                        </span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Pay Type</span>
                        <span className="card-value">{application.payType}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Pay Amount</span>
                        <span className="card-value">{application.payAmount || "N/A"}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Status</span>
                        <span className="card-value">{application.status}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Last Heard From</span>
                        <span className="card-value">{application.lastHeardFrom || "N/A"}</span>
                    </div>
                    <div className="card-field card-notes">
                        <span className="card-label">Notes</span>
                        <span className="card-value">{application.notes || "No notes added."}</span>
                    </div>
                    <div className="card-history-section">
                        <h3 className="history-title">Application Timeline</h3>
                        
                        {isLoading ? (
                            <p className="history-status-text">Loading timeline history...</p>
                        ) : history.length === 0 ? (
                            <p className="no-history-msg">No history exists yet for this application.</p>
                        ) : (
                            <div className="history-timeline">
                                {history.map((log, index) => (
                                    <div key={index} className="history-timeline-item">
                                        <span className="history-item-date">
                                            {/* Matches python database key names returned from your function */}
                                            {log.log_date} — <span className="history-item-time">{log.log_time}</span>
                                        </span>
                                        <span className="history-item-event">{log.event}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                <div className="card-footer">
                    <button className="card-close-btn" onClick={onClose}>Close</button>
                </div>

            </div>
        </div>
    );
}