#ifdef _WIN32
	#include "cpp/H5Cpp.h"
//	#include "H5Cpp.h"
#elif __linux
	#include "H5Cpp.h"
#endif
#include <vector>

#ifndef H5_NO_NAMESPACE
	using namespace H5;
#endif

using namespace std;

int hd5data(vector<vector<vector<int>>> data, float density, float car_ratio, int trial, char* _filename,
			long seed)
{
#define RANK 3
#define COMPRESSION_LEVEL 6
	int VEHICLENUM = data[0].size();
	int TIMESTEPS = data.size();
	hsize_t     dims[RANK] = { TIMESTEPS, VEHICLENUM, 2 };
	char *_data = new char[TIMESTEPS*VEHICLENUM * 2];
	char _density[16];
	char _car_ratio[16];
	char _trial[16];
	
	H5File *file;
	Group* group1;
	Group* group2;
	
	/* Convert the vector into an array */
	for (int i = 0; i < TIMESTEPS*VEHICLENUM * 2; i++) {
		int b = i / (VEHICLENUM * 2);
		int c = i / (2) % VEHICLENUM;
		int d = i % 2;
		_data[i] = data[b][c][d];
	}

	sprintf(_density, "Density::%.2f", density);
	sprintf(_car_ratio, "CarRatio::%.2f", car_ratio);
	sprintf(_trial, "Trial::%04d", trial);
	H5std_string	DATASET_NAME(_trial);
	
	H5std_string	FILE_NAME(_filename);

	Exception::dontPrint();

	/* Try to check is file exists. */
	try{
		file = new H5File(FILE_NAME, H5F_ACC_RDWR);
	}

	/* File does not exist, create file. */
	catch (FileIException error){
		file = new H5File(FILE_NAME, H5F_ACC_TRUNC);
	}
	
	try{
		group1 = new Group(file->openGroup(_car_ratio));
	}

	/* Density Group does not exist, create Group. */
	catch (FileIException error){
		group1 = new Group(file->createGroup(_car_ratio));
	}
	
	try{
		group2 = new Group(group1->openGroup(_density));
	}

	/* Density Group does not exist, create Group. */
	catch (GroupIException error){
		group2 = new Group(group1->createGroup(_density));
	}

	/* Try block to detect exceptions raised by any of the calls inside it */
	try
	{
		// Create the data space for the dataset.

		DataSpace *dataspace = new DataSpace(RANK, dims);

		hsize_t     chunk_dims[RANK] = { 1, VEHICLENUM, 2 };
		DSetCreatPropList  *plist = new  DSetCreatPropList;
		plist->setChunk(RANK, chunk_dims);

		DataType *datatype = new DataType(PredType::STD_I8LE);

		/* Using ZLIB compression library */
		plist->setDeflate(COMPRESSION_LEVEL);

		// Create the dataset.     
		DataSet *dataset = new DataSet(group2->createDataSet(DATASET_NAME, PredType::STD_I32BE, *dataspace, *plist));
		dataset->write(_data, PredType::STD_I8LE);

		DataSet s = group2->openDataSet(DATASET_NAME);
		const H5std_string	ATTR_NAME = "RNG Seed";
		hsize_t attdims[1] = { 1 };
		int attr_data[1] = { seed };

		DataSpace attr_dataspace = DataSpace(1, attdims);
		Attribute attribute = dataset->createAttribute(ATTR_NAME, 
														PredType::STD_I32BE, 
														attr_dataspace, 
														PropList::DEFAULT);
		attribute.write(PredType::STD_I8LE, attr_data);
		attribute.close();

		dataset->close();
		datatype->close();
		dataspace->close();
		group2->close();
		group1->close();
		file->close();
	}  // end of try block

	// catch failure caused by the H5File operations
	catch (FileIException error)
	{
		error.printError();
		return -1;
	}

	// catch failure caused by the DataSet operations
	catch (DataSetIException error)
	{
		error.printError();
		return -1;
	}

	// catch failure caused by the DataSpace operations
	catch (DataSpaceIException error)
	{
		error.printError();
		return -1;
	}

	// catch failure caused by the DataType operations
	catch (DataTypeIException error)
	{
		error.printError();
		return -1;
	}

	// catch failure caused by the Group operations
	catch (GroupIException error)
	{
		error.printError();
		return -1;
	}

	// catch failure caused by the H5File operations
	catch (AttributeIException error)
	{
		error.printError();
		return -1;
	}

	delete[] _data;
	return 0;  // successfully terminated
}