import cv2
import requests
import struct
import time
import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
raw_capture = PiRGBArray(camera, size=(640, 480))

server_url = 'http://192.168.103.220:8080/video_feed'

frames_sent_to_server = 0

try:
    print('Connected to Cache Server.')
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.resize(image, (320, 240))  # Resize the frame

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', image)
        frame_data = buffer.tobytes()

        headers = {
            'Content-Type': 'application/octet-stream',
            'Frame-Width': str(image.shape[1]),
            'Frame-Height': str(image.shape[0]),
            'Client-Timestamp': str(time.time())
        }
        start_time = time.time()
        response = requests.post(server_url, data=frame_data, headers=headers)
        end_time = time.time()
        delay = end_time - start_time
        print('Frame sent to server:', response.status_code)
        print('Delay time (client to server):', delay)

        frames_sent_to_server += 1
        print("Frame count:", frames_sent_to_server)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print('Frame sent by client at:', current_time)

        #cv2.imshow("TRANSMITTING TO CACHE SERVER", image)

        key = cv2.waitKey(1) & 0xFF
        raw_capture.truncate(0)
        if key == ord('q'):
            break
except Exception as e:
    print("Error:", str(e))
finally:
    camera.close()
    cv2.destroyAllWindows()

print("Frames sent to server:", frames_sent_to_server)
