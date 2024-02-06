import torch
import cv2
import numpy as np
from flask import Flask, request, jsonify
from ultralytics import YOLO
import time
from datetime import datetime

app = Flask(__name__)
frame_count_client = 0
frame_count_server = 0
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model = YOLO("yolov5s.pt")
model = model.to(device)
# Specify the desired dimensions for the resized frames
RESIZED_WIDTH = 1200
RESIZED_HEIGHT = 800

@app.route('/video_feed', methods=['POST'])
def video():
    st = time.time()
    global frame_count_client, frame_count_server
    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame_width = int(request.headers['Frame-Width'])
    frame_height = int(request.headers['Frame-Height'])
    #client_timestamp = float(request.headers['Client-Timestamp'])
    #server_to_client_delay = time.time() - client_timestamp

    img = cv2.resize(img, (RESIZED_WIDTH, RESIZED_HEIGHT))
    start_time = time.time()
    # Inference
    results = model.predict(img)
    end_time = time.time()
    processing_delay = end_time - start_time
    # Appending labels, confidence to detections
    st_det = time.time()
    detections = []
    for result in results:
        for obj in result.boxes:
            label = result.names[int(obj.cls[0])]
            confidence = obj.conf[0]
            detection = {
                'label': label,
                'confidence': float(confidence)
            }
            detections.append(detection)
    et = time.time()
    total_process = et - st
    rst = start_time - st
    appending_det_values = et - st_det
    response_data = {
        'Processing-Delay': processing_delay,
        'Before-inference-time': start_time,
        'After-inference-time': end_time,
        'detections': detections,
        'total-process': total_process,
        'total-process-start-time': st,
        'total-process-end-time': et,
        'resizing-time': rst,
        'Appending-Det-Values': appending_det_values
    }
    return jsonify(success=True, data="Detected labels and confidences sent to client.", **response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
