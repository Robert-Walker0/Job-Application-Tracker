import FormInput from './FormInput';
import FormSelect from './FormSelect';
import { useState } from "react";
import './ApplicationForm.css';

export default function ApplicationForm({ onSubmit, onClose }) {
    const today = new Intl.DateTimeFormat('en-CA').format(new Date());

    const [company, setCompany] = useState("");
    const [jobTitle, setJobTitle] = useState("");
    const [dateApplied, setDateApplied] = useState(today);
    const [platform, setPlatform] = useState("");
    const [link, setLink] = useState("");
    const [payType, setPayType] = useState("Contract");
    const [payAmount, setPayAmount] = useState("");
    const [notes, setNotes] = useState("");
    const [status, setStatus] = useState("Applied");
    const [lastHeardFrom, setLastHeardFrom] = useState(today);

    function handleSubmit(e) {
        e.preventDefault();

        const newApplication = {
            company,
            jobTitle,
            dateApplied,
            platform,
            link,
            payType,
            payAmount,
            status,
            lastHeardFrom,
            notes
        }

        console.log(newApplication);
        onSubmit(newApplication);
    }

    return (
    <div className="modal-overlay" onClick={onClose}>
        <div className="modal-box" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
                <h2>Add Job Application</h2>
                <button className="modal-close-button" onClick={onClose}>✕</button>
            </div>
            <form onSubmit={handleSubmit}>
                <FormInput label="Company *" value={company} onChange={e => setCompany(e.target.value)} required/>
                <FormInput label="Job Title *" value={jobTitle} onChange={e => setJobTitle(e.target.value)} required/>
                <FormInput label="Date Applied *" value={dateApplied} type="date" onChange={e => setDateApplied(e.target.value)} required/>
                <FormInput label="Platform" value={platform} onChange={e => setPlatform(e.target.value)}/>
                <FormInput label="Job Posting Link" value={link} type="url" onChange={e => setLink(e.target.value)}/>
                <FormSelect label="Pay Type *" value={payType} onChange={e => setPayType(e.target.value)} options={["Contract", "Hourly", "Salaried", "Internship"]} required/>
                <FormInput label="Pay Amount *" value={payAmount} type="number" onChange={e => setPayAmount(e.target.value)} required/>
                <FormInput label="Last Heard From" value={lastHeardFrom} type="date" onChange={e => setLastHeardFrom(e.target.value)}/>
                <div className="form-field">
                    <label>Notes</label>
                    <textarea placeholder="Place notes here" value={notes} onChange={e => setNotes(e.target.value)}/>
                </div>

                <div className="form-buttons">
                    <button type="button" className="button-cancel" onClick={onClose}>Cancel</button>
                    <button type="submit" className="button-submit">Add Application</button>
                </div>
            </form>
        </div>
    </div>
    );
}