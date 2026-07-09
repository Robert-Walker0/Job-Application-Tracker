import { useState, useEffect } from "react"
import ApplicationForm from './components/ApplicationForm'
import ApplicationList from './components/ApplicationList'
import API_BASE_URL from "./config"
import './App.css'


function App() {
  const [showForm, setShowForm] = useState(false);
  const [applications, setApplications] = useState([]);
  const localDBApplications = `${API_BASE_URL}/applications`;

  useEffect(() => {
    fetch(localDBApplications)
    .then(res => res.json())
    .then(data => setApplications(data))
  }, []);

  async function handleAddApplication(newApplication) {
    const response = await fetch(localDBApplications, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(newApplication)
    });

    if(response.ok) {
        const data = await response.json();
        console.log(data);
        setApplications(previousJobApplication => [...previousJobApplication, newApplication]);
        setShowForm(false);
    }
  }

  return (
    <div className="app-container">

        <div className="app-header">
            <h1 className="app-title">Job Application Tracker</h1>
        </div>

        <div className="app-toolbar">
            <button onClick={() => setShowForm(!showForm)}>
                Add Job
            </button>
        </div>

        {showForm && 
            <ApplicationForm
                onSubmit={handleAddApplication}
                onClose={() => setShowForm(false)}
            />
        }

        <div className="app-content">
            <ApplicationList applications={applications} />
        </div>

    </div>
)
}

export default App;