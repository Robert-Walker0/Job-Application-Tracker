import './TimelineTab.css';


export default function ApplicationTimeline( { history, isLoading} ) {

    if(isLoading) {
        return <p className="history-status-text">Loading timeline history...</p>
    }

    if(history.length === 0) {
        return <p className="no-history-msg">NO history exists yet for this application</p>
    }

    return (
        <div className="history-timeline">
            {history.map((log, index) => (
                <div key={index} className="history-timeline-item">
                    <span className="history-item-date">
                        {log.log_date} — <span className="history-item-time">{log.log_time}</span>
                    </span>
                    <span className="history-item-event">{log.event}</span>
                </div>
            ))}
        </div>
    )
}