import cv2
from flask import Flask, Response, request
import threading

app = Flask(__name__)
current_frame = None

frame_received_count = 0  # Track the number of frames received
frame_sent_count = 0  # Track the number of frames sent to the browser URL

@app.route('/')
def home():
    return "Welcome to Video Display Server!!!"

@app.route('/get_frame', methods=['POST'])
def get_frame():
    global current_frame, frame_received_count

    frame_received_count += 1
    print('Frames received from server:', frame_received_count)

    current_frame = request.data
    return "Frame received."

def generate_frames():
    global current_frame, frame_sent_count

    while True:
        if current_frame is not None:
            frame_sent_count += 1
            print('Frames sent to browser URL:', frame_sent_count)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')

@app.route('/display')
def display():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_display_server():
    app.run(host='0.0.0.0', port=8081)

if __name__ == '__main__':
    threading.Thread(target=run_display_server).start()
