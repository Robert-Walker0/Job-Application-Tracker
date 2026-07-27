import { useState } from "react";
import ApplicationCard from "../ApplicationCard/ApplicationCard";
import "./ApplicationList.css";

export default function ApplicationList({
    applications,
    onUpdate,
    onDelete,
}) {
    const [selectedApplication, setSelectedApplication] = useState(null);
    const [contextMenu, setContextMenu] = useState(null);

    return (
        <div
            className="application-table-container"
            // Close the menu if the user clicks elsewhere.
            onClick={() => setContextMenu(null)}
        >
            <h2>Current Tracked Applications ({applications.length})</h2>

            {applications.length === 0 ? (
                <h3 className="no-applications">No jobs being tracked</h3>
            ) : (
                <table className="application-table">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Location</th>
                            <th>Priority</th>
                            <th>Work Type</th>
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
                        {applications.map((application) => (
                            <tr
                                key={application.id}
                                className={`application-table-row ${
                                    application.isInactive
                                        ? "highlight-inactive"
                                        : ""
                                }`}
                                style={{ cursor: "pointer" }}

                                onClick={() =>
                                    setSelectedApplication(application)
                                }

                                onContextMenu={(event) => {
                                    event.preventDefault();

                                    setContextMenu({
                                        x: event.pageX,
                                        y: event.pageY,
                                        application,
                                    });
                                }}
                            >
                                <td>{application.company}</td>
                                <td>{application.jobTitle}</td>
                                <td>{application.location}</td>
                                <td>{application.priority}</td>
                                <td>{application.workType}</td>
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
            )}
            {contextMenu && (
                <div
                    className="context-menu"
                    style={{
                        position: "absolute",
                        top: contextMenu.y,
                        left: contextMenu.x,
                    }}
                    onClick={(event) => event.stopPropagation()}
                >
                    <button
                        onClick={() => {
                            const confirmed = window.confirm(
                                "Are you sure you want to delete this application?"
                            );

                            if (confirmed) {
                                onDelete(contextMenu.application.id);
                            }

                            setContextMenu(null);
                        }}
                    >
                        Delete
                    </button>
                </div>
            )}

            {selectedApplication && (
                <ApplicationCard
                    application={selectedApplication}
                    onClose={() => setSelectedApplication(null)}
                    onUpdate={() => {
                        onUpdate();
                        setSelectedApplication(null);
                    }}
                />
            )}
        </div>
    );
}