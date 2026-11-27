import os
import redis
from flask import Flask

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, decode_responses=True)

@app.route("/")
def register():
    number = r.incr("registrations")
    return f"<h1>TechFest Registration</h1><p>You are registered! Your number is {number}.</p>"

@app.route("/count")
def count():
    total = r.get("registrations") or 0
    return f"<h1>TechFest</h1><p>Total registrations so far: {total}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
