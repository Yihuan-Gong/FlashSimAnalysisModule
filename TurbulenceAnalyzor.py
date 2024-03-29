import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
import os
from scipy.integrate import quad
from scipy.optimize import curve_fit
from typing import Tuple

class TurbulenceAnalyzor:
    def __init__(self) -> None:
        self.kpc2cm = 3.08567758e21
        self.maxLevel = 6
        self.nindex_rho = 1.
        self.ds = None
        self.rboxKpc = None
        self.k = None
        self.Ek = None
        self.alpha = None
    
    
    def __rho_g1(self, x, rho_g0=0.472e7, a=600, a_c=60, c=0.17, n=5):
        alpha = -1 - n*(c-1)/(c-a/a_c)
        beta =  1 - n*(1-a/a_c)/(c-a/a_c)
        return rho_g0 * (1+x/a_c) * (1+(x/a_c)/c)**alpha * (1+x/a)**beta

    def __dM_g1(self, x):
        return 4*np.pi*x**2*self.__rho_g1(x)

    def __M_g1(self, x):
        return quad(self.__dM_g1, 0, x)

    def __kolmogorov(self, k, alpha):
        return alpha*k**(-5/3)
    
    def __getVelocityPowerSpectrum(self, v_components, rho, rboxKpc : float=75): # L in kpc
        nx = ny = nz = 2*rboxKpc
        rboxCm = rboxKpc*self.kpc2cm
        dxCm = 1.*self.kpc2cm

        # Creat the space to put 3D KE power spectrum
        Kk = np.zeros((nx // 2 + 1, ny // 2 + 1, nz // 2 + 1))

        for v_component in v_components:

            Kk += 0.5 * self.__fft_comp( v_component, rho )

        # If d is bot specified in f = fft.rfftfreq(), then f should be 
        # normalized by N_tot/T_0
        kx = np.fft.rfftfreq(nx) * nx / (2*rboxCm)
        ky = np.fft.rfftfreq(ny) * ny / (2*rboxCm)
        kz = np.fft.rfftfreq(nz) * nz / (2*rboxCm)

        # physical limits to the wavenumbers
        kmin = 1.0 / (2*rboxCm)  # f_0
        kmax = np.min(0.5 * 1./dxCm)  # Nyquist frequency = 0.5*N_tot*f_0

        kbins = np.arange(kmin, kmax, kmin)
        N = len(kbins) # should be N = N_tot/2

        # bin the Fourier KE into radial kbins
        kx3d, ky3d, kz3d = np.meshgrid(kx, ky, kz, indexing="ij")
        k3d = np.sqrt(kx3d**2 + ky3d**2 + kz3d**2)

        whichbin = np.digitize(k3d.flat, kbins)
        ncount = np.bincount(whichbin)

        E_spectrum = np.zeros(len(ncount) - 1) # len(ncount) = N_tot/2

        for n in range(1, len(ncount)): # n< N+tot/2
            # Find out all the sampling frequency in kk that within [n*f_0, (n+1)*f_0]
            # and sum it up
            E_spectrum[n - 1] = np.sum(Kk.flat[whichbin == n]) / kmin

        k = 0.5 * (kbins[0 : N - 1] + kbins[1:N])
        E_spectrum = E_spectrum[1:N]

        # Fit the E(k)-k relation by Kolmogorov -5/3 law
        initialGuess = 0.05
        alpha, pcov = curve_fit(self.__kolmogorov, k, E_spectrum, initialGuess)
        
        del v_components, Kk, kx3d, ky3d, kz3d, k3d
        # return kmax, Emax, fittedDissipationRate, Eheating
        return k, E_spectrum, alpha

    def __getDissipationRate(self, alpha : float):
        fittedDissipationRate = (alpha[0])**(3/2)
        return fittedDissipationRate
    
    def __getHeatingRate(self, dissipationRate : float, rboxKpc : float):
        Eheating = dissipationRate*(2e33)*self.__M_g1(1.24*rboxKpc)[0]
        return Eheating

    def __fft_comp(self, v_component, rho): # r in kpc
        # Get the velocity field within the box
        u = v_component
        nx, ny, nz = u.shape

        # Get density weighting field
        avgRho = np.mean(rho)
        rhoWeighting = (rho/avgRho)**self.nindex_rho
        
        # do the FFTs -- note that since our data is real, there will be
        # too much information here.  fftn puts the positive freq terms in
        # the first half of the axes -- that's what we keep.  Our
        # normalization has an '8' to account for this clipping to one
        # octant.
        ru = np.fft.fftn(rhoWeighting * u)[
            0 : nx // 2 + 1, 0 : ny // 2 + 1, 0 : nz // 2 + 1
        ]
        ru = 8.0 * ru / (nx * ny * nz)

        return np.abs(ru)**2

    def __extractFieldValues(self, ds, rboxKpc, field):

        # Calculate nessary informations
        low = yt.YTArray([-rboxKpc, -rboxKpc, -rboxKpc], "kpc")
        dims = np.array([rboxKpc, rboxKpc, rboxKpc])*2

        # Extract all data points in ds and convert it from AMR to fixed grid
        cube = ds.covering_grid(self.maxLevel, left_edge=low, dims=dims, fields=[field])

        return cube[field].d


    def setDensityWeightingIndex(self, index : float):
        self.nindex_rho = index
        return self

    def setDataSeries(self, ds : yt.DatasetSeries):
        self.ds = ds
        return self

    def setBoxSize(self, rboxKpc):
        self.rboxKpc = rboxKpc
        return self

    def calculatePowerSpectrum(self):
        if (self.ds == None):
            raise ValueError("You should give a yt.DataSeries")
        if (self.rboxKpc == None):
            raise ValueError("Check your rboxKpc setting")
        velx = self.__extractFieldValues(self.ds, self.rboxKpc, ('gas', 'velocity_x'))
        vely = self.__extractFieldValues(self.ds, self.rboxKpc, ('gas', 'velocity_y'))
        velz = self.__extractFieldValues(self.ds, self.rboxKpc, ('gas', 'velocity_z'))
        rho = self.__extractFieldValues(self.ds, self.rboxKpc, ('gas', 'density'))
        self.k, self.Ek, self.alpha = self.__getVelocityPowerSpectrum([velx, vely, velz], rho, rboxKpc=self.rboxKpc)
        return self


    def plotPowerSpectrum(self, ax : plt.Axes):
        if (self.Ek is None):
            raise RuntimeError("You should excute calculatePowerSpectrum() at first")
        time = np.round(self.ds.current_time.in_units('Gyr'), 2)
        title    = 't=%.1fGyr, l=%dkpc' %(time, self.rboxKpc)
        ax.set(
            xlabel=r"$k$" + "   " + r"$1/kpc$",
            ylabel=r"$E(k)$" + "    " +  r"$cm^3/s^2$",
            title=title
        )
        ax.loglog(self.k*self.kpc2cm, self.Ek)
        ax.loglog(self.k*self.kpc2cm, self.__kolmogorov(self.k, self.alpha[0]), ls=":", color="0.5")
    
        
    def getDissipationRate(self):
        if (self.Ek is None):
            raise RuntimeError("You should excute calculatePowerSpectrum() at first")
        dissipationRate = self.__getDissipationRate(self.alpha)
        heatingRate = self.__getHeatingRate(dissipationRate, self.rboxKpc)
        dic = {
            'l_kpc' : self.rboxKpc,
            'dissipation_rate' : dissipationRate,
            'turb_heating_rate' : heatingRate
        }
        return dic
    
