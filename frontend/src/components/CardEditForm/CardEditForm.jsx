import EditField from "./EditField";

export default function CardEditForm({ editData, onFieldChange }) {
    return (
        <div className="edit-grid">
            <EditField label="Company" fieldName="company" editData={editData} onFieldChange={onFieldChange} />
            <EditField label="Job Title" fieldName="jobTitle" editData={editData} onFieldChange={onFieldChange} />
            <EditField label="Location" fieldName="location" editData={editData} onFieldChange={onFieldChange}/>
            <div className="card-field">
                <label className="card-label">Priority</label>
                <select value={editData.priority} onChange={e => onFieldChange("priority", e.target.value)}>
                    <option value="None">None</option>
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                </select>
            </div>
            <div className="card-field">
                <label className="card-label">Work Type</label>
                <select value={editData.workType} onChange={e => onFieldChange("workType", e.target.value)}>
                    <option value="On-Site">On-Site</option>
                    <option value="Hybrid">Hybrid</option>
                    <option value="Remote">Remote</option>
                </select>
            </div>
            <EditField label="Date Applied" fieldName="dateApplied" type="date" editData={editData} onFieldChange={onFieldChange} />
            <EditField label="Platform" fieldName="platform" type="text" editData={editData} onFieldChange={onFieldChange}/>
            <EditField label="Link" fieldName="link" type="url" editData={editData} onFieldChange={onFieldChange} />
            <div className="card-field">
                <label className="card-label">Pay Type</label>
                <select value={editData.payType} onChange={e => onFieldChange("payType", e.target.value)}>
                    <option value="Contract">Contract</option>
                    <option value="Hourly">Hourly</option>
                    <option value="Salaried">Salaried</option>
                    <option value="Intership">Intership</option>
                </select>
            </div>
            <EditField label="Pay Amount" fieldName="payAmount" type="number" editData={editData} onFieldChange={onFieldChange} />
            <div className="card-field">
                <label className="card-label">Status</label>
                <select value={editData.status} onChange={e => onFieldChange("status", e.target.value)}>
                    <option value="Applied">Contract</option>
                    <option value="Phone Screen">Phone Screen</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Withdrawn">Withdrawn</option>
                </select>
            </div>
            <EditField label="Last Heard From" fieldName="lastHeardFrom" type="date" editData={editData} onFieldChange={onFieldChange}/>
            <EditField label="Resume Name" fieldName="resumeName" editData={editData} onFieldChange={onFieldChange}/>
            <EditField className="card-notes" label="Notes" fieldName="notes" type="text" editData={editData} onFieldChange={onFieldChange}/>
        </div>
    );
}