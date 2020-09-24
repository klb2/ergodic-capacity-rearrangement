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
    return NotImplemented

def rayleigh_comon_ergodic(snr, n):
    _part1 = np.exp(1./(n*snr))
    _part2 = expi(-1./(n*snr))
    return -_part1*_part2/np.log(2)


def main():
    n = np.arange(2, 10)
    snr = 10**(10/10.)
    best_case = np.array([rayleigh_best_ergodic(snr, _n) for _n in n])
    worst_case = np.array([rayleigh_worst_ergodic(snr, _n) for _n in n])
    comon = rayleigh_comon_ergodic(snr, n)
    plt.plot(n, best_case, 'o--', c='b', label="Best Case")
    plt.plot(n, worst_case, 'o--', c='r', label="Worst Case")
    plt.plot(n, comon, 'o--', c='orange', label="Comonotonic Exact")
    plt.legend()
    best_case = rayleigh_best_ergodic(snr, 3, return_ra=True, num_levels=1000)
    ra_best = best_case[1][0]
    print(ra_best)
    #ra_best = 1.-np.exp(-ra_best)
    #fig, axs = plt.subplots(3)
    #axs[0].scatter(ra_best[:, 0], ra_best[:, 1])
    #axs[1].scatter(ra_best[:, 0], ra_best[:, 2])
    #axs[2].scatter(ra_best[:, 1], ra_best[:, 2])
    fig2, axs2 = plt.subplots(subplot_kw={"projection": "3d"})
    axs2.scatter(*ra_best.T)
    #axs[1].hist(ra_best[:, 0], bins=30, density=True)
    num_levels = [5, 10, 100, 1000, 10000]
    best_case_quant = np.array([rayleigh_best_ergodic(snr, 5, num_levels=_levels) for _levels in num_levels])
    plt.figure()
    plt.loglog(num_levels, np.diff(best_case_quant, axis=1).ravel())


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    main()
    plt.show()
