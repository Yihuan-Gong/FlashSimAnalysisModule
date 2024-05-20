kpc = 3.08568025d21
Gyr = 3.15576d16

print,'Defining KE output array'
keout=dblarr(7)

; Ensure that nx1, nx2, nx3 are even
if (nx1 mod 2) ne 0 then nx1 = nx1 + 1
if (nx2 mod 2) ne 0 then nx2 = nx2 + 1
if (nx3 mod 2) ne 0 then nx3 = nx3 + 1

print,'Defining 1-d kx,ky,kz'
dkx1 = 1.0/(nx1*dx1/kpc)
dkx2 = 1.0/(nx2*dx2/kpc)
dkx3 = 1.0/(nx3*dx3/kpc)

x = findgen((nx1-1)/2)+1
kx1=[0.0,x,nx1/2,-nx1/2+x]*dkx1

y = findgen((nx2-1)/2)+1
kx2=[0.0,y,nx2/2,-nx2/2+y]*dkx2

z = findgen((nx3-1)/2)+1
kx3=[0.0,z,nx3/2,-nx3/2+z]*dkx3

print,'Putting k vectors into 3-d arrays'

kx13d=rebin(kx1,nx1,nx2,nx3)
kx23d=rebin(kx2,nx2,nx1,nx3)
kx33d=rebin(kx3,nx3,nx1,nx2)
kx23d=transpose(kx23d,[1,0,2])
kx33d=transpose(kx33d,[1,2,0])
ksq=kx13d^2+kx23d^2+kx33d^2+1e-10

print,' - performing Helmholtz decomposition'

print,'   - taking FFTs of velocity arrays'
vx1_ft = fft(vx1)
vx2_ft = fft(vx2)
vx3_ft = fft(vx3)

print,'   - allocating complex arrays for phi and vc_ft'
phik = complexarr(nx1,nx2,nx3)
vx1c_ft = complexarr(nx1,nx2,nx3)
vx2c_ft = complexarr(nx1,nx2,nx3)
vx3c_ft = complexarr(nx1,nx2,nx3)
   
print,'   - computing phik'
phik=(kx13d*vx1_ft + kx23d*vx2_ft + kx33d*vx3_ft)/ksq

print,'   - computing vxc_ft'
vx1c_ft = kx13d*phik
vx2c_ft = kx23d*phik
vx3c_ft = kx33d*phik

print,'   - deallocating phi' 
phik=0

print,'   - computing vxc with inverse FFT'
vx1c = real_part(fft(vx1c_ft,/inverse))
vx2c = real_part(fft(vx2c_ft,/inverse))
vx3c = real_part(fft(vx3c_ft,/inverse))

print,'   - deallocating vxc_ft arrays'
vx1c_ft=0
vx2c_ft=0
vx3c_ft=0

print,'   - computing vxi'
vx1i = vx1 - vx1c
vx2i = vx2 - vx2c
vx3i = vx3 - vx3c

print, 'vxc data range = ', min(vx1c), max(vx1c)
print, 'vyc data range = ', min(vx2c), max(vx2c)
print, 'vzc data range = ', min(vx3c), max(vx3c)
print, 'vxi data range = ', min(vx1i), max(vx1i)
print, 'vyi data range = ', min(vx2i), max(vx2i)
print, 'vzi data range = ', min(vx3i), max(vx3i)

