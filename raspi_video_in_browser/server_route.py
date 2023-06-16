import cv2
import numpy as np
from flask import Flask, request, Response, render_template
from ultralytics import YOLO
import threading

app = Flask(__name__)
model = YOLO("yolov5s.pt")
frame = None
frame_size = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    global frame, frame_size

    if request.method == 'POST':
        frame_data = request.data
        frame = np.frombuffer(frame_data, np.uint8)

        frame_width = request.headers.get('Frame-Width')
        frame_height = request.headers.get('Frame-Height')
        if frame_width is not None and frame_height is not None:
            try:
                frame_size = (int(frame_width), int(frame_height))
            except ValueError:
                return Response('Invalid frame size', status=400)
        else:
            return Response('Frame size headers not found', status=400)

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    global frame, frame_size
    while True:
        if frame is not None and frame_size is not None:
            img = np.frombuffer(frame, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, frame_size)

            results = model.predict(source=img, show=True)

            if isinstance(results, list):
                for img in results:
                    if isinstance(img, list):
                        for sub_img in img:
                            if isinstance(sub_img, np.ndarray):
                                sub_img_rgb = cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB)
                                frame_data = cv2.imencode('.jpg', sub_img_rgb)[1].tobytes()
                                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
                    else:
                        if isinstance(img, np.ndarray):
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            frame_data = cv2.imencode('.jpg', img_rgb)[1].tobytes()
                            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
            else:
                img_rgb = cv2.cvtColor(results.imgs[0], cv2.COLOR_BGR2RGB)
                frame_data = cv2.imencode('.jpg', img_rgb)[1].tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

            frame = None
            frame_size = None

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 9000, 'threaded': True})
    server_thread.start()
