# Experimental Results

When the codes are executed as mentioned above, the Kobuki was able to rotate, take multiple images and pass them to modified Inception v3 engine. Figure below shows the Kobuki rotating from its initial position, taking images at fixed intervals.

<p align="center">
  <img src="Images/rotate_1.jpg" width="23%"/> <img src="Images/rotate_2.jpg" width="23%"/> <img src="Images/rotate_3.jpg" width="23%"/> <img src="Images/rotate_4.jpg" width="23%"/>
  
  <em>Kobuki Turtlebot2 scanning the area environment with the vision sensor </em>
</p>

Figure below shows the terminal in which `Inception v3` engine using TensorFlow framework identifies different objects from the image. In the terminal, the identified object along with its accuracy (score) can be seen. 

<p align = "center">
  <img src = "Images/image_classifier.png" width="50%"/>
  
  <em>Terminal window displaying output of Inception v3 engine. The displayed output shows a _backpack_ and a _broom_ were discovered in the last two images.</em>
</p>

The engine classifies the image and the object recognized were registered in a `Object Position Discovery` (OPD) file. The yaw angle from the initial position of the robot to each object was written in same OPD file against the recognized object label. Sample of a generated `Object Position Discovery` file containing each recognized object and the corresponding angles to the objects as shown in figure.

<p align = "center">
  <img src = "Images/OPD.png" width="30%"/>
  
  <em> Sample of a generated Object Position Discovery file containing each recognized object and the corresponding angles to the objects</em>
</p>

The output of the `ImageIdentifier` script after cleaning up the csv file using `FileCleanup` script. All recognized objects were listed and ask the user to select the required object. Figure below a prompt to the user asking for the name of the discovered object.

<p align = "center">
  <img src = "Images/identifylocation.png" width="50%"/>
  
  <em>Terminal displaying the output of the `IdentifyLocation` script. The displayed output shows a prompt to the user asking for the name of the discovered object.</em>
</p>

The robot orients itself towards the required object once it gets an input from the user. At this point the `depthimage_to_laserscan` package was activated. ROS sensor visualization output displaying the _PointCloud_ image taken from the Asus Xtion RGB-D camera is shown in figure on left. Figure on right shows top view of simulated laser scan (_/scan_ ROS topic) from Asus Xtion. The distance of the object is calculated from this data.

<p align = "center">
  <img src = "Images/point cloud cropped.png" width="30%"/> 
  
  <em> OS sensor visualization output displaying the PointCloud image taken from the Asus Xtion RGB-D camera </em> </p>
  
  <p align = "center"> 
  <img src = "Images/laserscan cropped.png" width="27%"/>
  
  <em>Top view of simulated laser scan (_/scan_ ROS topic) from Asus Xtion </em>
</p>

After finding the distance to move, the robot starts moving towards the object. Figures below shows the movement of robot taken at various instances. The Kobuki will stop in front of the object keeping a safe distance.

<p align="center">
  <img src="Images/move1.jpg" width="25%"/> <img src="Images/move2.jpg" width="25%"/> <img src="Images/move3.jpg" width="25%"/>
</p>
