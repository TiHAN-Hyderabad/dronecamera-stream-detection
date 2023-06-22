# dronecamera-stream-detection
Detect objects using from drone camera streamed to kubernetes

https://stackoverflow.com/questions/48611517/raspberry-pi-3-python-and-opencv-face-recognition-from-network-camera-stream
https://www.youtube.com/watch?v=sYGdge3T30o

# Steps of execution
# Step-1:
- Server send the requests to client
- Client send live video capturing by raspi camera as a response to server
# Step-2:
- Server get that live video stream and do the object detection.
- Expose that object detected live video to the browser when browser enter the url.
# Step-3:
- End user enters the port url in browser then object detected video is displayed in browser which is sent by server.
