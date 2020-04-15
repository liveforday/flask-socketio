from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import time
from threading import Lock


async_mode=None
thread = None
thread_lock = Lock()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode)

def send_timer():
    while True:
        socketio.sleep(2)
        socketio.emit('my_respones', {'data':'response'}, namespace="/test")
        print('timer')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # emit('my_respones', {'data':'response'})
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(send_timer)
if __name__ == '__main__':
    socketio.run(app, debug=True)