#include <iostream>
#include <unistd.h>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <ctime>

void end(std::string window = "") {
	if(window != "") {
		cv::destroyWindow(window);
	}
	std::cout << "Program ended\n";
	exit(0);
}

cv::Mat diffImg(cv::Mat t0, cv::Mat t1, cv::Mat t2) {
	cv::Mat d1;
	cv::Mat d2;
	cv::Mat result;
	cv::absdiff(t2, t1, d1);
	cv::absdiff(t1, t0, d2);
	cv::bitwise_and(d1, d2, result);
	return result;
}

int customErrorHandler(int status, const char* func_name, const char* err_msg, const char* file_name, int line, void* data) {
	std::cout << "ERROR occured" << std::endl;
	end();
	return 0;
}

cv::VideoCapture tryInitCapture() {
	std::cout << "Initializing camera" << std::flush;
	cv::VideoCapture* cap = new cv::VideoCapture(0);
	for(int i = 0; i < 10 && !cap -> isOpened(); i++) {
		free(cap);
		cap = new cv::VideoCapture(0);
		std::cout << "." << std::flush;
		sleep(1);
	}
	if(cap -> isOpened()) {
		std::cout << "\r" << "Camera initialized succesfully\n";
	}
	else {
		std::cout << "\r" << "Camera could not be initialized\n";
		end();
	}
	return *cap;
}

void timespec_diff(struct timespec *start, struct timespec *stop, struct timespec *result) {

    if ((stop->tv_nsec - start->tv_nsec) < 0) {
        result->tv_sec = stop->tv_sec - start->tv_sec - 1;
        result->tv_nsec = stop->tv_nsec - start->tv_nsec + 1000000000;
    } else {
        result->tv_sec = stop->tv_sec - start->tv_sec;
        result->tv_nsec = stop->tv_nsec - start->tv_nsec;
    }
}

std::ostream& operator<<(std::ostream& o, const struct timespec& t) {
	o << t.tv_nsec + t.tv_sec * 1000000000;
	return o;
}

std::string winName = "OpenCV movement detector";

int main(int argc, char** argv) {
	cv::VideoCapture cap = tryInitCapture();
	bool capture = true;
	cv::Mat prev2;
	cv::Mat prev;
	cv::Mat curr;
	cap >> curr;
	cap >> prev;
	cv::cvtColor(curr, curr, cv::COLOR_RGB2GRAY);
	cv::cvtColor(prev, prev, cv::COLOR_RGB2GRAY);
	struct timespec t1, t2, tdiff;
	std::ofstream out("cpp_opencv_time.txt", std::ios::out);
	int i = 0;
	while(i++ < 50) {
		prev2 = prev;
		prev = curr;
		cap >> curr;
		clock_gettime(CLOCK_MONOTONIC, &t1);
		cv::cvtColor(curr, curr, cv::COLOR_RGB2GRAY);
		cv::Mat frame = diffImg(prev2, prev, curr);
		clock_gettime(CLOCK_MONOTONIC, &t2);
		timespec_diff(&t1, &t2, &tdiff);
		out<<tdiff<<std::endl;	
		imshow(winName, frame);
		if(cv::waitKey(10) == 'q') {
			capture = false;
		}
	}
	out.close();
	end(winName);
	return 0;
}
