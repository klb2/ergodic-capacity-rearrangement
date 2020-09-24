import functools

import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.functions import rinterface
from rpy2.robjects.packages import importr

base_r = importr("base")
stats_r = importr("stats")
r = robjects.r
r.source('ergodicRA.R')
#qrmtools = importr("qrmtools")

def rearrangement_supermod(quant_func, num_levels):
    results = r.supermodRA(quant_func, int(num_levels))
    low = np.array(results[0])
    up = np.array(results[1])
    return np.stack((low, up))
#rearrangement_supermod = np.vectorize(rearrangement_supermod)

def _create_comonotonic(quant_func, num_levels):
    p_low = rinterface.evalr('''
                             p <- (0:({0}-1))/{0}
                             (function (qF) qF(p))'''.format(num_levels), 2)
    low = np.array(base_r.sapply(quant_func, p_low))
    p_up = rinterface.evalr('''
                            p <- (1:{0})/{0}
                            (function (qF) qF(p))'''.format(num_levels), 2)
    up = np.array(base_r.sapply(quant_func, p_up))
    #X.up[N,] <- sapply(1:d, function(j) if(is.infinite(X.up[N,j])) qF[[j]](level+(1-level)*(1-1/(2*N))) else X.up[N,j])
    up[-1] = np.array(base_r.sapply(quant_func, rinterface.evalr("(function (qF) qF(1-1/(2*{})))".format(num_levels))))
    return np.stack((low, up))


#NUM_LEVELS = 1000
def bounds_ergodic(bound):
    def decorator_bound(func):
        @functools.wraps(func)
        def wrapper_dec(snr, n, num_levels=100, return_ra=False, *args, **kwargs):
            quant_func = func(n, *args, **kwargs)
            if bound == "best":
                rearranged = rearrangement_supermod(quant_func, num_levels=num_levels)
            elif bound == "worst":
                rearranged = _create_comonotonic(quant_func, num_levels=num_levels)
            _capac = np.log2(1. + snr*np.sum(rearranged, axis=2))
            _capac = np.mean(_capac, axis=1)
            if return_ra:
                return _capac, rearranged
            else:
                return _capac
        return wrapper_dec
    return decorator_bound
