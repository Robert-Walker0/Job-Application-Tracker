
export default function CardField({ label, value, noContentText = "N/A", className = ""}) {
    return (
        <div className={`card-field ${className}`}>
            <span className="card-label">{label}</span>
            <span className="card-value">{value || noContentText}</span>
        </div>
    );
}

