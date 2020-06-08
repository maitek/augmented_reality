#!/usr/bin/env python
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, disconnect
from camera import Camera
import cv2
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()
count = 10
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        
        frame = camera.get_frame_jpeg()
        pos = camera.get_head_pos()
        socketio.emit('my_response',
                    pos,
                    namespace='/test')
        yield frame

# MJPEG video feed         
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
    #app.run(host='0.0.0.0', debug=True)