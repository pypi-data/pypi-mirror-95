#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "../include/LFMF.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

py::array_t<double> vector_LFMF(py::array_t<double> data)
{
	py::buffer_info input_buf = data.request();
	
	int n_obs = input_buf.shape[0];
	
	py::array_t<double> results = py::array_t<double>(n_obs * 5);
	py::buffer_info output_buf = results.request();
	
	
  	double *input_ptr = (double *) input_buf.ptr,
               *output_ptr  = (double *) output_buf.ptr;

	for (size_t idx = 0; idx < n_obs; idx++)
	{
		LFMF(&input_ptr[idx * 9], &output_ptr[idx * 5]);
	}	
	results.resize({n_obs, 5});
	return results;
}

PYBIND11_MODULE(_cppkernel, m)
{

	m.doc()  = R"V0G0N(
Low Frequency / Medium Frequency (LF/MF) Propagation Model

|===============================================================================================|
|					INPUTS:							|
|-------------------------------------------------------------|---------------------------------|
|   Variable  |  Type	|  Units  |         Limits	      |	         Description	        |
|-------------|---------|---------|---------------------------|---------------------------------|
| h_tx__meter |	double	|  meter  |   0 <= h_tx__meter <= UB  |	   Height of the transmitter	|
|-------------|---------|---------|---------------------------|---------------------------------|
| h_rx__meter |	double	|  meter  |   0 <= h_rx__meter <= UB  |    Height of the receiver	|
|-------------|---------|---------|---------------------------|---------------------------------|
| f__mhz      |	double	|   MHz	  |   0.01 <= f__mhz <= 30    |    Frequency            	|		
|-------------|---------|---------|---------------------------|---------------------------------|
| P_tx__watt  |	double	|  Watt	  |       0 < P_tx__watt      |	   Transmitter power		|
|-------------|---------|---------|---------------------------|---------------------------------|
| N_s	      |	double	| N-Units |     250 <= N_s <= 400     |    Surface refractivity		|
|-------------|---------|---------|---------------------------|---------------------------------|
| d__km	      |	double	|   km	  |        0 < d__km	      |	   Path distance		|
|-------------|---------|---------|---------------------------|---------------------------------|
| epsilon     |	double	|         |       1 <= epsilon	      |	   Relative permittivity	|
|-------------|---------|---------|---------------------------|---------------------------------|
| sigma       |	double	|   S/m	  |        0 < sigma	      |	   Conductivity			|
|-------------|---------|---------|---------------------------|---------------------------------|
| pol	      |	 int	|	  | 	 0 = Horizontal       |    Polarization			|
|	      |		|	  |	 1 = Vertical	      |		   			|
|-------------|---------|---------|---------------------------|---------------------------------|
|  UB - upper bound is calculated according to the Handbook on Ground Wave Propagation	        |
|       published by The International Telecommunication Union (ITU):			        |
|       For epsilon << 60 * sigma * lambda: UB = 1.2 * sigma^{1/2} * lambda^{3/2}         	|
|-----------------------------------------------------------------------------------------------|	



|=======================================================================================|
|				   OUTPUTS						|
|==========|========|============|======================================================|
| Variable |  Type  |   Unit     | 	               Description			|
|----------|------- |------------|------------------------------------------------------|
|    A	   | double |	dB	 | 	Basic transmission loss				|
|----------|--------|------------|------------------------------------------------------|
|    E	   | double |	dB(uV/m) |	Electrice field strength			|
|----------|--------|------------|------------------------------------------------------|
|    P	   | double |	 dBm	 |	Received power					|
|----------|--------|------------|------------------------------------------------------|
|  method  |  int   |		 |	Solution method					|
|	   | 	    |		 |	0 = Flat earth with curve correction		|
|	   |	    |		 |	1 = Residue series				|
|----------|--------|------------|------------------------------------------------------|
|  status  |  int   |		 |	0 = SUCCESS					|
|	   |	    |		 |	2000 = Upper bound for h_tx__meter is used	|
|	   |  	    |		 |	2001 = Upper bound for h_rx__meter is used	|
|	   |	    |		 |	2002 = Upper bound for h_tx__meter is used	| 				
|	   |        |            |	1000 = TX terminal height is out of range	|
|          |        |            |      1001 = RX terminal height is out of range	|
|	   |	    |	   	 |	1002 = Frequency is out of range		|
|	   |	    |		 |	1003 = Transmit power is out of range		|
|	   |	    |		 |	1004 = Surface refractivity is out of range	|
| 	   |	    |		 |	1005 = Path distance is out of range		|		
|	   |	    | 		 |	1006 = Epsilon is out of range			|
|	   |	    |		 |	1007 = Sigma is out of range			|
|	   |	    |		 |	1008 = Invalid value for polarization		|
|----------|--------|------------|------------------------------------------------------|)V0G0N";

		
	m.def("LFMF", &LFMF);
	m.def("vector_LFMF", &vector_LFMF);
        m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
}
