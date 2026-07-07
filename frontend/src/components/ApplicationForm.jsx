import FormInput from './FormInput';
import FormSelect from './FormSelect';
import { useState } from "react";

export default function ApplicationForm( {onSubmit, onClose}) {
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
            notes,
            status,
            lastHeardFrom
        }

        console.log(newApplication);
        onSubmit(newApplication);
    }

    return (
        <form onSubmit={handleSubmit}>
            <FormInput label="Company *" value={company} onChange={e => setCompany(e.target.value)} required/>
            <FormInput label="Job Title *" value={jobTitle} onChange={e => setJobTitle(e.target.value)} required/>
            <FormInput label="Date *" value={dateApplied} type="date" onChange={e => setDateApplied(e.target.value)} required/>
            <FormInput label="Platform" value={platform} onChange={e => setPlatform(e.target.value)}/>
            <FormInput label="Job Posting Link" value={link} type="url" onChange={e => setLink(e.target.value)}/>
            <FormSelect label = "Pay Type *" value={payType} onChange={e => setPayType(e.target.value)} options={["Contract", "Hourly", "Salaried", "Internship"]} required/>
            <FormInput label="Pay Amount *" value={payAmount} type="number" onChange={e => setPayAmount(e.target.value)} required/>
            <label>Notes
                <textarea placeholder="Place notes here" value={notes} onChange={e => setNotes(e.target.value)}/>
            </label>
            <FormInput label="Last Heard From" value={lastHeardFrom} type="date" onChange={e => setLastHeardFrom(e.target.value)}/>
            <button type="submit">Add Application</button>
            <button type="button" onClick={onClose}>Cancel</button>
        </form>
    )
}