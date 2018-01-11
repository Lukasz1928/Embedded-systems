#include <iostream>
#include <unistd.h>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <ctime>
#include "parser.h"
#include "utils.h"

std::tuple<int, int> size = std::make_tuple(640, 480);

void end(std::string window = "") {
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
	parser p;
	std::map<std::string, std::tuple<int, int> > args;
	try {
		args = p.parse(argc, argv, size);
	}
	catch(std::string e) {
		std::cout << e;
		end();
	}
	cv::Rect img_part(std::get<0>(args["tl"]), std::get<1>(args["tl"]), std::get<0>(args["br"]) - std::get<0>(args["tl"]), std::get<1>(args["br"]) - std::get<1>(args["tl"]));
	cv::VideoCapture cap = tryInitCapture();
	bool capture = true;
	cv::Mat prev2;
	cv::Mat prev2Part;
	cv::Mat prev;
	cv::Mat prevPart;
	cv::Mat curr;
	cv::Mat currPart;
	cap >> prev;
	cap >> curr;
	cv::cvtColor(curr(img_part), currPart, cv::COLOR_RGB2GRAY);
	cv::cvtColor(prev(img_part), prevPart, cv::COLOR_RGB2GRAY);
	cv::Mat diff;
	cv::Mat frame;
	while(capture) {
		prev2Part = prevPart;
		prev2 = prev;
		prevPart = currPart;
		prev = curr;
		cap >> curr;
		currPart = curr(img_part);
		cv::cvtColor(currPart, currPart, cv::COLOR_RGB2GRAY);
		diff = diffImg(prev2Part, prevPart, currPart);
		cv::cvtColor(diff, diff, cv::COLOR_GRAY2RGB);
		frame = curr.clone();
		diff.copyTo(frame.rowRange(std::get<1>(args["tl"]), std::get<1>(args["br"])).colRange(std::get<0>(args["tl"]), std::get<0>(args["br"])));
		imshow(winName, frame);
		if(cv::waitKey(1) == 'q') {
			capture = false;
		}
	}
	end();
	return 0;
}
