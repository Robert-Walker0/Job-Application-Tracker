import { useState } from "react"
import ApplicationForm from './components/ApplicationForm'
import ApplicationList from './components/ApplicationList'

function App() {
  const [showForm, setShowForm] = useState(false);
  const [applications, setApplications] = useState([]);

  function handleAddApplication(newApplication) {
    setApplications(previousJobApplication => [...previousJobApplication, newApplication]);
    setShowForm(false);
  }

  return (
    <div>
      <h1>Job Application Tracker</h1>
      <button onClick={() => setShowForm(!showForm)}>
        Add Job
      </button>
      {showForm && 
      <ApplicationForm
        onSubmit={handleAddApplication}
        onClose={() => setShowForm(false)}
      />
      }
      <ApplicationList applications={applications} />    
    </div>
  )
}

export default App;