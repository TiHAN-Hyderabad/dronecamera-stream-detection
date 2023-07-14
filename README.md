# dronecamera-stream-detection
Detect objects using from drone camera streamed to kubernetes

https://stackoverflow.com/questions/48611517/raspberry-pi-3-python-and-opencv-face-recognition-from-network-camera-stream
https://www.youtube.com/watch?v=sYGdge3T30o

dev
# Steps of execution
### Step-1:
- Server send the requests to client
- Client send live video capturing by raspi camera as a response to server
### Step-2:
- Server get that live video stream and do the object detection.
- Expose that object detected live video to the browser when browser enter the url.
### Step-3:
- End user enters the port url in browser then object detected video is displayed in browser which is sent by server.
# Architecture diagram

![Untitled Diagram](https://github.com/TiHAN-Hyderabad/dronecamera-stream-detection/assets/94279266/c34ce4f9-2a8d-4b17-8f0b-27be77b86e8c)


# Documentation

The main objective of the project is to create a system that enables live video streaming from a drone camera to a server for real-time object detection. The client code represents the drone camera module, which captures frames using the PiCamera. It continuously sends these frames to the server code.

The client code captures frames, resizes them, encodes them in JPEG format, and sends them to the server using HTTP POST requests. The server code receives the frames, decodes them, resizes them to a desired dimension, and performs object detection on the frames using the YOLO model. Detected objects are then annotated on the frames. The annotated frames are made available as a continuous video stream for viewing.

### Raspberry pi configuration
* Model: Raspberry-pi-4

### How the entire code works?
#### (1) Start the Server:
* The server code should be executed first.
* The server starts by importing the necessary modules and creating a Flask app.
* It defines the necessary routes, such as the root route ('/') and the video feed route ('/video_feed').
* The YOLO model is initialized.
* The desired dimensions for resized frames are specified.
* The generate() function and the process_frame() function are defined.
* Finally, the server is run using app.run() with the specified host and port.
#### (2) Start the Client:
* The client code is executed after the server code is running.
* The client starts by importing the necessary modules.
* The PiCamera and PiRGBArray objects are created to handle frame capture.
* The URL of the server where frames will be sent is specified.
* The main loop for frame capturing, processing, and sending is started using a try-except-finally block.
#### (3) Client Captures and Sends Frames:
* Inside the main loop, the client continuously captures frames from the PiCamera using camera.capture_continuous().
* Each captured frame is resized using imutils.resize() to a width of 320 pixels.
* The frame is then encoded in JPEG format using cv2.imencode().
* The encoded frame data is stored in the frame_data variable.
* The necessary headers for the HTTP POST request are defined.
* The frame data is sent to the server using requests.post().
* The server's response status code is printed.
* The captured frame is displayed locally using cv2.imshow().
#### (4) Server Receives and Processes Frames:
* The server receives frames through the '/video_feed' route, which accepts POST requests.
* The received frame data is decoded using np.frombuffer() and cv2.imdecode().
* The frame is resized to the desired dimensions using cv2.resize().
* Object detection is performed on the frame using the YOLO model.
* Detected objects are annotated on the frame using rectangles and labels.
* The annotated frame is encoded in JPEG format using cv2.imencode().
* The encoded frame is stored in the current_frame variable.
* The server updates the frame count variables.
* The server returns a response of "Video frame received."
#### (5) Server Generates Video Stream:
* The generate() function continuously checks if current_frame is not None.
* If a new frame is available, it yields the frame with appropriate headers as a multipart response.
* This creates a continuous video stream.
#### (6) Client and Server Communication:
* The client sends each captured frame to the server using an HTTP POST request.
* The server receives and processes each frame, performing object detection and annotating the frame.
* The annotated frames are then made available as a continuous video stream.
* The client continuously displays the frames received from the server locally using cv2.imshow().
#### (7) Termination:
* To stop the client, the user can press the 'q' key, which breaks out of the main loop.
* The client code then closes the PiCamera and destroys OpenCV windows.
* To stop the server, the user can press the 'q' key, which breaks out of the process_frame() loop.
* The server code then destroys OpenCV windows and terminates.

### Deploying pod in kubernetes dashboard:
* Created docker image for server – 9381421553/image1.
* Deployed .yaml script in kubernetes dashboard for the pod to run.
* After successful running of pod start the client code and open the url in browser.

### Screenshots

* This is the demo streaming video:
https://github.com/TiHAN-Hyderabad/dronecamera-stream-detection/assets/94279266/f02c4b47-5aa0-482c-ac4a-6aa9a528bc2f
* This is the screenshot of logs of server pod:
![Screenshot from 2023-07-05 11-43-10](https://github.com/TiHAN-Hyderabad/dronecamera-stream-detection/assets/94279266/ac92e995-b95e-4e32-9124-33376978bb2d)
* This is the demo video when drone is flying:
https://github.com/TiHAN-Hyderabad/dronecamera-stream-detection/assets/94279266/e2326a5b-cd1c-4533-a8d1-cfc3ba651d39

### Resources 
* https://youtu.be/Az1MH_e1hVA - to display video in browser
* https://github.com/ultralytics/yolov5 - to understand and use yolov5 model
* https://youtu.be/9BnubSbXnRM - to use Flask API

### Testing
#### I did testing using CPU only.
#### Test-1:
* In this I kept drone and server at same place and did testing.The results I got:
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.027099
  * Delay from server to browser url: 0.015
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.019686
  * Delay from server to browser url: 0.016348
* Here client sent 267 frames in 49.264599 seconds, so 5.419 frames per second approximately.
#### Test-2:
* In this I kept drone at 5 meters from server and did testing.The results I got:
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.160655
  * Delay from server to browser url: 0.016859
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.136318
  * Delay from server to browser url: 0.0161
* Here client sent 273 frames in 51.873947 seconds, so 5.26 frames per second approximately.
#### Test-3:
* In this I kept objects at 10 meters from drone and did testing.The results I got:
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.203943
  * Delay from server to browser url: 0.021099
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 5.662186
  * Delay from server to browser url: 0.016122
* Here client sent 347 frames in  15 seconds, so 23.2 frames per second approximately.

#### I did testing using GPU.
#### Test-1 :
* In this I kept objects at less than 1meter distance and did testing.The results I got:
* Network speed : 50 Mbps
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.027099
  * Delay from server to browser url: 0.015
  * Delay from client to browser url: 0.042099
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.019686
  * Delay from server to browser url: 0.016348
  * Delay from client to browser url: 0.036034
* Here client sent 225 frames in  61.457714 seconds, so 3.66 frames per second approximately.
#### Test-2 :
* In this I kept objects at 5 meters from drone and did testing.Here also I used only CPU in .yaml script.The results I got:
* Network speed : 100 Mbps
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.160655
  * Delay from server to browser url: 0.016859
  * Delay from client to browser url: 0.177514
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.136318
  * Delay from server to browser url: 0.016165
  * Delay from client to browser url: 0.152483
* Here client sent 280 frames in 31.99 seconds, so 8.75 frames per second approximately.
#### Test-3 (objects are at 10 meters away from drone):
* Network speed : 70 Mbps
* In this I kept objects at 10 meters from drone and did testing.The results I got:
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.102356
  * Delay from server to browser url: 0.014856
  * Delay from client to browser url: 0.117212
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.031748
  * Delay from server to browser url: 0.010426
  * Delay from client to browser url: 0.042174
* Here client sent 1269 frames in  240 seconds, so 5.28 frames per second approximately.
#### Test-4 (During flying):
* Network speed : 70 Mbps
  - [ ] At first frame(Delay in seconds):
  * Delay from client to server: 0.049506
  * Delay from server to browser url: 0.015341
  *  Delay from client to browser url: 0.064847
  - [ ] At last frame(Delay in seconds):
  * Delay from client to server: 0.049857
  * Delay from server to browser url: 0.015336
  *  Delay from client to browser url: 0.065193
* Here client sent 561 frames in  230 seconds, so 2.5 frames per second approximately.

#### Further changes to be done:
* As I used yolov5 pre-trained model it was detecting only 80 classes present in it.So we have to train that model with the labels we want.
* When the network is slow frame rate per second is varying. Network speed is directly proportional to frame rate per second.
* As we have advanced cameras compared to raspberry pi, we can use them for better resolution and quality of video.





  
