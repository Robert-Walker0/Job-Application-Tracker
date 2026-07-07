import { useState } from "react"
import ApplicationForm from './components/ApplicationForm'
import ApplicationList from './components/ApplicationList'
import './App.css'

function App() {
  const [showForm, setShowForm] = useState(false);
  const [applications, setApplications] = useState([]);

  function handleAddApplication(newApplication) {
    setApplications(previousJobApplication => [...previousJobApplication, newApplication]);
    setShowForm(false);
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