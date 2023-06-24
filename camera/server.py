import socket
import cv2
import pickle
import struct
import threading
from flask import Flask, render_template, Response
from ultralytics import YOLO
import torch
import numpy as np

app = Flask(__name__)
app.debug = False
model = YOLO("yolov5s.pt")
server_socket = None

@app.route('/')
def index():
    return render_template('index.html')

def start_video_stream():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = '192.168.21.159'
    print('HOST IP:', host_ip)
    port = 5000
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen()
    print("Listening at", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                img = frame.copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (640, 480))
                img = torch.from_numpy(img.transpose((2, 0, 1))).float()
                img /= 255.0
                img = img.unsqueeze(0)

                results = model.predict(img, show=True)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(start_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    thread = threading.Thread(target=start_video_stream, args=())
    thread.start()
    app.run(debug=True)
