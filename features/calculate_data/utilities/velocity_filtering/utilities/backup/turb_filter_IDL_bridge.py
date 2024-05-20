import numpy as np
import yt
import matplotlib.pyplot as plt
import mirpyidl as idl
import time


def extract_vel_comp(ds, iu, level):

    # Calculate nessary informations
    ref = 2 ** level
    low = ds.domain_left_edge
    dims = ds.domain_dimensions * ref

    # Extract all data points in ds and convert it from AMR to fixed grid
    cube = ds.covering_grid(level, left_edge=low, dims=dims, fields=[iu])

    # The velocity field
    u = cube[iu].d

    return u


def extract_density(ds, level):

    # Calculate nessary informations
    ref = 2 ** level
    low = ds.domain_left_edge
    dims = ds.domain_dimensions * ref

    # Extract all data points in ds and convert it from AMR to fixed grid
    cube = ds.covering_grid(level, left_edge=low, dims=dims, fields=('gas', 'density'))

    # The velocity field
    rho = cube[('gas', 'density')].d

    return rho


def doit(ds, v_components, turb_v_components, level=0, title='power spectrum', figname='power_spec.png'):

    # a FFT operates on uniformly gridded data.  We'll use the yt
    # covering grid for this.

    ref = 2 ** level
    low = ds.domain_left_edge
    dims = ds.domain_dimensions * ref

    nx, ny, nz = dims

    Kk = np.zeros((nx // 2 + 1, ny // 2 + 1, nz // 2 + 1))

    #############
    # Set plot  #
    #############
    fig, ax = plt.subplots(figsize=(8,6))
    ax.set(
        xlabel=r"$k$",
        ylabel=r"$E(k)dk$",
        title=title
    )


    for v_field in [v_components, turb_v_components]:

        for v_component in v_field:
            Kk += 0.5 * fft_comp(ds, v_component)

        # wavenumbers
        L = (ds.domain_right_edge - ds.domain_left_edge).d

        # If d is bot specified in f = fft.rfftfreq(), then f should be 
        # normalized by T_0/N_tot
        kx = np.fft.rfftfreq(nx) * nx / L[0]
        ky = np.fft.rfftfreq(ny) * ny / L[1]
        kz = np.fft.rfftfreq(nz) * nz / L[2]

        # physical limits to the wavenumbers
        kmin = np.min(1.0 / L)  # f_0
        kmax = np.min(0.5 * dims / L)  # Nyquist frequency = 0.5*N_tot*f_0

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
            # E_spectrum[n - 1] = np.mean(Kk.flat[whichbin == n])

        k = 0.5 * (kbins[0 : N - 1] + kbins[1:N])
        E_spectrum = E_spectrum[1:N]

        index = np.argmax(E_spectrum)
        kmax = k[index]
        Emax = E_spectrum[index]
        

        # Plot velocity and turbulence velocity field
        if v_field is v_components:
            
            # Fit E(k) with constant slope in log space
            # The fited equation should be
            # logE(k) = m*logk + b
            logk = np.log10(k)
            logE_spectrum = np.log10(E_spectrum)
            m = -5/3 # Slope of E(k) 
            b = np.mean(logE_spectrum - m*logk) # Intercept of E(k)
            E_fitted = (10**b)*(k**m) # Exponential form of logE(k) = m*logk + b
            
            ax.loglog(k, E_spectrum, label='velocity') # 'velocity'
            ax.loglog(k, E_fitted, ls=":", color="0.5", label='Komologrov')
        else:
            ax.loglog(k, E_spectrum, label='turbulence')  # 'turbulence'

        # Reset kk
        Kk = np.zeros((nx // 2 + 1, ny // 2 + 1, nz // 2 + 1))
    

    ax.legend()
    fig.savefig(figname)


def fft_comp(ds, v_component):

    nx, ny, nz = v_component.shape

    # do the FFTs -- note that since our data is real, there will be
    # too much information here.  fftn puts the positive freq terms in
    # the first half of the axes -- that's what we keep.  Our
    # normalization has an '8' to account for this clipping to one
    # octant.
    ru = np.fft.fftn(v_component)[
        0 : nx // 2 + 1, 0 : ny // 2 + 1, 0 : nz // 2 + 1
    ]
    ru = 8.0 * ru / (nx * ny * nz)

    return np.abs(ru)**2


def get_turb_vel_field(ds, level):

    # Calculate array length in each dimension
    n = 128*2**level

    # Extract velocity field
    velx = extract_vel_comp(ds, ('gas', 'velocity_x'), level=level).astype('float32')
    vely = extract_vel_comp(ds, ('gas', 'velocity_y'), level=level).astype('float32')
    velz = extract_vel_comp(ds, ('gas', 'velocity_z'), level=level).astype('float32')

    # Reshape from (128, 128, 128) to (128**3)
    velx_flat = velx.reshape(n**3, order='F')
    vely_flat = vely.reshape(n**3, order='F')
    velz_flat = velz.reshape(n**3, order='F')

    # # Change data type from float64 to float32
    # velx_flat = velx_flat.astype('float32')
    # vely_flat = vely_flat.astype('float32')
    # velz_flat = velz_flat.astype('float32')

    # velocity field
    v_component = [velx, vely, velz]
    turb_v_component = []
    skewness_component = []
    scale_component = []


    # Iterate through all 3 component
    for vel in [velx_flat, vely_flat, velz_flat]:

        # Run IDL script
        try:
            # Pass the 1D array to IDL
            idl.setVariable('n', n)
            idl.setVariable('vel1D', vel)

            # Reshape to 3D array
            idl.execute("vel = reform(vel1D, n, n, n)")

            # Run IDL filering script
            idl.execute(" \
                r2=63    &\
                r1=2    &\
                turbo=fltarr(n,n,n)    &\
                scale=fltarr(n,n,n)    &\
                sk=fltarr(n,n,n)    &\
                scale(*,*,*)= 0.    &\
                eps=0.1    &\
                nk=8    &\
                epssk=1.    &\
                drr=1.    &\
                meanv = smooth(vel,nk,/EDGE_TRUNCATE)   &\
                sc = abs((vel-meanv)/vel)   &\
                kernel=MAKE_ARRAY(nk,nk,nk, /float, value =1.)   &\
                kernel(0,*,*) = 0.   &\
                kernel(*,0,*) = 0.   &\
                kernel(*,*,0) = 0.   &\
                kernel(nk-1,*,*) = 0.   &\
                kernel(*,nk-1,*) = 0.   &\
                kernel(*,*,nk-1) = 0.   &\
                sk=convol((vel-meanv)^2,kernel,/edge_truncate,/normalize)   &\
                sk=meanv^3/float(sk^1.5)   &\
                sc1 = 0    &\
                for r=r1,r2,drr do begin   &\
                    print,r   &\
                    width = 2.*r+1    &\
                    meanv = smooth(vel,width,/EDGE_TRUNCATE)   &\
                    sc = abs((vel-meanv)/vel)    &\
                    skm=smooth(sk,width,/EDGE_TRUNCATE)    &\
                    ibox=where((abs(sc-sc1)/float(sc1) lt eps or abs(skm) gt epssk) and scale eq 0.,nn)   &\
                    if nn gt 0 then begin   &\
                        turbo(ibox)=vel(ibox)-meanv(ibox)    &\
                        scale(ibox) = float(r+0.01)    &\
                    endif   &\
                    sc1=sc   &\
                endfor   \
            ")
        
        except idl.IdlArithmeticError:
            pass

        # Get result back from IDL
        vel_turb = idl.getVariable('turbo')
        scale    = idl.getVariable('scale')
        skewness = idl.getVariable('sk')

        # Convert to python format
        vel_turb = vel_turb.transpose()
        scale    = scale.transpose()

        # Append to turb_v_component
        turb_v_component.append(vel_turb)
        scale_component.append(scale)
        skewness_component.append(skewness)

    return v_component, turb_v_component, scale_component, skewness_component


'''
    Main Function
'''
# Set level
level = 3
print ('-------- Level %d ---------' %level)

# Load data
ds = yt.load('../../../data/sloshing/test2/perseus_merger_hdf5_plt_cnt_0400')

# Turb velocity field filtering
start_time = time.time()
v_component, turb_v_component, scale_component, skewness_component = get_turb_vel_field(ds, level)
print("--- %.2f seconds for filtering ---" % (time.time() - start_time))

# Save the filtered velocity field
start_time = time.time()
np.save('test/400_level%d/turb_x.npy'%level, turb_v_component[0])
np.save('test/400_level%d/turb_y.npy'%level, turb_v_component[1])
np.save('test/400_level%d/turb_z.npy'%level, turb_v_component[2])


print("--- %.2f seconds for saving ---" % (time.time() - start_time))

# Plot velocity spectrum
start_time = time.time()
doit(
    ds = ds, 
    v_components = v_component, 
    turb_v_components = turb_v_component, 
    level = level, 
    title = '10 iterations, t=2.2Gyr, level=%d'%level,
    figname='test/level%d.png'%level
)
print("--- %.2f seconds for spectrum ---" % (time.time() - start_time))
