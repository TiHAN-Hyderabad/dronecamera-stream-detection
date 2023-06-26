import cv2
from flask import Flask, Response
import threading

app = Flask(__name__)
frame_file = 'processed_frame.jpg'  # File storing the processed frame

@app.route('/')
def home():
    return "Welcome to Video Display Server!!!"

@app.route('/display')
def display():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    while True:
        frame = cv2.imread(frame_file)  # Read the processed frame from the file
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            current_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')

def run_display_server():
    app.run(host='0.0.0.0', port=8081)

if __name__ == '__main__':
    threading.Thread(target=run_display_server).start()
