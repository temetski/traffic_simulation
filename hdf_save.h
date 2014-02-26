#ifndef _HDF_SAVE_COMPRESS_H
#define _HDF_SAVE_COMPRESS_H

#if (_MSC_VER >= 1400)
	#define _CRT_SECURE_NO_WARNINGS
#endif

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

int hd5data(vector<vector<vector<short>>> data, float density, float car_ratio, int trial, char* _filename,
			long seed);
#endif
