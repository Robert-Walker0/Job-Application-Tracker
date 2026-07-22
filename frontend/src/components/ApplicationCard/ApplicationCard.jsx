import { useState, useEffect } from "react";
import "./ApplicationCard.css";
import InterviewRoundsTab from '../InterviewRoundsTab/InterviewRoundsTab';
import CardEditForm from "../CardEditForm/CardEditForm";
import CardToolbar from "../CardToolbar/CardToolbar";
import CardDetailView from "../CardDetailView/CardDetailView";
import TimelineTab from "../TimelineTab/TimelineTab";
import API_BASE_URL from "../../config";

export default function ApplicationCard({ application, onClose, onUpdate }) {

    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({ ...application });
    const [rounds, setRounds] = useState([]);
    const [isLoadingRounds, setIsLoadingRounds] = useState(true);
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

    useEffect(() => {
        async function fetchRounds() {
            try {
                const response = await fetch(`${API_BASE_URL}/applications/${application.id}/interview-rounds`);
                if (response.ok) {
                    const data = await response.json();
                    setRounds(data);
                }
            } catch (error) {
                console.error("Error fetching interview rounds:", error);
            } finally {
                setIsLoadingRounds(false);
            }
        }
        fetchRounds();
    }, [application.id]);

    async function handleAddRound(roundData) {
        try {
            const response = await fetch(`${API_BASE_URL}/applications/${application.id}/interview-rounds`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    roundLabel: roundData.label,
                    roundDate: roundData.date,
                    notes: roundData.notes
                })
            });

            if (response.ok) {
                const result = await response.json();
                setRounds(prev => [
                    ...prev,
                    {
                        id: result.id,
                        roundLabel: roundData.label,
                        roundDate: roundData.date,
                        notes: roundData.notes
                    }
                ]);
            }
        } catch (error) {
            console.error("Error adding interview round:", error);
        }
    }

    function handleFieldChange(field, value) {
        setEditData(prev => ({ ...prev, [field]: value }));
    }

    function nothingChanged() {
        return Object.keys(editData).every(key => editData[key] === application[key]);
    }

    function handleTabChange(currentTab) {
        if(currentTab == activeTab) return;

        if(isEditing) {
            handleCancelEdit();
        }
        setActiveTab(currentTab);
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
                <CardToolbar activeTab={activeTab} onTabChange={handleTabChange}/>
                <div className="card-body">
                    {activeTab === "Details" && (isEditing ? (<CardEditForm editData={editData} onFieldChange={handleFieldChange}/>) : (<CardDetailView application={application}/>))}
                    {activeTab === "Timeline" && (
                        <div className="card-history-section">
                            <h3 className="history-title">Application Timeline</h3>
                            <TimelineTab history={history} isLoading={isLoading}/>
                        </div>
                    )}
                    {activeTab === "Interview Rounds" && (
                        <InterviewRoundsTab rounds={rounds} isLoading={isLoadingRounds} onAddRound={handleAddRound}/>
                    )}
                </div>
                <div className="card-footer">
                    {isEditing ? (
                        <>
                            <button className="card-save-btn" onClick={handleSave}>Save Changes</button>
                            <button className="card-cancel-btn" onClick={handleCancelEdit}>Cancel</button>
                        </>
                    ) : (
                        <>
                            {activeTab === "Details" && (<button className="card-edit-btn" onClick={() => setIsEditing(true)}>Edit</button>)}
                            <button className="card-close-btn" onClick={onClose}>Close</button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}