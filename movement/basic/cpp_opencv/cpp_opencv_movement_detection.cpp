#include <iostream>
#include <unistd.h>
#include <opencv2/opencv.hpp>

void end() {
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

std::string winName = "OpenCV movement detector";

int main(int argc, char** argv) {
	cv::VideoCapture cap = tryInitCapture();
	bool capture = true;
	cv::Mat prev2;
	cv::Mat prev;
	cv::Mat curr;
	cv::Mat frame;
	cap >> curr;
	cap >> prev;
	cv::cvtColor(curr, curr, cv::COLOR_RGB2GRAY);
	cv::cvtColor(prev, prev, cv::COLOR_RGB2GRAY);
	while(capture) {
		prev2 = prev;
		prev = curr;
		cap >> curr;
		cv::cvtColor(curr, curr, cv::COLOR_RGB2GRAY);
		frame = diffImg(prev2, prev, curr);
		imshow(winName, frame);
		if(cv::waitKey(10) == 'q') {
			capture = false;
		}
	}
	end();
	return 0;
}
