import { useState } from "react";
import "./InterviewRoundsTab.css";
import AddRoundForm from "../AddRoundForm/AddRoundForm";

export default function InterviewRoundsTab({ rounds, onAddRound }) {
    const [isAdding, setIsAdding] = useState(false);

    function handleAdd(roundData) {
        onAddRound(roundData);
        setIsAdding(false);
    }

    return (
        <div className="rounds-container">
            <div className="rounds-header">
                <h3 className="rounds-title">Interview Rounds</h3>
                <button className="rounds-add-btn" onClick={() => setIsAdding(prev => !prev)}>
                    {isAdding ? "Cancel" : "+ Add Round"}
                </button>
            </div>

            {isAdding && <AddRoundForm onSubmit={handleAdd} />}

            {rounds.length === 0 ? (
                <p className="rounds-empty">No interview rounds logged yet.</p>
            ) : (
                <ul className="rounds-list">
                    {rounds.map(round => (
                        <li key={round.id} className="round-item">
                            <div className="round-item-header">
                                <span className="round-label">{round.label}</span>
                                <span className="round-date">{round.date}</span>
                            </div>
                            {round.notes && <p className="round-notes">{round.notes}</p>}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}