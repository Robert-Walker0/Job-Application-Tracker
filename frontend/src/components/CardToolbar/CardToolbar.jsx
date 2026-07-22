
export default function CardToolbar({ activeTab, onTabChange }) {
    return (
        <div className="card-toolbar">
            <button 
                className={activeTab === "Details" ? "active-tab" : ""}
                onClick={() => onTabChange("Details")}
            >
                Details
            </button>
            <button 
                className={activeTab === "Interview Rounds" ? "active-tab" : ""}
                onClick={() => onTabChange("Interview Rounds")}
            >
                Interview Rounds
            </button>
            <button 
                className={activeTab === "Timeline" ? "active-tab" : ""}
                onClick={() => onTabChange("Timeline")}
            >
                Timeline
            </button>
        </div>
    );
}