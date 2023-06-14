import cv2
import numpy as np
from flask import Flask, request, Response
from ultralytics import YOLO
import threading

app = Flask(__name__)
model = YOLO("yolov5s.pt")
frame = None

@app.route('/video_feed', methods=['POST'])
def video_feed():
    global frame
    frame_data = request.data
    frame = np.frombuffer(frame_data, np.uint8)
    return Response(status=200)

def process_frame():
    global frame
    while True:
        if frame is not None:
            img = np.frombuffer(frame, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            results = model.predict(source=img, show=True)

            if isinstance(results, list):
                for img in results:
                    if isinstance(img, list):
                        for sub_img in img:
                            if isinstance(sub_img, np.ndarray):
                                sub_img_rgb = cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB)
                                cv2.imshow("Object Detection", sub_img_rgb)
                    else:
                        if isinstance(img, np.ndarray):
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            cv2.imshow("Object Detection", img_rgb)
            else:
                img_rgb = cv2.cvtColor(results.imgs[0], cv2.COLOR_BGR2RGB)
                cv2.imshow("Object Detection", img_rgb)

            frame = None

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 9000, 'threaded': True})
    server_thread.start()
    process_frame()

