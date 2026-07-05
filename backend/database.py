import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'job_application_tracker_table.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

def initialize_project_databases():
    connection = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH) as file:
        connection.executescript(file.read())
    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize_project_databases()
    print("Database created successfully.")