pro decomposeVel, dir=dir, fnum=fnum, pltfile=pltfile, $
                  nx1=nx1, nx2=nx2, nx3=nx3, out=out, $
                  ecrmin=ecrmin, nr=nr

if(not keyword_set(dir)) then $
  dir = 'cool_agn_cold_eff1e-3_p15_accreteTracers'
if(not keyword_set(fnum)) then $
  fnum = '0100'
if(not keyword_set(nx1)) then $
  nx1 = 64
if(not keyword_set(nx2)) then $
  nx2 = 64
if(not keyword_set(nx3)) then $
  nx3 = 64
if(not keyword_set(nr)) then $
  nr = 50 ; the radius within which to compute Ekin in units of cells

; If ecrmin is set, this is the threshold of ecr to distinguish regions
; between the bubbles and the ambient medium. This is used for summarizing Ekin 

kpc = 3.08568025d21
Gyr = 3.15576d16

;-------------------------------------------------------------
; Start reading files
;-------------------------------------------------------------

basedir = '/homes/hsyang/workspace/clusterHBINFW/'
if(keyword_set(pltfile)) then begin
  chkfile = basedir+dir+'/clusterHBI_hdf5_plt_cnt_'+fnum
endif else begin 
  chkfile = basedir+dir+'/clusterHBI_hdf5_chk_'+fnum
endelse
oudir = './data/'+dir
isdir = file_test(oudir)
if(not isdir) then file_mkdir, oudir
print, 'Input file: '+strtrim(chkfile,2)

; read velocity data
vx1 = loaddata(chkfile,'velx',xcoords=xx,ycoords=yy,zcoords=zz,time=tt,$
               sample=sample)
vx2 = loaddata(chkfile,'vely',sample=sample)
vx3 = loaddata(chkfile,'velz',sample=sample)
rho = loaddata(chkfile,'dens',sample=sample)
if(keyword_set(ecrmin)) then begin
  ecr = loaddata(chkfile,'cray',sample=sample)
  ecr = ecr*rho
endif

n = size(vx1)
nx = n[1]
ny = n[2]
nz = n[3]
xx = xx / kpc
yy = yy / kpc
zz = zz / kpc
dx1 = xx[1]-xx[0]
dx2 = yy[1]-yy[0]
dx3 = zz[1]-zz[0]
dV = dx1*dx2*dx3*kpc^3.
print, 'dV = ', dV

; extract data
il = nx/2 - nx1/2
ir = nx/2 + nx1/2 - 1
jl = ny/2 - nx2/2
jr = ny/2 + nx2/2 - 1
kl = nz/2 - nx3/2
kr = nz/2 + nx3/2 - 1
vx1 = vx1[il:ir,jl:jr,kl:kr]
vx2 = vx2[il:ir,jl:jr,kl:kr]
vx3 = vx3[il:ir,jl:jr,kl:kr]
rho = rho[il:ir,jl:jr,kl:kr]
print, 'vx data range = ', min(vx1), max(vx1)
print, 'vy data range = ', min(vx2), max(vx2)
print, 'vz data range = ', min(vx3), max(vx3)
print, 'rho data range = ', min(rho), max(rho)
if(keyword_set(ecrmin)) then begin
  ecr = ecr[il:ir,jl:jr,kl:kr]
  print, 'ecr data range = ', min(ecr), max(ecr)
endif

;-------------------------------------------------------------
; Start performing FFTs
;-------------------------------------------------------------

print,'Defining KE output array'
keout=dblarr(7)

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

;-------------------------------------------------------------
; Compute kinetic energy
;-------------------------------------------------------------

print,' - Computing Kinetic Energy'

if(keyword_set(nr)) then begin
  inradius = replicate(0, nx1, nx2, nx3)
  print,'   - select region within the chosen radius'
  for i = 0, nx1-1L do begin
  for j = 0, nx2-1L do begin
  for k = 0, nx3-1L do begin
    ii = i - nx1/2
    jj = j - nx2/2
    kk = k - nx3/2
    ir = sqrt(ii*ii + jj*jj + kk*kk)
    if (ir le nr) then $
      inradius(i, j, k) = 1
  end
  end
  end
endif

print,'   - delineate bub and amb region'
if(keyword_set(ecrmin)) then begin
  if(keyword_set(nr)) then begin
    bub = where(ecr ge ecrmin and inradius eq 1)
    amb = where(ecr lt ecrmin and inradius eq 1)
  endif else begin
    bub = where(ecr ge ecrmin)
    amb = where(ecr lt ecrmin)
  endelse
endif else begin
  if(keyword_set(nr)) then begin
    bub = where(inradius eq 1)
    amb = where(inradius eq 1)
  endif 
endelse

print,'   - computing 0.5 rho v^2 for bubble region'
keout(0) = tt/Gyr

keout(1) = total(0.5*rho(bub)*( vx1c(bub)*vx1c(bub) + vx2c(bub)*vx2c(bub) + vx3c(bub)*vx3c(bub) ))*dV

keout(2) = total(0.5*rho(bub)*( vx1i(bub)*vx1i(bub) + vx2i(bub)*vx2i(bub) + vx3i(bub)*vx3i(bub) ))*dV

keout(3) = total(rho(bub)*( vx1c(bub)*vx1i(bub) + vx2c(bub)*vx2i(bub) + vx3c(bub)*vx3i(bub) ))*dV

print,'   - computing 0.5 rho v^2 for ambient region'

keout(4) = total(0.5*rho(amb)*( vx1c(amb)*vx1c(amb) + vx2c(amb)*vx2c(amb) + vx3c(amb)*vx3c(amb) ))*dV

keout(5) = total(0.5*rho(amb)*( vx1i(amb)*vx1i(amb) + vx2i(amb)*vx2i(amb) + vx3i(amb)*vx3i(amb) ))*dV

keout(6) = total(rho(amb)*( vx1c(amb)*vx1i(amb) + vx2c(amb)*vx2i(amb) + vx3c(amb)*vx3i(amb) ))*dV

print, 'keout = ', keout

print,' - Write to output file'
outfile = oudir+'/kinetic_energy.dat'
isfile = file_test(outfile)
if(isfile) then begin
  openw,1,outfile,/append
endif else begin
  openw, 1, outfile
  printf, 1, '# Time(Gyr) Ec,bub Ei,bub Eci,bub Ec,amb Ei,amb Eci,amb'
endelse
printf,1,keout,format='(7e12.4)'
close,1

;-------------------------------------------------------------
; Dumping velocity data
;-------------------------------------------------------------

if(keyword_set(out)) then begin

openw, 1, oudir+'/vcx'+fnum+'.dat'
openw, 2, oudir+'/vcy'+fnum+'.dat'
openw, 3, oudir+'/vcz'+fnum+'.dat'
openw, 4, oudir+'/vix'+fnum+'.dat'
openw, 5, oudir+'/viy'+fnum+'.dat'
openw, 6, oudir+'/viz'+fnum+'.dat'
writeu, 1, vx1c
writeu, 2, vx2c
writeu, 3, vx3c
writeu, 4, vx1i
writeu, 5, vx2i
writeu, 6, vx3i
close, 1
close, 2
close, 3
close, 4
close, 5
close, 6

endif

print,' - DONE'

end
