from flask import Flask, request
import redis

app = Flask(__name__)

# Connecting to the 'redis' service defined in docker-compose
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Increment visit count in Redis
    r.incr('visit_count')
    
    if request.method == 'POST': 
        message = request.form['message']
        # Push the message to a list in Redis
        r.rpush('messages', message)

    return '''
        <h1>Message Collector</h1>
        <form method="POST">
            <input type="text" name="message" placeholder="Enter message" required>
            <button type="submit">Send</button>
        </form>
    '''

if __name__ == '__main__':
    # host='0.0.0.0' is required for the app to be reachable from outside the container
    app.run(host='0.0.0.0', port=5000)