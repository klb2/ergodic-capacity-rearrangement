"""Calculations of the best case for dependent Rayleigh fading channels.

This module contains different functions to calculate the best-case/upper
bound on the outage capacity for dependent Rayleigh fading channels.


Copyright (C) 2020 Karl-Ludwig Besser

Parts of this program are taken from
https://gitlab.com/klb2/reliability-bounds-dependent-fading-channels which
belongs to the article Karl-Ludwig Besser and Eduard Jorswieck, "Reliability
Bounds for Dependent Fading Wireless Channels", IEEE Transactions on Wireless
Communications, 2020, DOI:10.1109/TWC.2020.2997332.

This program belongs to the article
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
from scipy import optimize

#np.seterr(all='raise')


# Definitions of f, F, G, H
def pdf(x):
    return np.exp(-x)

def cdf(x):
    return 1-np.exp(-x)

def inv_cdf(x):
    x = np.minimum(x, 1)
    return -np.log(1-x)

def H(x, n, a):
    return (n-1)*inv_cdf(a+(n-1)*x) + inv_cdf(1-x)

def T(x, n, a):  # Integral of H
    return n*x - x*np.log(x) + (1-a+x-n*x)*np.log(1-a+x-n*x)

def psi(a):  # Conditional expectation
    if a == 1:
        return np.inf
    return 1 - np.log(1-a)


def lhs_cmin(c, n, a):
    if c == 0:
        return (-1 + a)*(-1 + np.log(1-a))
    return (1-a)-(c*n - c*np.log(c) + (1-a+c-c*n)*np.log(1-a+c-c*n))

def rhs_cmin(c, n, a):
    return ((1-a)/n-c)*H(c, n, a)

def diff_cmin(c, n, a):
    return lhs_cmin(c, n, a) - rhs_cmin(c, n, a)


def determine_cmin(n, a):
    _eps = np.finfo(float).eps
    x0 = ((1-a)/n+_eps)/2
    bracket = [0+_eps, (1-a)/(n*(n-1))]
    try:
        solution = optimize.root_scalar(diff_cmin, args=(n, a), x0=x0,
                                        bracket=bracket)
    except ValueError as e:
        print("Error during root solving for n={:d}, a={:.2f}: {}".format(n, a, e))
        return 1
    #print(solution)
    return solution.root
