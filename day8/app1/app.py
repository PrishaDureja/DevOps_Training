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
    cur.execute("INSERT INTO visits (app) VALUES ('app1')")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"<h1>App 1: Visitor Counter</h1><p>Your visit was saved in the database.</p><p>Total visits from both apps: {total}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
