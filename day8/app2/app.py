import os
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, app TEXT, visited_at TIMESTAMP DEFAULT NOW())")
    cur.execute("INSERT INTO visits (app) VALUES ('app2')")
    conn.commit()
    cur.execute("SELECT app, visited_at FROM visits ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    items = "".join(f"<li>{name} at {when:%H:%M:%S}</li>" for name, when in rows)
    return f"<h1>App 2: Visit Log</h1><p>Last 10 visits from both apps:</p><ul>{items}</ul>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
