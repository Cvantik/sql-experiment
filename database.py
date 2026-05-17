import sqlite3

DB_NAME = "job_applications.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        position TEXT,
        date_applied TEXT,
        status TEXT,
        location TEXT,
        contact_person TEXT,
        notes TEXT
    )
    """)
    conn.commit()
    return conn

def fetch_applications(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM applications")
    return c.fetchall()

def add_application(conn, data):
    c = conn.cursor()
    c.execute("""
        INSERT INTO applications (company, position, date_applied, status, location, contact_person, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()

def update_application(conn, data, app_id):
    c = conn.cursor()
    c.execute("""
        UPDATE applications
        SET company=?, position=?, date_applied=?, status=?, location=?, contact_person=?, notes=?
        WHERE id=?
    """, (*data, app_id))
    conn.commit()

def delete_application(conn, app_id):
    c = conn.cursor()
    c.execute("DELETE FROM applications WHERE id=?", (app_id,))
    conn.commit()

def get_connection():
    """Returns a new database connection (without reinitializing schema)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    return conn, c

def get_status_distribution(conn):
    """Return a dictionary with counts of each status."""
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM applications")
    rows = cursor.fetchall()

    counts = {}
    for (status,) in rows:
        counts[status] = counts.get(status, 0) + 1
    return counts
