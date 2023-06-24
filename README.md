# dronecamera-stream-detection
Detect objects using from drone camera streamed to kubernetes

https://stackoverflow.com/questions/48611517/raspberry-pi-3-python-and-opencv-face-recognition-from-network-camera-stream
https://www.youtube.com/watch?v=sYGdge3T30o

dev
# Steps of execution
# Step-1:
- Server send the requests to client
- Client send live video capturing by raspi camera as a response to server
# Step-2:
- Server get that live video stream and do the object detection.
- Expose that object detected live video to the browser when browser enter the url.
# Step-3:
- End user enters the port url in browser then object detected video is displayed in browser which is sent by server.
=======
# Architecture diagram

![Untitled Diagram](https://github.com/TiHAN-Hyderabad/dronecamera-stream-detection/assets/94279266/c34ce4f9-2a8d-4b17-8f0b-27be77b86e8c)

## Discussion on 02/06/2023

- Install the server edition in the raspi. => Future
- Run the object detection on the server but not on raspi.
- 
main
