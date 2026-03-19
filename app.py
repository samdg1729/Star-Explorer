from flask import Flask, render_template # type: ignore
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("stars.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        distance REAL,
        spectral_type TEXT,
        habitable INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM stars")
    count = cursor.fetchone()[0]

    if count == 0:
        stars_data = [
            ("Proxima Centauri", 4.24, "M", 1),
            ("Alpha Centauri A", 4.37, "G", 0),
            ("Alpha Centauri B", 4.37, "K", 0),
            ("Barnard's Star", 5.96, "M", 0),
            ("Sirius A", 8.6, "A", 0),
            ("Epsilon Eridani", 10.5, "K", 1),
            ("Tau Ceti", 11.9, "G", 1)
        ]

        cursor.executemany(
            "INSERT INTO stars (name, distance, spectral_type, habitable) VALUES (?, ?, ?, ?)",
            stars_data
        )

    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect("stars.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home route - show all stars
@app.route("/")
def home():
    conn = get_db_connection()
    stars = conn.execute(
        "SELECT name, distance FROM stars ORDER BY distance ASC"
    ).fetchall()
    conn.close()
    return render_template("index.html", stars=stars, title="All Stars")

# Habitable stars route
@app.route("/habitable")
def habitable():
    conn = get_db_connection()
    stars = conn.execute(
        "SELECT name, distance FROM stars WHERE habitable = 1 ORDER BY distance ASC"
    ).fetchall()
    conn.close()
    return render_template("index.html", stars=stars, title="Habitable Stars")

if __name__ == "__main__":
    app.run()