"""Functions for Rayleigh fading channels.

This module contains different functions to calculate the ergodic capacity for
Rayleigh fading channels.


Copyright (C) 2020 Karl-Ludwig Besser

This program is used in the article:
Karl-Ludwig Besser and Eduard Jorswieck, "Calculation of Bounds on the Ergodic
Capacity for Fading Channels with Dependency Uncertainty", 2021 IEEE
International Conference on Communications (ICC), 2021.

License:
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
See the GNU General Public License for more details.

Author: Karl-Ludwig Besser, Technische Universität Braunschweig
"""
__author__ = "Karl-Ludwig Besser"
__copyright__ = "Copyright (C) 2020 Karl-Ludwig Besser"
__credits__ = ["Karl-Ludwig Besser", "Eduard A. Jorswieck"]
__license__ = "GPLv3"
__version__ = "1.0"

import numpy as np
from scipy.special import expi, expn
from scipy import integrate
from rpy2.robjects.functions import rinterface
from rpy2.robjects.packages import importr

from ergodic_capac_ra import bounds_ergodic
from best_case_rayleigh import H, determine_cmin

stats_r = importr("stats")

def _quant_rayleigh(n, lam=None):
    if lam is None:
        quant_func = [stats_r.qexp]*n
    else:
        quant_func = [rinterface.evalr("(function (p) qexp(p, rate={}))".format(l)) for l in lam]
        if len(quant_func) != len(lam):
            raise ValueError("The length of provided lambdas needs to be equal to n")
    return quant_func

rayleigh_best_ergodic_ra = bounds_ergodic("best")(_quant_rayleigh)
rayleigh_worst_ergodic_ra = bounds_ergodic("worst")(_quant_rayleigh)

def rayleigh_best_ergodic(snr, n):
    cmin = determine_cmin(n, 0)
    _int_func = lambda x, n: np.log2(1 + snr*H(x, n, 0))
    _integral = integrate.quad(_int_func, 0, cmin, args=(n,))[0]
    _part2 = (1-n*cmin)*_int_func(cmin, n)
    return n*_integral + _part2

def rayleigh_iid_ergodic(snr, n):
    # Sum is Gamma-distributed
    _part1 = np.log2(np.e) * np.exp(1/snr)
    k = np.arange(0, max(n))
    #_part2 = gammaincc(-k, 1./snr)*gamma(-k)/snr**k
    _part2 = expn(1+k, 1/snr)
    _part2 = np.cumsum(_part2)[-len(n):]
    return _part1 * _part2

def rayleigh_comon_ergodic(snr, n):
    _part1 = np.exp(1./(n*snr))
    _part2 = expi(-1./(n*snr))
    return -_part1*_part2/np.log(2)

if __name__ == "__main__":
    best_case_ra = rayleigh_best_ergodic_ra(10, n=2, return_ra=True, num_levels=1000)[1]
    print(best_case_ra[0])
    #print(np.sum(best_case_ra[0], axis=1))
    print(np.log2(1 + 10*np.sum(best_case_ra[0], axis=1)))
    print(np.mean(np.log2(1 + 10*np.sum(best_case_ra[0], axis=1))))
