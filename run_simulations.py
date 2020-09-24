import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from rayleigh_fading import (rayleigh_best_ergodic, rayleigh_comon_ergodic,
                             rayleigh_iid_ergodic, rayleigh_worst_ergodic)

def main(snr_db=10., num_levels=1000, plot=True, export=False):
    n = np.arange(2, 10)
    snr = 10**(snr_db/10.)
    best_case = np.array([rayleigh_best_ergodic(snr, _n, num_levels=num_levels) for _n in n])
    worst_case = np.array([rayleigh_worst_ergodic(snr, _n, num_levels=num_levels) for _n in n])
    comon = rayleigh_comon_ergodic(snr, n)
    indep = rayleigh_iid_ergodic(snr, n)
    if export:
        filename = "EC-rayleigh-snr{}-numLev{}.dat".format(snr_db, num_levels)
        results = {"bestLow": best_case[:, 0], "bestUp": best_case[:, 1],
                   "worstLow": worst_case[:, 0], "worstUp": worst_case[:, 1],
                   "comon": comon, "iid": indep, "n": n}
        export_data(results, filename)
    num_levels = [5, 10, 100, 1000, 10000]
    best_case_quant = np.array([rayleigh_best_ergodic(snr, 5, num_levels=_levels) for _levels in num_levels])
    if plot:
        fig1, axs1 = plt.subplots()
        axs1.plot(n, best_case, 'o--', c='b', label="Best Case")
        axs1.plot(n, worst_case, 'o--', c='r', label="Worst Case")
        axs1.plot(n, comon, 'o--', c='orange', label="Comonotonic Exact")
        axs1.legend()
        fig2, axs2 = plt.subplots(subplot_kw={"projection": "3d"})
        best_case = rayleigh_best_ergodic(snr, 3, return_ra=True, num_levels=1000)
        ra_best = best_case[1][0]
        #print(ra_best)
        #ra_best = 1.-np.exp(-ra_best)
        axs2.scatter(*ra_best.T)
        #axs[1].hist(ra_best[:, 0], bins=30, density=True)
        fig3, axs3 = plt.subplots()
        axs3.loglog(num_levels, np.diff(best_case_quant, axis=1).ravel())

def export_data(data, filename):
    import pandas as pd
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filename, sep="\t", index=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--snr", dest="snr_db", type=float, help="SNR in dB", default=10)
    parser.add_argument("-n", "--num_levels", type=int, default=1000, help="Number of quantization steps")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--plot", action="store_true")
    args = vars(parser.parse_args())
    main(**args)
    plt.show()
