#!/bin/bash

rm cpp_times.csv
rm cv_times.csv
rm pg_times.csv

touch cpp_times.csv
echo "size, time" >> cpp_times.csv

touch cv_times.csv
echo "size, time" >> cv_times.csv

touch pg_times.csv
echo "size, time" >> pg_times.csv

make -C ../cpp_opencv
for i in {1..10};
do
	let w="64*i";
	let h="48*i";
	echo "Running cpp version for width = $w, height = $h"
	../cpp_opencv/md --tl=0,0 --br=$w,$h
	sleep 5s
	echo "Running opencv version for width = $w, height = $h"
	python3 ../python_opencv/opencv_movement_detection.py -tl 0 0 -br $w $h
	sleep 5s
	echo "Running pygame version for width = $w, height = $h"
	python3 ../python_pygame/pygame_movement_detection.py -tl 0 0 -br $w $h
	sleep 5s
done