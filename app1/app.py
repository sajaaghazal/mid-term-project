from flask import Flask, request
import redis

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    r.incr('visit_count')
    if request.method == 'POST':
        message = request.form['message']
        r.rpush('messages', message)

    return '''
        <h1>Message Collector</h1>
        <form method="POST">
            <input type="text" name="message" placeholder="Enter message" required>
            <button type="submit">Send</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)