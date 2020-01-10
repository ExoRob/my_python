import numpy as np
import my_constants as myc


def rebin_arrays(a, binsize, method="mean"):
    a = np.asarray(a)

    # print a
    # print a.size
    # print binsize

    cut = a.size % binsize

    if method == "mean":
        abin = a[cut:].reshape(a.size // binsize, binsize).mean(axis=1)

    return abin


def md2r(md, d):
    r = np.sqrt(md) * d * myc.PC / myc.RS

    return r


def mag2lum(mag):
    return 10. ** (-mag / 2.5)


def phase_fold(in_time, in_flux, period, tt0):
    foldtimes = ((in_time-tt0+period/2.0) / period) % 1

    phase, phase_flux = zip(*sorted(zip(foldtimes, in_flux)))
    
    return np.asarray(phase), np.asarray(phase_flux)


def running_sigma_clip(data, ax, ef, usig=3, lsig=10, binsize=10):
    import numpy as np
    #
    # Sigma clipping (running): find local outliers
    #
    data_clipped = []
    ax_clipped, err = [], []
    upperlist = []
    lowerlist = []
    i = 0
    while i < len(data):
        bin_begin = max(0, (i - binsize/2))
        bin_end = min(len(data),(i+binsize/2))
        the_bin = data[bin_begin:bin_end]
        
        std = np.nanstd(np.sort(the_bin)[1:])
        median = np.median(the_bin)
        upperbound = (median + (usig*std))
        lowerbound = (median - (lsig*std))
        upperlist.append(upperbound)
        lowerlist.append(lowerbound)
        if (data[i] < upperbound) and (data[i] > lowerbound):
            data_clipped.append(data[i])
            ax_clipped.append(ax[i])
            err.append(ef[i])
        
        i = i + 1
    
    return data_clipped, ax_clipped, err


def calc_i(_a, _b):
    return np.degrees(np.arccos(_b / _a))

def calc_b(_a, _i):
    return _a * np.cos(np.radians(_i))

