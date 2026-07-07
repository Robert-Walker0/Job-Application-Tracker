import "./ApplicationList.css"

export default function ApplicationList({ applications }) {
    return (
        <div className="application-table-container">
            <h2>Current Tracked Applications</h2>
            {applications.length === 0
                ? <h3 className="no-applications">No jobs being tracked</h3>
                : <table className="application-table">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Date Applied</th>
                            <th>Platform</th>
                            <th>Link</th>
                            <th>Pay Type</th>
                            <th>Pay Amount</th>
                            <th>Status</th>
                            <th>Last Heard From</th>
                        </tr>
                    </thead>
                    <tbody>
                        {applications.map(application => (
                            <tr key={application.id}>
                                <td>{application.company}</td>
                                <td>{application.jobTitle}</td>
                                <td>{application.dateApplied}</td>
                                <td>{application.platform || "N/A"}</td>
                                <td>{application.link}</td>
                                <td>{application.payType}</td>
                                <td>{application.payAmount || "N/A"}</td>
                                <td>{application.status}</td>
                                <td>{application.lastHeardFrom || "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            }
        </div>
    );
}