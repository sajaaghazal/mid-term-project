from flask import Flask, request, render_template_string
import redis

app = Flask(__name__)

# Connects to the Redis service using the name 'redis' from docker-compose
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def collector():
    # 1. Increment visit count every time the page is loaded
    r.incr('visit_count')
    
    status_message = ""
    
    if request.method == 'POST':
        user_text = request.form.get('message')
        if user_text:
            # 2. Store the message in a Redis list called 'user_messages'
            r.lpush('user_messages', user_text)
            status_message = "Message saved successfully!"

    # Simple HTML Form for the user to type into
    return render_template_string('''
        <h1>DevOpsHub: Message Collector (App 1)</h1>
        <p>Type a message to send to the Dashboard.</p>
        <form method="post">
            <input type="text" name="message" placeholder="Enter message here..." required>
            <button type="submit">Submit</button>
        </form>
        <p style="color: green;">{{ status }}</p>
        <br>
        <a href="http://localhost:5001">Go to Dashboard (App 2)</a>
    ''', status=status_message)

if name == "__main__":
    app.run(host="0.0.0.0", port=5000)