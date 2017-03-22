The proposed autonomous navigation method is separated into two phases: marker detection and robot navigation. 
## 1) Marker Detection Phase: 
Machine learning is used in the Marker Detection Phase of the navigational algorithm. TensorFlow and the Inception v3 Image Recognition Engine
are used in this phase. The robot captures images of the environment around it and transfers these images to modified Inception v3 Image Classification Engine. Objects identified
with the Inception V3 engine are classified with the classes found in the ImageNet database. This engine records the position and orientation of markers in a file for use by the
controller in the robot navigation phase. 
## 2) Robot Navigation Phase: 
In the navigation phase, the robot prompts the user to identify a marker that the robot should move to. When the user selects a desired marker, the
robot locates the position and orientation of the target in its database. Then the robot calculates the pose of target relative to its current location and orients towards the target. When the
robot has oriented towards the object, the robot moves towards it using on-board depth camera for feedback. 

A flowchart of the process is provided below:
