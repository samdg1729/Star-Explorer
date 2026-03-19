from flask import Flask, render_template # type: ignore
import sqlite3

app = Flask(__name__)

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