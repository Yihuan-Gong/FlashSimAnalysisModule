import yt

class Constants:
    kpc = float(yt.YTArray(1, 'kpc').in_cgs().d)
    solarMass = 1.9891e33
    Myr = 3.1557e13
    yr = 3.1557e7
