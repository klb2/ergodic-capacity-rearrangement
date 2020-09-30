import numpy as np
from scipy import stats
from scipy import integrate
from rpy2.robjects.functions import rinterface
from rpy2.robjects.packages import importr
import matplotlib.pyplot as plt

from ergodic_capac_ra import bounds_ergodic
from run_simulations import export_data

stats_r = importr("stats")

def _quant_mixed(n):
    quant_func = [rinterface.evalr("(function (p) qexp(p, rate=1/4))"),
                  rinterface.evalr("(function (p) qlnorm(p, sdlog=sqrt(2*log(4))))"),
                  rinterface.evalr("(function (p) qchisq(p, 4))")]
    return quant_func

mixed_best_ergodic_ra = bounds_ergodic("best")(_quant_mixed)
mixed_worst_ergodic_ra = bounds_ergodic("worst")(_quant_mixed)

RV = [stats.expon(scale=4), stats.lognorm(np.sqrt(2*np.log(4))), stats.chi2(4)]
def mixed_comonotonic(snr):
    int_func = lambda u: np.log2(1 + snr*sum([_rv.ppf(u) for _rv in RV]))
    comon = integrate.quad(int_func, 0, 1)[0]
    return comon

def mixed_independent(snr, num_samples=10000):
    samples = [_rv.rvs(num_samples) for _rv in RV]
    samples = np.sum(samples, axis=0)
    capac = np.log2(1 + snr*samples)
    return np.mean(capac)


def main(num_levels, export=False, plot=False, only_ra=False):
    snr_db = np.arange(0, 21)
    snr = 10**(snr_db/10.)
    print("Running RA to determine best case")
    best_case_ra = np.array([mixed_best_ergodic_ra(_snr, 3, num_levels=num_levels) for _snr in snr])
    print("Running RA to determine worst case")
    worst_case_ra = np.array([mixed_worst_ergodic_ra(_snr, 3, num_levels=num_levels) for _snr in snr])
    if not only_ra:
        print("Calculating comonotonic case")
        comon = np.array([mixed_comonotonic(_snr) for _snr in snr])
        print("Estimating independent case")
        indep = np.array([mixed_independent(_snr) for _snr in snr])
    else:
        comon = np.zeros_like(snr_db)
        indep = np.zeros_like(snr_db)
    if export:
        filename = "EC-mixed-numLev{}.dat".format(num_levels)
        results = {"bestLow": best_case_ra[:, 0], "bestUp": best_case_ra[:, 1],
                   "worstLow": worst_case_ra[:, 0], "worstUp": worst_case_ra[:, 1],
                   "comon": comon, "indep": indep, "snr": snr_db}
        export_data(results, filename)
    if plot:
        fig, axs = plt.subplots()
        axs.plot(snr_db, best_case_ra, c='b', label="Best Case")
        axs.plot(snr_db, worst_case_ra, c="r", label="Worst Case")
        axs.plot(snr_db, comon, c='orange', label="Comonotonic")
        axs.plot(snr_db, indep, c='g', label="Independent")
        axs.set_xlabel("SNR [dB]")
        axs.set_ylabel("Ergodic Capacity [bit]")
        axs.legend()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_levels", type=int, default=1000, help="Number of quantization steps")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--only_ra", action="store_true")
    args = vars(parser.parse_args())
    main(**args)
    plt.show()
