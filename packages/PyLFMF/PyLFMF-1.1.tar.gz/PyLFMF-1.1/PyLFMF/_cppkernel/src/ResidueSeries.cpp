#include "../include/LFMF.h"
#include <iostream>
/*=============================================================================
 |
 |  Description:  Calculates the groundwave field strength using the
 |                Residue Series method
 |
 |        Input:  d__km         - Path distance, in km
 |                k             - Wavenumber, in rad/km
 |                h_1__km       - Height of the higher antenna, in km
 |                h_2__km       - Height of the lower antenna, in km
 |                nu            - Intermediate value, 
 |                                pow(a_e__km * k / 2.0, THIRD);
 |                theta__rad    - Angular distance of path, in radians
 |                q             - Intermediate value -j*nu*delta
 |
 |      Returns:  E_gw          - Normalized field strength in mV/m
 |
 *===========================================================================*/
double ResidueSeries(double d__km, double k, double h_1__km, double h_2__km, double nu, double theta__rad, complex<double> q)
{
    complex<double> DW2[200], W2[200]; // dummy variables
    complex<double> G;

    complex<double> j = complex<double>(0.0, 1.0);

    complex<double> T[200], W1[200], W[200];
    double yHigh, yLow;

    complex<double> GW = complex<double>(0, 0); // initial ground wave

    // Associated argument for the height-gain function H_1[h_1]
    yHigh = k * h_2__km / nu;

    // Associated argument for the height-gain function H_2[h_2]
    yLow = k * h_1__km / nu;

    double x = nu * theta__rad;

    for (int i = 0; i < 200; i++) 
    {
        T[i] = WiRoot(i + 1, &DW2[i], q, &W2[i], WONE, WAIT); // find the (i+1)th root of Airy function for given q
        W1[i] = Airy(T[i], WONE, WAIT); // Airy function of (i)th root 

        if (h_1__km > 0) 
        {
            W[i] = Airy(T[i] - yLow, WONE, WAIT) / W1[i]; //height gain function H_1(h_1) eqn.(22) from NTIA report 99-368
            
            if (h_2__km > 0)
                W[i] *= Airy(T[i] - yHigh, WONE, WAIT) / W1[i]; //H_1(h_1)*H_1(h_2)
        }
        else if (h_2__km > 0)
            W[i] = Airy(T[i] - yHigh, WONE, WAIT) / W1[i];
        else
            W[i] = complex<double>(1, 0);

        // W[i] is the coefficient of the distance factor for the i-th
        W[i] /= (T[i] - (q*q)); // H_1(h_1)*H_1(h_2)/(t_i-q^2) eqn.26 from NTIA report 99-368
        G = W[i] * exp(-1.0*j*x*T[i]); // sum of exp(-j*x*t_i)*W[i] eqn.26 from NTIA report 99-368
        GW += G; // sum the series
	std::cout << "Residuals GW: " << GW << "\n";
    }

    // field strength.  complex<double>(sqrt(PI/2)) = sqrt(pi)*e(-j*PI/4)
    complex<double> Ew = sqrt(x)*complex<double>(sqrt(PI / 2), -sqrt(PI / 2))*GW;

    double E_gw = abs(Ew); // take the magnitude of the result
    std::cout << "ResSeriesReturn : " << E_gw << "\n";
    return E_gw;

};
