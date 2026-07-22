
export default function EditField( {label, fieldName, editData, onFieldChange, type = "text"}) {
    return (
        <div className="card-field">
            <label className="card-label">{label}</label>
            <input
                type={type}
                value={editData[fieldName] || ""}
                onChange={e => onFieldChange(fieldName, e.target.value)}
            /> 
        </div>
    );
}