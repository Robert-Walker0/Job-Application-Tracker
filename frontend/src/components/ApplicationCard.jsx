import { useState, useEffect } from "react";
import "./ApplicationCard.css";
import "./CardField";
import CardField from "./CardField";

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
                    <CardField label="Company" value={application.company}/>
                    <CardField label="Job Title" value={application.jobTitle}/>
                    <CardField label="Date Applied" value={application.dateApplied}/>
                    <CardField label="Platform" value={application.platform}/>
                    <CardField label="Link" value={application.link ? (<a href={application.link} target="_blank" rel="noreferrer">{application.link}</a>) : null}/>
                    <CardField label="Pay Type" value={application.payType}/>
                    <CardField label="Pay Amount" value={application.payAmount}/>
                    <CardField label="Status" value={application.status}/>
                    <CardField label="Last Heard From" value={application.lastHeardFrom}/>
                    <CardField label="Notes" value={application.notes} noContentText="No notes added." className="card-notes"/>
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