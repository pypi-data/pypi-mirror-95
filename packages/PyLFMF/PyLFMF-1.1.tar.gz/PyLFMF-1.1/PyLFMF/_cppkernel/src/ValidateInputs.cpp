#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "../include/LFMF.h"

/*=============================================================================
 |
 |  Description:  Perform input parameter validation
 |
 |        Input:  h_tx__meter   - Height of the transmitter, in meter
 |                h_rx__meter   - Height of the receiver, in meter
 |                f__mhz        - Frequency, in MHz
 |                P_tx__watt    - Transmitter power, in Watts
 |                N_s           - Surface refractivity, in N-Units
 |                d__km         - Path distance, in km
 |                epsilon       - Relative permittivity
 |                sigma         - Conductivity
 |                pol           - Polarization
 |                                  + 0 : POLARIZATION__HORIZONTAL
 |                                  + 1 : POLARIZATION__VERTICAL
 |
 |      Outputs:  [None]
 |
 |      Returns:  error         - Error code
 |
 *===========================================================================*/
int ValidateInput(double * h_tx__meter, double * h_rx__meter, double f__mhz, double P_tx__watt,
    double N_s, double d__km, double epsilon, double sigma, int pol)
{
    
    double f__hz = f__mhz * 1e6;
    double lambda__meter = Cl / f__hz;                  
    
    double upper_bound = 1.2 * sqrt(sigma) * pow(lambda__meter, 3/2);
    
    int flag = 0;
	
    if (*h_tx__meter < 0)
        return ERROR__TX_TERMINAL_HEIGHT;
  

    if (*h_tx__meter > upper_bound)
    {
	    *h_tx__meter = upper_bound;
	    flag = 1;
    }
    
    if (*h_rx__meter < 0)
    	 return ERROR__RX_TERMINAL_HEIGHT;

    if (*h_rx__meter > upper_bound)
    {
	    *h_rx__meter = upper_bound;
	    flag += 2;
    }
    if (f__mhz < 0.01 || f__mhz > 30)
        return ERROR__FREQUENCY;

    if (P_tx__watt <= 0)
        return ERROR__TX_POWER;

    if (N_s < 250 || N_s > 400)
        return ERROR__SURFACE_REFRACTIVITY;

    if (d__km < 0.001 || d__km > 10000)
        return ERROR__PATH_DISTANCE;

    if (epsilon < 1)
        return ERROR__EPSILON;

    if (sigma <= 0)
        return ERROR__SIGMA;

    if (pol != POLARIZATION__HORIZONTAL &&
        pol != POLARIZATION__VERTICAL)
        return ERROR__POLARIZATION;
    
    if (!flag)
	 return SUCCESS;
    else {
	    if (flag == 1)
		    return TX_CORRECTED;
	    if (flag == 2)
		    return RX_CORRECTED;
	    if (flag == 3)
		    return TX_RX_CORRECTED;
    }
	    
}
