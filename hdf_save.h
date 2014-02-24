#ifndef _HDF_SAVE_COMPRESS_H
#define _HDF_SAVE_COMPRESS_H

#ifdef _WIN32
	#include "cpp/H5Cpp.h"
#elif __linux
	#include "H5Cpp.h"
#endif
#include <vector>

#ifndef H5_NO_NAMESPACE
	using namespace H5;
#endif

using namespace std;

int hd5data(vector<vector<vector<int>>> data, float density, float car_ratio, int trial, char* _filename,
			long seed);
#endif
