#!/bin/bash

function print_help {
	echo $'Usage:\nbash run.sh algorithm [type [area]]'
	echo 'Arguments meaning:'
	echo $'\talgorithm: choose what you want to run: movement, edge or face detection'
	echo $'\ttype: choose algorithm type(only movement detection)'
	echo $'\tarea: choose part of screen to proceed(only movement detection)'
	echo 'Possible arguments values:'
	echo $'\talgorithm: movement, edge, face'
	echo $'\ttype(when algorithm=movement): cpp, pygame, opencv'
	echo $'\ttype(when algorithm=edge):-c (Canny), -l (Laplacian), -s (Sobel), -sc (Scharr)'
	echo $'\tarea(when algorithm=movement): four integers x1, y1, x2, y2 such that 0 <= x1 < x2 <= 640 and 0 <= y1 < y2 <= 480'
}

if [ $# = 0 ]; then
	print_help
	exit 0
fi

if [ $1 = "movement" ]; then
	if [ $2 = "cpp" ]; then
		make -C ../movement_detection/partial/cpp_opencv
		if [ $# -gt 2 ]; then
			../movement_detection/partial/cpp_opencv/md --tl=$3,$4 --br=$5,$6
		else
			../movement_detection/partial/cpp_opencv/md
		fi
		rm ../movement_detection/partial/cpp_opencv/md
	elif [ $2 = "pygame" ]; then
		if [ $# -gt 2 ]; then
			python3 ../movement_detection/partial/python_pygame/pygame_movement_detection.py -tl $3 $4 -br $5 $6
		else
 			python3 ../movement_detection/partial/python_pygame/pygame_movement_detection.py
		fi
	elif [ $2 = "opencv" ]; then
		if [ $# -gt 2 ]; then
			python3 ../movement_detection/partial/python_opencv/opencv_movement_detection.py -tl $3 $4 -br $5 $6
		else
 			python3 ../movement_detection/partial/python_opencv/opencv_movement_detection.py
		fi
	fi
elif [ $1 = "edge" ]; then
	python3 ../edge_detection/edge.py $2
elif [ $1 = "face" ]; then
	python3 ../face_detection/face.py
fi

