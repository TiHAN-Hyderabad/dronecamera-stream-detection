import cv2
import numpy as np
from flask import Flask, request
import requests
import threading
from ultralytics import YOLO

app = Flask(__name__)
frame_url = 'http://192.168.252.225:8081/get_frame'  # URL of the display server's get_frame endpoint

# Specify the desired dimensions for the resized frames
RESIZED_WIDTH = 1200
RESIZED_HEIGHT = 800
model = YOLO("yolov5s.pt")  # Create the YOLO model

def send_frame(frame):
    requests.post(frame_url, data=frame, headers={'Content-Type': 'image/jpeg'})

@app.route('/')
def home():
    return "Welcome to Video Processing Server!!!"

@app.route('/video_feed', methods=['POST'])
def video_feed():
    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame_width = int(request.headers['Frame-Width'])
    frame_height = int(request.headers['Frame-Height'])

    # Resize the frame to desired dimensions
    img = cv2.resize(img, (RESIZED_WIDTH, RESIZED_HEIGHT))

    # Perform object detection on the frame
    # (your object detection code here)
    results = model.predict(img)
    for result in results:
        for obj in result.boxes:
            x1, y1, x2, y2 = map(int, obj.xyxy[0])  # Convert coordinates to integers
            label = result.names[int(obj.cls[0])]  # Get the class label
            confidence = obj.conf[0]  # Get the confidence score

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


    ret, buffer = cv2.imencode('.jpg', img)
    frame_data = buffer.tobytes()
    threading.Thread(target=send_frame, args=(frame_data,)).start()

    return "Frame processed."

def run_processing_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_processing_server).start()
