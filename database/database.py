"""
ResumeAI Database Configuration

SQLite database connection and initialization.
"""

import sqlite3
import os


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "resumeai.db"
)


# ============================================================
# CREATE DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create database file and required tables.
    """

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = get_connection()

    cursor = connection.cursor()


    # --------------------------------------------------------
    # Screening Sessions Table
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS screening_sessions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_description TEXT NOT NULL,

            total_candidates INTEGER DEFAULT 0,

            shortlisted INTEGER DEFAULT 0,

            not_shortlisted INTEGER DEFAULT 0,

            average_score REAL DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    # --------------------------------------------------------
    # Candidate Results Table
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id INTEGER,

            candidate_name TEXT NOT NULL,

            score REAL,

            status TEXT,

            skills_score REAL,

            education_score REAL,

            role_score REAL,

            project_score REAL,

            tfidf_score REAL,

            semantic_score REAL,

            FOREIGN KEY(session_id)
            REFERENCES screening_sessions(id)

        )
        """
    )


    connection.commit()

    connection.close()


# ============================================================
# TEST RUN
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "ResumeAI database initialized successfully."
    )