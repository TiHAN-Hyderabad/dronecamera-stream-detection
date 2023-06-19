import cv2
import numpy as np
from flask import Flask, render_template, Response, request
import threading

app = Flask(__name__)
frame = None
frame_size = None

@app.route('/')
def home():
    return "Welcome to Video Streaming Server!!!"

def generate_frames():
    global frame, frame_size
    while True:
        if frame is not None and frame_size is not None:
            img = np.frombuffer(frame, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, frame_size)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    global frame, frame_size
    if request.method == 'POST':
        frame_data = request.data
        frame_width = int(request.headers.get('Frame-Width'))
        frame_height = int(request.headers.get('Frame-Height'))
        frame_size = (frame_width, frame_height)
        frame = np.frombuffer(frame_data, np.uint8)
        print('Frame received from client:', frame.shape)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def process_frame():
    global frame, frame_size
    while True:
        if frame is None or frame_size is None:
            continue

        img = np.frombuffer(frame, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        img = cv2.resize(img, frame_size)

        cv2.imshow("Object Detection", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=process_frame).start()
    app.run(host='0.0.0.0', port=9000)
