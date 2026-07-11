import "./ApplicationCard.css"

export default function ApplicationCard({ application, onClose }) {
    return (
        <div className="card-overlay" onClick={onClose}>
            <div className="card-box" onClick={e => e.stopPropagation()}>

                <div className="card-header">
                    <h2>Job Application #{application.id} — {application.company}</h2>
                    <button className="card-close-button" onClick={onClose}>✕</button>
                </div>

                <div className="card-body">
                    <div className="card-field">
                        <span className="card-label">Company</span>
                        <span className="card-value">{application.company}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Job Title</span>
                        <span className="card-value">{application.jobTitle}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Date Applied</span>
                        <span className="card-value">{application.dateApplied}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Platform</span>
                        <span className="card-value">{application.platform || "N/A"}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Link</span>
                        <span className="card-value">
                            {application.link 
                                ? <a href={application.link} target="_blank" rel="noreferrer">{application.link}</a>
                                : "N/A"
                            }
                        </span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Pay Type</span>
                        <span className="card-value">{application.payType}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Pay Amount</span>
                        <span className="card-value">{application.payAmount || "N/A"}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Status</span>
                        <span className="card-value">{application.status}</span>
                    </div>
                    <div className="card-field">
                        <span className="card-label">Last Heard From</span>
                        <span className="card-value">{application.lastHeardFrom || "N/A"}</span>
                    </div>
                    <div className="card-field card-notes">
                        <span className="card-label">Notes</span>
                        <span className="card-value">{application.notes || "No notes added."}</span>
                    </div>
                </div>

                <div className="card-footer">
                    <button className="card-close-btn" onClick={onClose}>Close</button>
                </div>

            </div>
        </div>
    )
}