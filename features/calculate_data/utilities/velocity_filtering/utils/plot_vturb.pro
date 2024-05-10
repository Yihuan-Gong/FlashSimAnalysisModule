pro plot_vturb, indir=indir, invar=invar, fnum=fnum, ng=ng, dx=dx, dir=dir, $
    rev_color=rev_color, title=title, drange=drange, double=double, log=log, $
    cltable=cltable, outfile=outfile

if(not keyword_set(invar)) then $
  invar = 'turb'
if(not keyword_set(ng)) then $
  ng = 64
if(not keyword_set(dx)) then $
  dx = 2.
if(not keyword_set(dir)) then $
  dir = 'z'
if(not keyword_set(title)) then begin
  dt = 0.02 ; Gyr
  time = dt*fnum
  title = 't = '+strtrim(string(time,format='(F5.2)'), 2)+' Gyr'
endif
if(not keyword_set(cltable)) then $
  cltable = 13

if(dir eq 'all') then begin
  if(keyword_set(double)) then begin
    datax = dblarr(ng, ng, ng)
  endif else begin
    datax = fltarr(ng, ng, ng)
  endelse
  filename = indir+'/'+invar+'x'+fnum+'.dat'
  openr, 3, filename
  readu, 3, datax
  close, 3
  datax = reform(datax[ng/2,*,*])
  datax = datax / 1.e5 

  if(keyword_set(double)) then begin
    datay = dblarr(ng, ng, ng)
  endif else begin
    datay = fltarr(ng, ng, ng)
  endelse
  filename = indir+'/'+invar+'y'+fnum+'.dat'
  openr, 3, filename
  readu, 3, datay
  close, 3
  datay = reform(datay[ng/2,*,*])
  datay = datay / 1.e5

  if(keyword_set(double)) then begin
    dataz = dblarr(ng, ng, ng)
  endif else begin
    dataz = fltarr(ng, ng, ng)
  endelse
  filename = indir+'/'+invar+'z'+fnum+'.dat'
  openr, 3, filename
  readu, 3, dataz
  close, 3
  dataz = reform(dataz[ng/2,*,*])
  dataz = dataz / 1.e5

  data = sqrt(datax^2. + datay^2. + dataz^2.)
  undefine, datax
  undefine, datay 
  undefine, dataz
  filename = indir+'/'+invar+'all'+fnum+'.dat'

endif else begin
  if(keyword_set(double)) then begin
    data = dblarr(ng, ng, ng)
  endif else begin
    data = fltarr(ng, ng, ng)
  endelse
  filename = indir+'/'+invar+dir+fnum+'.dat'
  openr, 3, filename
  readu, 3, data
  close, 3
  data = reform(data[ng/2,*,*])
  data = data / 1.e5
endelse

dmin = min(data)
dmax = max(data)
print, 'Read in file ', strtrim(filename,2)
print, 'min(data), max(data) in km/s = ', dmin, dmax
if(keyword_set(drange)) then begin
  cut = where(data lt drange[0])
  if(cut[0] ne -1) then $
    data[cut] = drange[0]
  cut = where(data gt drange[1])
  if(cut[0] ne -1) then $
    data[cut] = drange[1]
endif
dmin = min(data)
dmax = max(data)
print, 'After limiting extrema: min(data), max(data) in km/s = ', dmin, dmax
dmin = drange[0]
dmax = drange[1]
if(keyword_set(log)) then begin
  data = alog10(data)
  dmin = min(data)
  dmax = max(data)
  print, 'After taking log10: min(data), max(data) in km/s = ', dmin, dmax
  dmin = alog10(drange[0])
  dmax = alog10(drange[1])
endif

ng2  = ng/2
xmin = -ng2*dx
xmax =  ng2*dx
ymin = xmin
ymax = xmax



if(keyword_set(outfile)) then begin
  filename = indir+'/'+outfile
endif else begin
  filename = filename+'.eps'
endelse
aspect = 1
xlpos = 0.1
xrpos = 0.78
ylpos = 0.12
yrpos = 0.9
xsize = 5
ysize = xsize*0.85*aspect
page_width = xsize+0.5
page_height = ysize+0.5
xoffset = (page_width-xsize)*0.5
yoffset = (page_height-ysize)*0.5
set_plot, 'ps'
setdots, 10, /fill

device, bits_per_pixel=8, color=1, filename=filename, /portrait
device, xsize=xsize, ysize=ysize, $
        xoffset=xoffset, yoffset=yoffset, /inches, /encapsulated
title = '!6'+title
thickness = 2
charthick = thickness
charsize  = 1.
symsize   = 0.2
!p.thick = thickness
!x.thick = thickness
!y.thick = thickness
!p.charthick = thickness
!p.charsize  = charsize

loadct, cltable
if(keyword_set(rev_color)) then begin
  reverse_ct
  textcolor = 255
endif else begin
  textcolor = 0
endelse



data = bytscl(data, min=dmin, max=dmax)
tv, data, xlpos, ylpos, xsize=xrpos-xlpos, ysize=yrpos-ylpos, /normal

plot, [xmin, xmax], [ymin, ymax], pos=[xlpos, ylpos, xrpos, yrpos], $
      xrange=[xmin,xmax], xstyle=1, ystyle=1, /nodata, /noerase, $
      xtitle=xtitle, ytitle=ytitle, title=title, $
      charthick=charthick, charsize=charsize, color=textcolor

position = [xrpos, ylpos, xrpos+0.04, yrpos]
colorbar, ncolors=256, min=dmin, max=dmax, position=position, $
          vertical=1, right=1, divisions=6, charsize=charsize*0.8, $
          color=textcolor, /pscolor



if(keyword_set(out)) then begin
  device, /close
  set_plot, 'X'
endif

end

