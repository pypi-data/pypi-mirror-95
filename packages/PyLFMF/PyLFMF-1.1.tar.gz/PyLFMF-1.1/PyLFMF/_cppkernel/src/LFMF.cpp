#include "../include/LFMF.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
namespace py = pybind11;

/*=============================================================================
 |
 |  Description:  Compute the LFMF propagation prediction
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
 |      Outputs:  result        - Result structure
 |
 |      Returns:  error         - Error code
 |
 *===========================================================================*/
void LFMF(double * input_ptr, double * output_ptr)
{
    double h_tx__meter = input_ptr[0];
    double h_rx__meter = input_ptr[1];
    double f__mhz = input_ptr[2];
    double P_tx__watt = input_ptr[3];
    double N_s = input_ptr[4];
    double d__km = input_ptr[5];
    double epsilon = input_ptr[6];
    double sigma = input_ptr[7];
    int pol = input_ptr[8];   

    double f__hz = f__mhz * 1e6;
    double lambda__meter = Cl / f__hz;                           // wavelength, in meters 
    
    int rtn = ValidateInput(&h_tx__meter, &h_rx__meter, f__mhz, P_tx__watt, N_s,
     				 d__km, epsilon, sigma, pol);
    if ((rtn != SUCCESS) && (rtn != TX_CORRECTED)  && (rtn != RX_CORRECTED) && (rtn != TX_RX_CORRECTED))
    {
	    output_ptr[0] = 0;
	    output_ptr[1] = 0;
	    output_ptr[2] = 0;
	    output_ptr[3] = 0;
	    output_ptr[4] = rtn;
	    return;
    }
    output_ptr[4] = rtn;
    // Create the complex value j since this was written by electrical engineers
    complex<double> j = complex<double>(0.0, 1.0);

    double h_1__km = MIN(h_tx__meter, h_rx__meter) / 1000;      // lower antenna, in km
    double h_2__km = MAX(h_tx__meter, h_rx__meter) / 1000;      // higher antenna, in km

    double a_e__km =  a_0__km * 1 / (1 - 0.04665 * exp(0.005577 * N_s));    // effective earth radius, in km

    double theta__rad = d__km / a_e__km;

    double k = 2.0 * PI / (lambda__meter / 1000);               // wave number, in rad/km

    double nu = pow(a_e__km * k / 2.0, THIRD);                  // Intermediate value nu

    // dielectric ground constant. See Eq (17) DeMinco 99-368
    complex<double> eta = complex<double>(epsilon, -sigma / (epsilon_0 * 2 * PI * f__hz));

    // Find the surface impedance, DeMinco 99-368 Eqn (15)
    complex<double> delta = sqrt(eta - 1.0);
    if (pol == POLARIZATION__VERTICAL)
        delta /= eta;

    complex<double> q = -nu * j * delta;                         // intermediate value q 

    // Determine which smooth earth method is used; SG3 Groundwave Handbook, Eq 15
    double d_test__km = 80 * pow(f__mhz, -THIRD);

    double E_gw;
    if (d__km < d_test__km)
    {
        E_gw = FlatEarthCurveCorrection(delta, q, h_1__km, h_2__km, d__km, k);
        output_ptr[3] = METHOD__FLAT_EARTH_CURVE;
    }
    else
    {
        E_gw = ResidueSeries(d__km, k, h_1__km, h_2__km, nu, theta__rad, q);
        output_ptr[3] = METHOD__RESIUDE_SERIES;
    }

    // Antenna gains
    double G_tx__dbi = 4.77;
    double G_rx__dbi = 4.77;

    double G_tx = pow(10, G_tx__dbi / 10);

    // Un-normalize the electric field strength
    double E_0 = sqrt(ETA * (P_tx__watt * G_tx) / (4.0 * PI)) / d__km;  // V/km or mV/m
    
    E_gw = E_gw * E_0;
    std::cout << "E_gw*E_0: " << E_gw << "\n";
    // Calculate the basic transmission loss using (derived using Friis Transmission Equation with Electric Field Strength)
    //      Pt     Gt * Pt * ETA * 4*PI * f^2
    // L = ---- = ---------------------------  and convert to dB
    //      Pr            E^2 * c^2
    // with all values entered using base units: Watts, Hz, and V/m
    // basic transmission loss is not a function of power/gain, but since electric field strength E_gw is a function of (Gt * Pt),
    //    and Lbtl is a function of 1/E_gw, we add in (Gt * Pt) to remove its effects
    output_ptr[0]   = 10 * log10(P_tx__watt * G_tx) 
                + 10 * log10(ETA * 4 * PI) 
                + 20 * log10(f__hz) 
                - 20 * log10(E_gw / 1000) 
                - 20 * log10(Cl);

    // the 60 constant comes from converting field strength from mV/m to dB(uV/m) thus 20*log10(1e3)
    output_ptr[1] = 60 + 20 * log10(E_gw);

    // Note power is a function of frequency.  42.8 comes from MHz to hz, power in dBm, and the remainder from
    // the collection of constants in the derivation of the below equation.
    output_ptr[2] = output_ptr[1] + G_rx__dbi - 20.0*log10(f__hz) + 42.8;

    return;
}
