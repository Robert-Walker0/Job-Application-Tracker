import CardField from './CardField'
import './CardDetailView.css';

export default function CardDetailView({ application }) {
    return(
        <div className="details-grid"> 
            <CardField label="Company" value={application.company}/>
            <CardField label="Job Title" value={application.jobTitle}/>
            <CardField label="Location" value={application.location}/>
            <CardField label="Priority" value={application.priority}/>
            <CardField label="Work Type" value={application.workType}/>
            <CardField label="Date Applied" value={application.dateApplied}/>
            <CardField label="Platform" value={application.platform}/>
            <CardField label="Link" value={application.link ? (<a href={application.link} target="_blank" rel="noreferrer">{application.link}</a>) : null}/>
            <CardField label="Pay Type" value={application.payType}/>
            <CardField label="Pay Amount" value={application.payAmount}/>
            <CardField label="Status" value={application.status}/>
            <CardField label="Last Heard From" value={application.lastHeardFrom}/>
            <CardField label="Resume Name" value={application.resumeName || "No Resume Attached"}/>
            <CardField label="Notes" value={application.notes} noContentText="No notes added." className="card-notes"/>
        </div>
    )
}