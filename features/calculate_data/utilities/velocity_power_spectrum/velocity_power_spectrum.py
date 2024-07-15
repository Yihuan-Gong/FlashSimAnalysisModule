from .models import VelocityPowerSpectrumInputModel
from ...utilities.velocity_filtering import (
    VelocityFiltering,
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData3dReturnModel,
    VelocityFilteringField
)

from typing import Iterable
import astropy.units as u
import numpy as np


class VelocityPowerSpectrum:
    
    def getPowerSpectrum(
        self, 
        input: VelocityPowerSpectrumInputModel
    ) -> tuple[u.Quantity, u.Quantity]:
        '''
            rho is required if rhoIndex != 0
            
            Return: (k, E_spectrum)
        '''
        return self.__getVelocityPowerSpectrum(
            v_components=[input.velx, input.vely, input.velz],
            rboxKpc=input.rbox.to("kpc").value,
            cellSize=input.cellSize,
            rhoIndex=input.rhoIndex,
            rho=input.rho
        )
    
    
    def getPowerSpectrumByVelocityFilteringData3d(
        self,
        field: VelocityFilteringField,
        velocityData3d: VelocityFilteringData3dReturnModel
    ):
        fieldBaseName = f"{field}".split(".")[-1].removesuffix("total")
        return self.getPowerSpectrum(VelocityPowerSpectrumInputModel(
                velx=getattr(velocityData3d, f"{fieldBaseName}x"),
                vely=getattr(velocityData3d, f"{fieldBaseName}y"),
                velz=getattr(velocityData3d, f"{fieldBaseName}z"),
                cellSize=velocityData3d.xAxis[1] - velocityData3d.xAxis[0],
                rbox=(velocityData3d.xAxis[-1] - velocityData3d.xAxis[0])/2
            )
        )
    

    
    def __getVelocityPowerSpectrum(
        self, 
        v_components: Iterable[u.Quantity], 
        rboxKpc: float, 
        cellSize: u.Quantity, 
        rhoIndex = 0, 
        rho = None
    ): 
        # nx = ny = nz = int(2*(u.Quantity(rboxKpc, "kpc")/cellSize))
        (nx, ny, nz) = v_components[0].shape
        rboxCm = rboxKpc*u.Quantity(1, "kpc").cgs.value
        dxCm = cellSize.cgs.value

        # Creat the space to put 3D KE power spectrum
        Kk = np.zeros((nx // 2 + 1, ny // 2 + 1, nz // 2 + 1))

        for v_component in v_components:

            Kk += 0.5 * self.__fft_comp(v_component, rhoIndex, rho)

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

        del v_components, Kk, kx3d, ky3d, kz3d, k3d
        return u.Quantity(k, "1/cm"), u.Quantity(E_spectrum, "cm**3/s**2")


    def __fft_comp(
        self, 
        v_component: u.Quantity, 
        rhoIndex: float = 0,
        rho: u.Quantity = None
    ):  
        # r in kpc
        # Get the velocity field within the box
        u = v_component
        nx, ny, nz = u.shape

        # Get density weighting field
        if (rhoIndex == 0):
            rhoWeighting = 1
        else:
            avgRho = np.mean(rho)
            rhoWeighting = (rho/avgRho)**rhoIndex
        
        # do the FFTs -- note that since our data is real, there will be
        # too much information here.  fftn puts the positive freq terms in
        # the first half of the axes -- that's what we keep.  Our
        # normalization has an '8' to account for this clipping to one
        # octant.
        ru = np.fft.fftn(rhoWeighting * u.cgs.value)[
            0 : nx // 2 + 1, 0 : ny // 2 + 1, 0 : nz // 2 + 1
        ]
        ru = 8.0 * ru / (nx * ny * nz)

        return np.abs(ru)**2


