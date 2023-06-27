import cv2
from flask import Flask, Response, request
import threading

app = Flask(__name__)
current_frame = None

@app.route('/')
def home():
    return "Welcome to Video Display Server!!!"

@app.route('/get_frame', methods=['POST'])
def get_frame():
    global current_frame
    current_frame = request.data
    return "Frame received."

def generate_frames():
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')

@app.route('/display')
def display():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_display_server():
    app.run(host='0.0.0.0', port=8081)

if __name__ == '__main__':
    threading.Thread(target=run_display_server).start()
