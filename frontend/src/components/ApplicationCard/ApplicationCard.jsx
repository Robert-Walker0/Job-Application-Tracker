import { useState, useEffect } from "react";
import "./ApplicationCard.css";
import CardEditForm from "../CardEditForm/CardEditForm";
import CardDetailView from "../CardDetailView/CardDetailView";
import TimelineTab from "../TimelineTab/TimelineTab";
import API_BASE_URL from "../../config";

export default function ApplicationCard({ application, onClose, onUpdate }) {

    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({ ...application });
    const [activeTab, setActiveTab] = useState("Details");

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
                <div className="card-toolbar">
                    <button className="active-tab" onClick={() => null}>
                        Details
                    </button>
                    <button onClick={() => null}>
                        Interview Rounds
                    </button>
                    <button onClick={() => null}>
                        Timeline
                    </button>
                </div>
                <div className="card-body">
                    {isEditing ? (<CardEditForm editData={editData} onFieldChange={handleFieldChange}/>) : (<CardDetailView application={application}/>)}
                    <div className="card-history-section">
                        <h3 className="history-title">Application Timeline</h3>
                        <TimelineTab history={history} isLoading={isLoading}/>
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