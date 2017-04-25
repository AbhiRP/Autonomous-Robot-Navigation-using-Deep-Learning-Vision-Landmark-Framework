#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Created by Abhi Ravikumar (abhi.ravikumar@protonmail.com)
# Graduate Student @ The University of Texas at San Antonio, TX U.S.A
# Research Assistant @ Autonomous Control & Engineering (ACE) Laboratory at UTSA
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#!/bin/sh
while true
do
	echo "Press Ctrl C to stop"
	rosservice call /image_saver/save
	#python /home/abhijith/image_classification/Imageresizer.py
	python classify_image_abhi.py --image_file /home/abhijith/TestImage.jpg
	#espeak -f "Textspeech.txt"
	sleep 1
done


