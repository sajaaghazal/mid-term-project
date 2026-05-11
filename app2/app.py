
from flask import Flask, render_template_string
import redis

app = Flask(__name__)

# host='redis' matches the service name in docker-compose
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def index():
    # Retrieve data from Redis
    visits = r.get('visit_count') or 0
    message_count = r.llen('user_messages')
    all_messages = r.lrange('user_messages', 0, -1)

    # Basic HTML Dashboard
    html = f"""
    <h1>DevOpsHub Dashboard</h1>
    <p><strong>Total Visits:</strong> {visits}</p>
    <p><strong>Total Messages:</strong> {message_count}</p>
    <hr>
    <h3>Message Log:</h3>
    <ul>{"".join([f"<li>{msg}</li>" for msg in all_messages])}</ul>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)