import { useState, useEffect } from "react";
import "./ApplicationCard.css";
import CardField from "./CardField";
import API_BASE_URL from "../config";

export default function ApplicationCard({ application, onClose, onUpdate }) {

    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({ ...application });

    useEffect(() => {
        async function fetchHistory() {
            try {
                const response = await fetch(`${API_BASE_URL}/applications/${application.id}/history`);
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
    }, [application.id]);

    function handleFieldChange(field, value) {
        setEditData(prev => ({ ...prev, [field]: value }));
    }

    function nothingChanged() {
        return Object.keys(editData).every(key => editData[key] === application[key]);
    }

    function handleCancelEdit() {
        setEditData({ ...application });
        setIsEditing(false);
    }

    async function handleSave() {
        if (nothingChanged()) {
            alert("No changes were made.");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/applications/${application.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(editData)
            });

            if (response.ok) {
                setIsEditing(false);
                onUpdate();
            }
        } catch (error) {
            console.error("Error saving application:", error);
        }
    }

    return (
        <div className="card-overlay" onClick={onClose}>
            <div className="card-box" onClick={e => e.stopPropagation()}>

                <div className="card-header">
                    <h2>Job Application #{application.id} — {application.company}</h2>
                    <button className="card-close-button" onClick={onClose}>✕</button>
                </div>

                <div className="card-body">
                    {isEditing ? (
                        <>
                            <div className="card-field">
                                <label className="card-label">Company</label>
                                <input value={editData.company} onChange={e => handleFieldChange("company", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Job Title</label>
                                <input value={editData.jobTitle} onChange={e => handleFieldChange("jobTitle", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Date Applied</label>
                                <input type="date" value={editData.dateApplied} onChange={e => handleFieldChange("dateApplied", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Platform</label>
                                <input value={editData.platform || ""} onChange={e => handleFieldChange("platform", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Link</label>
                                <input type="url" value={editData.link || ""} onChange={e => handleFieldChange("link", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Pay Type</label>
                                <select value={editData.payType} onChange={e => handleFieldChange("payType", e.target.value)}>
                                    <option value="Contract">Contract</option>
                                    <option value="Hourly">Hourly</option>
                                    <option value="Salaried">Salaried</option>
                                    <option value="Internship">Internship</option>
                                </select>
                            </div>
                            <div className="card-field">
                                <label className="card-label">Pay Amount</label>
                                <input type="number" value={editData.payAmount || ""} onChange={e => handleFieldChange("payAmount", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Status</label>
                                <select value={editData.status} onChange={e => handleFieldChange("status", e.target.value)}>
                                    <option value="Applied">Applied</option>
                                    <option value="Phone Screen">Phone Screen</option>
                                    <option value="Interview">Interview</option>
                                    <option value="Offer">Offer</option>
                                    <option value="Rejected">Rejected</option>
                                    <option value="Withdrawn">Withdrawn</option>
                                </select>
                            </div>
                            <div className="card-field">
                                <label className="card-label">Last Heard From</label>
                                <input type="date" value={editData.lastHeardFrom || ""} onChange={e => handleFieldChange("lastHeardFrom", e.target.value)} />
                            </div>
                            <div className="card-field">
                                <label className="card-label">Notes</label>
                                <textarea value={editData.notes || ""} onChange={e => handleFieldChange("notes", e.target.value)} />
                            </div>
                        </>
                    ) : (
                        <>
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
                        </>
                    )}

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
                    {isEditing ? (
                        <>
                            <button className="card-save-btn" onClick={handleSave}>Save Changes</button>
                            <button className="card-cancel-btn" onClick={handleCancelEdit}>Cancel</button>
                        </>
                    ) : (
                        <>
                            <button className="card-edit-btn" onClick={() => setIsEditing(true)}>Edit</button>
                            <button className="card-close-btn" onClick={onClose}>Close</button>
                        </>
                    )}
                </div>

            </div>
        </div>
    );
}