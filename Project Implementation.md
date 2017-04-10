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

A new ROS package, kobuki odom was created and contains a new script `odom_listener` which subscribes to current position of the robot 
(x, y, z) from the _nav_msgs/Odometry_ type message published by the robot in Quaternion form. Another requirement is the current angle of the robot, which is collected from a _geometry_msgs/Quarternion_ type message published from the robot. The angles in Quaternion form and converted to converted to Euler form. The conversion of the angle is included in the `odom_listener` script. The converted angles are published as a new node `odom_listener` with a _geometry_msgs/Vector3_ message type. This node is used in many scripts for Kobuki navigation.
```
rosrun kobuki_odom odom_listener
```

## Marker Detection Phase:

Image recognition is accomplished by the TensorFlow framework based Inception v3 engine. The default engine is designed such that it is not integrated with ROS. An interface was added to integrate Inception V3 with ROS. Positions of the markers are identified by the robot’s orientation data topic and the yaw angle topic. The combined engine and ROS interface subscribes to odometry data and transforms the quaternion-based heading to an Euler angle. 

Once the position of robot is obtained, the Kobuki robot is rotated using keyboard control and commands for starting image capture are executed. Once the live image feed from Asus Xtion camera is up and running, images can be saved at regular intervals. For saving images, the _image_saver_ tool of _image_view_ (a viewer for ROS image topics) is used which subscribes to image feed of camera. When the above _image_saver_ code is executed, images with a resolution of 640x480 are saved whenever the `image_saver save` ROS service is called.
```
rosrun image_view image_view image:=/camera/rgb/image_raw
rosrun image_view image_saver image:=/camera/rgb/image_raw _save_all_image:=false _filename_format:=TestImage.jpg __name:=image_saver
```

The saved image is passed to Inception v3 engine immediately via a bash script.
```
./ImageClassifier.sh
```

Recognized object labels from the image captured after passing through Inception v3 engine are recorded in `Object Position Discovery (OPD)` system which is a column separated values (CSV) file. The object with the highest accuracy is written into the file. There can be multiple labels for the same object in ImageNet, but only the first label is used. All other label entries are omitted. Also, all empty rows are deleted to make the OPD file light and readable. A python script `filecleanup` is executed to clean up and update the OPD file.
```
python FileCleanup.py
```
_image_save_ command is stopped after a few rotations of the robot (this is user defined). When marker detection phase is over, the Kobuki robot is made to stop rotating again using keyboard control. `keyop.launch` process is stopped now.

## Robot Navigation Phase:

The user is prompted with the recognized object labels via a python script `IdentifyLocation`. The purpose of the prompt is to determine which marker the robot is supposed to move towards. After receiving input from user, the updated OPD file is scanned for the location of the target. The average location a selected label from the initial scanning phase is used to determine the object location. The average location of an object is used as the existence of a particular marker in multiple images is likely the case during the scanning phase.
```
python IdentifyLocation.py
```

The algorithm for orienting the robot towards the target is shown in figure below. First, the position of object is read from OPD file and copied to a variable _`required_angle`_. The current yaw angle of the robot is collected from `odom_listener` ROS node. The difference of required angle and current yaw angle is determined and stored in a new variable, _`error`_. The algorithm will minimize the error by rotating the robot towards the object until the error is approximately 0, in which case the robot stops and is oriented with the target.

The distance from the robot to the target is calculated from measurements of the Asus Xtion depth camera. Due to lack of proper laser scanner, a ROS package `depthimage_to_lasercan` is used to convert the point cloud obtained from the depth image to a 2D laser scan in a _sensor_msgs/LaserScan_ type topic. The stock parameters for the `depthimage_to_lasercan` node are modified for the application (_scan_time_ is set to 0.5s, _range_min_ is reduced from 0.45m to 0.10m so the robot can detect the object even if it is very close to it).
```
rosrun depthimage_to_laserscan depthimage_to_laserscan image:=/camera/depth/image_raw _scan_time:=0.5 _min_range:=0.1
```

After `depthimage_to_laserscan` ROS package is up and running, a controller written in python, `move_kobuki` is executed which subscribes to _/scan(sensor msgs/LaserScan)_ type topics and odometry data from the Kobuki in the form of _Twist(geometry_msgs)_ type messages. This script also publishes a ROS topic named `dist_range`. From the depth image values, the shortest distance value is selected and passed to a variable _`minimum_distance`_, which will be the distance for the robot to travel to the required object. Required distance to travel is calculated by taking the magnitude of the difference of minimum distance and current position of Kobuki and stored in variable _`required_distance`_. Command velocity _`cmd_vel`_ is passed to _/mobile base/commands/velocity_ to move the Kobuki in forward direction. When the robot reaches near the required object, the _`cmd_vel`_ is forced to 0. To avoid collision with the object, a safe distance is maintained between the robot and object. This threshold distance is set to 40cm.
```
python scan _subscriber.py
```

In next section, you can see the [Experimental Results](https://github.com/AbhiRP/Autonomous-Robot-Navigation-using-Deep-Learning-Vision-Landmark-Framework/blob/master/Experimental%20Results.md).
