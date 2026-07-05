# Project: JAT/Job Application Tracker

This is not a required document, this is a functionified version of in the project that needs to be completed for self reference.

## React/Frontend

App()
- Main Application, holds everything

~~ApplicationForm()~~
- Add form  for applications or editing

~~FormInput()~~
- Used for reusable input component for ApplicationForm

~~FormSelect()~~
- Used for reusable select component for ApplicationForm

ApplicationLog()
- Display the history log for a single application

ApplicationList()
- Displays all applications

ApplicationCard()
- Single application row

FilterBar()
- Allows the filtering by status, company, date filter, etc

InterviewRoundList()
- Rounds under an application

InterviewRoundForm()
- Adds a new round

ExportButton()
- Triggers JSON Download

ImportButton() 
- Triggers JSON Importer

InactivityFlag()
- Highlights flagged applications

## Python/Backend

### Database

~~initialize_project_database()~~
- Creates the main database for our project, this step/function has been completed/.

### Applications

add_application(company, job_title, date_applied, platform, link, pay_type, pay_amount, notes, status, last_heard_from)
- Insert a new application with the default status of Applied into the list

get_all_applications()
- Returns all application from the database

get_application_by_id(application_id)
- Return a single application by id

filter_applications()
- Return applications based on filter

update_application(application_id, update_fields)
- Update application fields if something actually changed


flag_inactive_applications()
- Flag all applications with applied status with no update in two weeks.

## Status

update_status(id, status)
- Change status and records the of the change

is_closed(application)
- Returns true if the status is rejected or withdrawn

nothing_changed(original, updated)
- Returns if nothing has changed for the applications


## Interview Rounds

add_interview_round(application_id, round_date, round_label, notes)
- Adds an interview round linked to the application


get_interview_rounds(application_id)
- Returns all interview rounds for a given application

## Log

add_log_entry(application_id, log_date, event)
- Write a new entry to job_application_log automatically when a status changes or application is updated.

get_application_log(application_id)
- Returns all log entries for a given application in date order.

## Import

import_from_json()
- Accepts a JSON file previous exported

validate_import_data(data)
- Checks the imported JSON matches expected structure before inserting
- Returns True if valid, False if not

## Export

export_to_json()
- Return all application and their interview rounds as a JSON file for the user to download

## Startup

run_application()
- initialize_project_database()
- flag_inactive_applications()
