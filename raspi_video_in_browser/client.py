import cv2
import requests
import struct
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
raw_capture = PiRGBArray(camera, size=(640, 480))

server_url = 'http://192.168.21.159:8080/video_feed'
frames_sent = 0

try:
    print('Connected to Cache Server.')
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        image = imutils.resize(image, width=320)

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', image)
        frame_data = buffer.tobytes()

        # Send the frame to the server
        headers = {
            'Content-Type': 'application/octet-stream',
            'Frame-Width': str(image.shape[1]),
            'Frame-Height': str(image.shape[0])
        }
        response = requests.post(server_url, data=frame_data, headers=headers)
        print('Frame sent to server:', response.status_code)
        frames_sent += 1

        cv2.imshow("TRANSMITTING TO CACHE SERVER", image)

        key = cv2.waitKey(1) & 0xFF
        raw_capture.truncate(0)
        if key == ord('q'):
            break
except Exception as e:
    print("Error:", str(e))
finally:
    camera.close()
    cv2.destroyAllWindows()

print("Frames sent to server:", frames_sent)
