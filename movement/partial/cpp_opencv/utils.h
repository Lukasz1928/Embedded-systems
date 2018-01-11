#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <ctime>

void timespec_diff(struct timespec*, struct timespec*, struct timespec*);

std::ostream& operator<<(std::ostream&, const struct timespec&);

#endif