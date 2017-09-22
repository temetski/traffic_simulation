py: pytraffic.pyx
	python setup.py build_ext --inplace
clean:
	rm pytraffic.cpp pytraffic*.so

