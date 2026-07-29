import { useState, useEffect } from "react";
import ApplicationForm from './components/ApplicationForm/ApplicationForm';
import ApplicationList from './components/ApplicationList/ApplicationList';
import FilterBar from "./components/FilterBar/FilterBar";
import API_BASE_URL from "./config" ;
import { filterApplications } from "./components/utils/filterApplications";
import './App.css'


function App() {
  const [showForm, setShowForm] = useState(false);
  const [applications, setApplications] = useState([]);
  const [importMessage, setImportMessage] = useState("");
  const [filters, setFilters] = useState({
    status: "",
    searchText: "",
    priority: "",
    isInactive: false,
    minPay: 0,
    maxPay: 0,
    dateFrom: "",
    dateTo: ""
  });

  const DEFAULT_EXPORT_FILENAME = "job_applications";
  const localDBApplications = `${API_BASE_URL}/applications`;
  const filteredApplications = filterApplications(applications, filters);


  useEffect(() => {
    async function loadApplications() {
        try {
            const response = await fetch(localDBApplications);

            if(!response.ok) {
                throw new Error("Failed to load applciations");
            }

            const data = await response.json();
            setApplications(data)
        } catch (error) {
            console.log(error);
        }
    }
    loadApplications();
  }, []);

  async function handleDeleteApplication(applicationId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this application?"
    );

    if (!confirmed) return;

    const response = await fetch(
        `${API_BASE_URL}/applications/${applicationId}`,
        {
            method: "DELETE"
        }
    );

    if(!response.ok) {
        throw new Error("Failed to delete application.");
    }

    fetch(localDBApplications)
        .then(res => res.json())
        .then(data => setApplications(data));
  }

  async function handleDeleteAllApplications() {
    const confirmed = window.confirm(
        "Are you sure you want to permanently delete every job application?"
    );

    if(!confirmed) return;

    const response = await fetch(`${API_BASE_URL}/applications/all`, {
        method: "DELETE"
    });

    if(!response.ok) {
        throw new Error("Failed to delete all job applications.");
    }

    fetch(localDBApplications)
        .then(res => res.json())
        .then(data => setApplications(data));
  }

  function handleClearFilters() {
    setFilters({
        status: "",
        searchText: "",
        priority: "",
        isInactive: false,
        minPay: 0,
        maxPay: 0,
        dateFrom: "",
        dateTo: ""
    });
  }

  async function handleAddApplication(newApplication) {
    const response = await fetch(localDBApplications, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(newApplication)
    });

    if (!response.ok) {
        throw new Error("Network response was not ok");
    }

    if(response.ok) {
       fetch(localDBApplications)
        .then(res => res.json())
        .then(data => setApplications(data));
       setShowForm(false);
    }
  }

  async function handleExportJSON() {
    const requestedFileName = prompt("Enter a filename for your export:", DEFAULT_EXPORT_FILENAME);
    if (requestedFileName === null) return;
    const filename = requestedFileName.trim() || DEFAULT_EXPORT_FILENAME;
    const downloadUrl = `${API_BASE_URL}/applications/export/json?filename=${encodeURIComponent(filename)}`;
    const link = document.createElement("a");
    link.href = downloadUrl;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);  
  }

    async function handleImportJSON(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(`${API_BASE_URL}/applications/import/json`, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                setImportMessage(data.message);
                fetch(localDBApplications)
                    .then(res => res.json())
                    .then(data => setApplications(data));
                setTimeout(() => {
                    setImportMessage("");
                }, 5000);
             } else {
                setImportMessage(data.detail);
           }
        } catch (error) {
            setImportMessage(`Import failed due to ${error}. Please try again.`);
        }
        event.target.value = "";
    }

  return (
    <div className="app-container">
        <div className="app-header">
            <h1 className="app-title">Job Application Tracker</h1>
        </div>
        <div className="app-toolbar">
            <button onClick={() => setShowForm(!showForm)}>Add Job</button>
            <button onClick={handleExportJSON} disabled={applications.length === 0}>Export All Jobs</button>
            <button onClick={() => document.getElementById("import-input").click()}>Import Jobs</button>
            <button onClick={handleDeleteAllApplications} disabled={applications.length === 0}>
                Delete All Job
            </button>
            <input id="import-input" type="file" accept=".json" style={{ display: "none" }} onChange={handleImportJSON}/>
        </div>
        {importMessage && <p>{importMessage}</p>}
        <FilterBar filters={filters} onFilterChange={setFilters} onClear={handleClearFilters}/>
        {showForm &&  <ApplicationForm onSubmit={handleAddApplication} onClose={() => setShowForm(false)}/>}
        <div className="app-content">
            <ApplicationList 
                applications={filteredApplications} 
                onDelete={handleDeleteApplication}
                onUpdate={() => {
                    fetch(localDBApplications)
                    .then(res => res.json())
                    .then(data => setApplications(data));
                }} 
            />
        </div>

    </div>
    )
}

export default App;