import numpy as np
from scipy.special import expi
from rpy2.robjects.functions import rinterface
from rpy2.robjects.packages import importr

from ergodic_capac_ra import bounds_ergodic

stats_r = importr("stats")

def _quant_rayleigh(n, lam=None):
    if lam is None:
        quant_func = [stats_r.qexp]*n
    else:
        quant_func = [rinterface.evalr("(function (p) qexp(p, rate={}))".format(l)) for l in lam]
        if len(quant_func) != len(lam):
            raise ValueError("The length of provided lambdas needs to be equal to n")
    return quant_func

rayleigh_best_ergodic = bounds_ergodic("best")(_quant_rayleigh)
rayleigh_worst_ergodic = bounds_ergodic("worst")(_quant_rayleigh)

def rayleigh_iid_ergodic(snr, n):
    # Sum is Gamma-distributed
    #return NotImplemented
    return n

def rayleigh_comon_ergodic(snr, n):
    _part1 = np.exp(1./(n*snr))
    _part2 = expi(-1./(n*snr))
    return -_part1*_part2/np.log(2)
