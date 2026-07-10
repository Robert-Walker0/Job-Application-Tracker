# Job Application Tracker

## Keep track of where you apply with one application

Having problems remembering where you last applied, not anymore. With this application you can keep track of every job you applied with ease. 
Just take note of the company, role, date, hourly or salaried, last heard from, status, link, resume, and notes.  Remove any jobs after a time frame of not hearing back from them or consider them discontinued.


## Technologies

* Python
* React
* FastAPI
* SQLite
* PyTest
* Render

## Features

- Log job applications with company, role, date, platform, link and more.
- Track application status: Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn
- Applications flagged automatically after 2 weeks of no response
- Track interview rounds per application with custom labels
- Export and import data as JSON
- Application history showing all status changes

## The Process

This project started as a personal need: a way to keep track of the job
applications during an active job search, after struggling to remember
where I had applied and the current status of each application.

Before writing any code, the project was planned using a set of
development documents. FUNCTIONS.md became the most useful of these,
breaking the entire project down into named functions across the frontend
and backend before a single line of code was written. This gave a clear
picture of exactly what needed to be built and in what order.

The database schema went through an important evolution during planning.
Originally designed with two tables in mind, the need to track status
changes over time led to the addition of a third — the application
history log. The final schema consists of three tables: job_applications,
interview_rounds, and job_application_log.

The project was built in this order: problem definition, function
breakdown, schema design, database implementation, frontend components,
styling, then backend query functions.

Starting on the database side, the schema was created, and the core
An initialization function was built to set up all three tables on startup.

With the database foundation in place, the main React components were
developed: ApplicationForm for submitting new applications,
ApplicationList for displaying them, and FormInput and FormSelect as
Reusable form elements used throughout the project.

During this time, database.py was expanded with query functions for
adding applications, retrieving by ID, and fetching all applications,
along with a connection helper to standardize database access across
all functions.

The User Interface was styled to match a dark theme with full-width
headers, a toolbar, and a formatted data table. It was tweaked until all
data displayed correctly and the application felt genuinely usable.

The next step after this was developing the FastAPI backend for the application. During this, the routes for retrieving all applications, retrieving by ID, and creating a new application were developed. A Pydantic model was added to handle the data collected for the JobApplication, alongside two utility functions. The most important one, to_camel_case, used an alias generator to accept camelCase field names from React and map them to Python snake case conventions.

CORS middleware was configured to allow the React frontend to communicate with the FastAPI backend both locally and in production on Render. Configuring CORS between the deployment frontend and backend proved to be the most challenging for me, with me receiving environment variable errors, URL mismatches, and reordering the application before GitHub tests passed. Multiple commits and pull requests were needed to fix this issue alone.

With the core functionality working end-to-end, a Pytest suite was written
to cover the database functions, API routes, and utility functions. Tests
were written for both happy paths and error cases. Including missing
required fields, invalid data types, and non-existent IDs. A GitHub
Actions workflow was added to run the full test suite automatically on
every push and pull request to main.

The application was then deployed to Render using two separate services:
a web service for the FastAPI backend and a static site for the React
frontend.

Environment variables were used to manage the frontend and
backend URLs across local development and production without hardcoding
any values.

Finally, for now, an export feature was added, allowing users to download all their
tracked applications as a JSON file — an important addition given that
Render’s free tier uses ephemeral storage, meaning the database resets on
each cold start. The export feature gives users a way to preserve their
data between sessions.


## Planned Features
- Import from JSON to restore exported data
- ApplicationCard for viewing full application details
- Application history log display
- Interview round tracking
- Edit existing applications
- Customizable color schema settings

## What I Learned

Sample text goes here

## Running the Project 

### Requirements

Ensure you have Node.js and Python 3.11 or higher installed before proceeding.


### Locally

You need to setup both the backend and frontend server for both of them to work properly.

**Backend**:
```bash
cd backend
python -m venv .venv
# Window command: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

### Remote
The application is currently live at:
- Frontend: https://job-application-tracker-front.onrender.com
- Backend API: https://job-application-tracker-mxlz.onrender.com/docs

Note: The free tier hosting may take 30-60 seconds to wake up on first visit.

## Video

Coming soon; will be added upon project completion.
