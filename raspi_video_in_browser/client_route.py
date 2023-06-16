import cv2
import requests
import struct
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera

# Configure camera settings
camera = PiCamera()
camera.resolution = (320, 240)  # Decrease the resolution
camera.framerate = 15  # Decrease the frame rate
raw_capture = PiRGBArray(camera, size=(320, 240))

server_url = 'http://192.168.21.159:9000/video_feed'

try:
    print('Connected to Cache Server.')
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Resize the frame
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
        requests.post(server_url, data=frame_data, headers=headers)

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
