import cv2
import numpy as np
from flask import Flask, render_template, Response, request
import threading
from ultralytics import YOLO

app = Flask(__name__)
current_frame = None
model = YOLO("yolov5s.pt")

@app.route('/')
def home():
    return "Welcome to Video Streaming Server!!!"

@app.route('/video_feed', methods=['POST'])
def video_feed():
    global current_frame

    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    # Process the frame here using the model or any other operations
    # Example: processed_frame = model.detect(img)

    ret, buffer = cv2.imencode('.jpg', img)
    current_frame = buffer.tobytes()

    return "Video frame received."

@app.route('/get_frame')
def get_frame():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    global current_frame

    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')

def process_frame():
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=process_frame).start()
    app.run(host='0.0.0.0', port=9000)
