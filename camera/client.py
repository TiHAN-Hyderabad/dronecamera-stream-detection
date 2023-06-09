import socket
import cv2
import pickle
import struct
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.21.159'  # Enter the Cache Server IP address
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.connect(socket_address)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
raw_capture = PiRGBArray(camera, size=(640, 480))

try:
    print('Connected to Cache Server.')
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        image = imutils.resize(image, width=320)
        frame_data = pickle.dumps(image)
        message = struct.pack("Q", len(frame_data)) + frame_data
        server_socket.sendall(message)
        cv2.imshow("TRANSMITTING TO CACHE SERVER", image)
        key = cv2.waitKey(1) & 0xFF
        raw_capture.truncate(0)
        if key == ord('q'):
            break
except Exception as e:
    print("Error:", str(e))
finally:
    server_socket.close()
    camera.close()
    cv2.destroyAllWindows()