#ifndef PARSER_H
#define PARSER_H

#include <tuple>
#include <map>

class parser {
	std::string help = std::string("usage: cpp_opencv_movement_detection [--help] [--tl=x1,y1] [--br=x2,y2]\n\n")
			 + "Movement Detection, choose fragment to process\n\n"
			 + "optional arguments:\n"
			 + "--help show this help message and exit"
			 + "--tl=x1,y1 X and Y coordinates of the top left corner of proceeded area\n"
			 + "--br=x2,y2 X and Y coordinates of the bottom right corner of proceeded area\n";
public:
	std::map<std::string, std::tuple<int, int> > parse(int, char**, std::tuple<int, int>);
private:
	std::tuple<int, int> parse_arg(std::string);
	bool are_correct_args(std::tuple<int, int>, std::tuple<int, int>, std::tuple<int, int>);
};
#endif