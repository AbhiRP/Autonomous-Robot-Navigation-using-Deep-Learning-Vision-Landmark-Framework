# Project Implementation

The project implementation is again divided into two phases. Before starting the marker detection phase, the Kobuki robot need to be prepared. 

ROS packages are used for the interface for the connectivity to the Kobuki Turtlebot2 and the ASUS Xtion RGB-D camera. The Kobuki ROS launch file `minimal.launch` is executed first to bring up the robot model and start the basic nodes of the robot. The OPENNI2 ROS launch file `openni2.launch` is used to connect to OpenNI-compliant devices such as the Asus Xtion. The robot keyboard controller launch file `keyop.launch` provides control for the initial stage to rotate the robot while taking pictures.

A general purpose consumer laptop is used to supplement the robot’s on-board computer. The ODROID microcomputer can run the image recognition engine but adds a significant level of latency to the operations of the robot. ROS is used to facilitate the connectivity between the microcomputer and the laptop. Software developed using the ROS middleware only needs to be aware of the IP Address of the microcomputer to subscribe to the camera topic.

The Kobuki robot is accessed through the laptop over Wi-Fi using SSH.
```
ssh -X odroid@<ip address>
```

After logging into the Kobuki robot, the above mentioned _launch files_ are executed to activate basic nodes, camera and keyboard control.
```
roslaunch kobuki_node minimal.launch
roslaunch openni2_launch openni2.launch
roslaunch kobuki_keyop keyop.launch
```

A new ROS package, kobuki odom was created and contains a new script `odom listener` which subscribes to current position of the robot 
(x, y, z) from the _nav_msgs/Odometry_ type message published by the robot in Quaternion form. Another requirement is the current angle of the robot, which is collected from a _geometry_msgs/Quarternion_ type message published from the robot. The angles in Quaternion form and converted to converted to Euler form. The conversion of the angle is included in the `odom listener` script. The converted angles are published as a new node `odom listener` with a _geometry_msgs/Vector3_ message type. This node is used in many scripts for Kobuki navigation.
```
rosrun kobuki_odom odom_listener
```

## Marker Detection Phase

Image recognition is accomplished by the TensorFlow framework based Inception v3 engine. The default engine is designed such that it is not integrated with ROS. An interface was added to integrate Inception V3 with ROS. Positions of the markers are identified by the robot’s orientation data topic and the yaw angle topic. The combined engine and ROS interface subscribes to odometry data and transforms the quaternion-based heading to an Euler angle. 

Once the position of robot is obtained, the Kobuki robot is rotated using keyboard control and commands for starting image capture are executed. Once the live image feed from Asus Xtion camera is up and running, images can be saved at regular intervals. For saving images, the _image_saver_ tool of _image_view_ (a viewer for ROS image topics) is used which subscribes to image feed of camera. When the above _image_saver_ code is executed, images with a resolution of 640x480 are saved whenever the _image_saver save_ ROS service is called.
```
rosrun image_view image_view image:=/camera/rgb/image_raw
rosrun image_view image_saver image:=/camera/rgb/image_raw _save_all_image:=false _filename_format:=TestImage.jpg __name:=image_saver
```

The saved image is passed to Inception v3 engine immediately via a bash script.
```
./ImageClassifier.sh
```
