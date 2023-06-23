import cv2
import numpy as np
from flask import Flask, Response, request
import threading
from ultralytics import YOLO

app = Flask(__name__)
current_frame = None
model = YOLO("yolov5s.pt")  # Create the YOLO model

# Specify the desired dimensions for the resized frames
RESIZED_WIDTH = 1200
RESIZED_HEIGHT = 800

@app.route('/')
def home():
    return "Welcome to Video Streaming Server!!!"

@app.route('/video_feed', methods=['POST'])
def video_feed():
    global current_frame

    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame_width = int(request.headers['Frame-Width'])
    frame_height = int(request.headers['Frame-Height'])

    # Resize the frame to desired dimensions
    img = cv2.resize(img, (RESIZED_WIDTH, RESIZED_HEIGHT))

    # Perform object detection on the frame
    results = model.predict(img)

    for result in results:
        for obj in result.boxes:
            x1, y1, x2, y2 = map(int, obj.xyxy[0])  # Convert coordinates to integers
            label = result.names[int(obj.cls[0])]  # Get the class label
            confidence = obj.conf[0]  # Get the confidence score

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)




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
    app.run(host='0.0.0.0', port=8080)
