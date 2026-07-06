
export default function ApplicationList({ applications }) {
    return (
        <div>
            <h2>Current Tracked Applications</h2>
            {
                applications.length === 0
                ? <h3>No jobs being tracked</h3>
                : <h3>Jobs go here</h3>
            }
        </div>
    );
}

 