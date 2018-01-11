#include "parser.h"
#include <iostream>
#include <getopt.h>


std::map<std::string, std::tuple<int, int> > parser::parse(int argc, char** argv, std::tuple<int, int> size) {
	static struct option long_options[] = {
		{"tl", optional_argument, NULL, 'a'},
		{"br", optional_argument, NULL, 'b'},
		{"help", optional_argument, NULL, 'h'},
		{NULL, 0, NULL, 0}
	};
	int c;
	std::tuple<int, int> tl = std::make_tuple(0, 0);
	std::tuple<int, int> br = size;
	while((c = getopt_long(argc, argv, "+-a:b:", long_options, NULL)) != -1) {
		switch(c) {
		case 'a':
			tl = parse_arg(optarg);
			break;
		case 'b':
			br = parse_arg(optarg);
			break;
		case 'h':
			throw help;
			break;
		default:
			std::cout << "No such argument is handled" << std::endl;
			break;
		}
	}
	if(!are_correct_args(tl, br, size)) {
		throw std::string("ERROR: Coordinates must satisfy:\n0 <= x1 < x2 < 640 and 0 <= y1 < y2 < 480\n");
	}
	std::map<std::string, std::tuple<int, int> > result;
	result.insert(std::pair<std::string, std::tuple<int, int> >("tl", tl));
	result.insert(std::pair<std::string, std::tuple<int, int> >("br", br));
	return result;
}

std::tuple<int, int> parser::parse_arg(std::string arg) {
	int a, b;
	sscanf(arg.c_str(), "%d,%d", &a, &b);
	return std::make_tuple(a, b);
}

bool parser::are_correct_args(std::tuple<int, int> tl, std::tuple<int, int> br, std::tuple<int, int> size) {
	if(std::get<0>(tl) < 0 || std::get<0>(tl) > std::get<0>(size) || std::get<1>(tl) < 0 || std::get<1>(tl) > std::get<1>(size)) {
		return false;
	}
	else if(std::get<0>(br) < 0 || std::get<0>(br) > std::get<0>(size) || std::get<1>(br) < 0 || std::get<1>(br) > std::get<1>(size)) {
		return false;
	}
	else if(std::get<0>(tl) > std::get<0>(br) || std::get<1>(tl) > std::get<1>(br)) {
		return false;
	}
	return true;
}
