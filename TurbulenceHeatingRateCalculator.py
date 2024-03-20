import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
import os
from scipy.integrate import quad, dblquad
from scipy.optimize import curve_fit
from typing import Tuple
from python.modules.FieldAdder import FieldAdder


class TurbulenceHeatingRateCalculator:
    def __init__(self) -> None:
        self.kpc2cm = 3.08567758e21
        
    
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
    
    def __getVelocityPowerSpectrum(self, ds, v_components, level : int=4, LboxKpc : float=75): # L in kpc
        # Length of sample region
        LboxCm = LboxKpc*self.kpc2cm  # in cm
        L = np.array([2*LboxCm, 2*LboxCm, 2*LboxCm])

        # Total length of the simulation
        L_tot = (ds.domain_right_edge - ds.domain_left_edge).d

        # a FFT operates on uniformly gridded data.  We'll use the yt
        # covering grid for this.

        ref = 2 ** level
        dims = ds.domain_dimensions * ref

        # Grid size
        dx = L_tot[0]/dims[0]
        dy = L_tot[1]/dims[1]
        dz = L_tot[2]/dims[2]
        grid_size = np.array([dx, dy, dz])

        # Number of sample grid in each side.
        # nx, ny, nz should be even
        nx = int((L[0]/dx//2)*2)
        ny = int((L[1]/dy//2)*2)
        nz = int((L[2]/dz//2)*2)
        sample_dims = np.array([nx, ny, nz])

        # Modify L to the nearest integer grid
        L = grid_size * sample_dims

        # Creat the space to put 3D KE power spectrum
        Kk = np.zeros((nx // 2 + 1, ny // 2 + 1, nz // 2 + 1))

        for v_component in v_components:

            Kk += 0.5 * self.__fft_comp(
                v_component, dims, sample_dims
            )

        # If d is bot specified in f = fft.rfftfreq(), then f should be 
        # normalized by N_tot/T_0
        kx = np.fft.rfftfreq(nx) * nx / L[0]
        ky = np.fft.rfftfreq(ny) * ny / L[1]
        kz = np.fft.rfftfreq(nz) * nz / L[2]

        # physical limits to the wavenumbers
        kmin = np.min(1.0 / L)  # f_0
        kmax = np.min(0.5 * sample_dims / L)  # Nyquist frequency = 0.5*N_tot*f_0

        kbins = np.arange(kmin, kmax, kmin)
        N = len(kbins) # should be N = N_tot/2

        # bin the Fourier KE into radial kbins
        kx3d, ky3d, kz3d = np.meshgrid(kx, ky, kz, indexing="ij")
        k = np.sqrt(kx3d**2 + ky3d**2 + kz3d**2)

        whichbin = np.digitize(k.flat, kbins)
        ncount = np.bincount(whichbin)

        E_spectrum = np.zeros(len(ncount) - 1) # len(ncount) = N_tot/2

        for n in range(1, len(ncount)): # n< N+tot/2
            # Find out all the sampling frequency in kk that within [n*f_0, (n+1)*f_0]
            # and sum it up
            E_spectrum[n - 1] = np.sum(Kk.flat[whichbin == n])

        k = 0.5 * (kbins[0 : N - 1] + kbins[1:N])
        E_spectrum = E_spectrum[1:N]

        index = np.argmax(E_spectrum)
        kmax = k[index]
        Emax = E_spectrum[index]

        # The time of this simulation
        time = np.round(ds.current_time.in_units('Gyr'),1)

        # The title and the filename of the plot
        title    = 't=%.1fGyr, l=%dkpc' %(time, LboxKpc)
        # filename = 'box_power_spectrum/%dMyr/%dMyr_%dkpc.png' %(int(time*1000), int(time*1000), l0)
        
        # Create directory to put .png file if needed
        # dir = 'box_power_spectrum/%dMyr/' %(int(time*1000))
        # if not os.path.isdir(dir):
        #     os.mkdir(dir)

        # Fit the E(k)-k relation by Kolmogorov -5/3 law
        initialGuess = 0.05
        alpha, pcov = curve_fit(self.__kolmogorov, k, E_spectrum, initialGuess)
        

        # Plot and save
        fig, ax = plt.subplots(figsize=(8,6))
        ax.set(
            xlabel=r"$k$",
            ylabel=r"$E(k)$",
            title=title
        )
        ax.loglog(k, E_spectrum)
        ax.loglog(k, self.__kolmogorov(k, alpha[0]), ls=":", color="0.5")
        # fig.savefig(filename)

        del v_components, Kk, kx3d, ky3d, kz3d
        # return kmax, Emax, fittedDissipationRate, Eheating
        return k, E_spectrum, alpha
    


    def __getDissipationRate(self, alpha : float, LboxKpc : float):
        LboxCm = LboxKpc*self.kpc2cm
        dk = 1/(2*LboxCm)
        fittedDissipationRate = (alpha[0]/dk)**(3/2)
        return fittedDissipationRate
    
    def __getHeatingRate(self, dissipationRate : float, LboxKpc : float):
        Eheating = dissipationRate*(2e33)*self.__M_g1(1.24*LboxKpc)[0]
        return Eheating


    def __fft_comp(self, v_component, delta, sample_dims): # r in kpc
        # Calculate start and the end index for sampling
        x_start = int(delta[0]/2 - sample_dims[0]/2)
        y_start = int(delta[1]/2 - sample_dims[1]/2)
        z_start = int(delta[2]/2 - sample_dims[2]/2)
        x_end = int(delta[0]/2 + sample_dims[0]/2)
        y_end = int(delta[1]/2 + sample_dims[1]/2)
        z_end = int(delta[2]/2 + sample_dims[2]/2)

        # Get the velocity field within the box
        u = v_component[x_start:x_end, y_start:y_end, z_start:z_end]

        # nx, ny, nz = rho.shape
        nx, ny, nz = u.shape

        # do the FFTs -- note that since our data is real, there will be
        # too much information here.  fftn puts the positive freq terms in
        # the first half of the axes -- that's what we keep.  Our
        # normalization has an '8' to account for this clipping to one
        # octant.
        ru = np.fft.fftn(u)[
            0 : nx // 2 + 1, 0 : ny // 2 + 1, 0 : nz // 2 + 1
        ]
        ru = 8.0 * ru / (nx * ny * nz)

        return np.abs(ru)**2


    def __extract_vel_comp(self, ds, iu, level):

        # Calculate nessary informations
        ref = 2 ** level
        low = ds.domain_left_edge
        dims = ds.domain_dimensions * ref

        # Extract all data points in ds and convert it from AMR to fixed grid
        cube = ds.covering_grid(level, left_edge=low, dims=dims, fields=[iu])

        # The velocity field
        u = cube[iu].d

        del cube
        return u


    # Main Function:
    def boxPowerSpectrum(self, ds, LboxKpc : float, level : int):

        # Simulation time of the data
        time = np.round(ds.current_time.in_units('Gyr'),1)

        # Extract velocity field
        velx = self.__extract_vel_comp(ds, ('gas', 'velocity_x'), level=level)
        vely = self.__extract_vel_comp(ds, ('gas', 'velocity_y'), level=level)
        velz = self.__extract_vel_comp(ds, ('gas', 'velocity_z'), level=level)

        # Ekdk = alpha*k^(-5/3)
        k, Ekdk, alpha = self.__getVelocityPowerSpectrum(ds, [velx, vely, velz], level=level, LboxKpc=LboxKpc)
        dissipationRate = self.__getDissipationRate(alpha, LboxKpc)
        heatingRate = self.__getHeatingRate(dissipationRate, LboxKpc)

        # Initialization
        df = {
            'l_kpc':[],
            'dissipation_rate':[],
            'turb_heating_rate':[]
        }
        df = pd.DataFrame(df)
        df = df.append({
            'l_kpc':LboxKpc,
            'dissipation_rate':dissipationRate,
            'turb_heating_rate':heatingRate
        }, ignore_index=True)

        return df
        # Save the output data
        # df.to_csv('./heating_cooling_data_csv/turb_heating_rate_in_box_%dMyr.csv'%int(time*1000), index=False)
    
