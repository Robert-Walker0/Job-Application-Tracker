import { useState } from "react";
import "./AddRoundForm.css";

export default function AddRoundForm({ onSubmit }) {
    const [label, setLabel] = useState("");
    const [date, setDate] = useState("");
    const [notes, setNotes] = useState("");

    function handleSubmit(e) {
        e.preventDefault();

        if (!label || !date) {
            alert("Label and date are required.");
            return;
        }

        onSubmit({
            id: Date.now(),
            label,
            date,
            notes
        });

        setLabel("");
        setDate("");
        setNotes("");
    }

    return (
        <form className="add-round-form" onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Round label (e.g. Phone Screen)"
                value={label}
                onChange={e => setLabel(e.target.value)}
            />
            <input
                type="date"
                value={date}
                onChange={e => setDate(e.target.value)}
            />
            <textarea
                placeholder="Notes (optional)"
                value={notes}
                onChange={e => setNotes(e.target.value)}
            />
            <button type="submit" className="add-round-submit-btn">Save Round</button>
        </form>
    );
}