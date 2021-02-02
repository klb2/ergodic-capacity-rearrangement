"""Run the Rayleigh fading simulations from the paper.

This module contains different functions to rerun the simulations from the
paper with homogeneous Rayleigh fading channels.


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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from rayleigh_fading import (rayleigh_best_ergodic_ra, rayleigh_comon_ergodic,
                             rayleigh_iid_ergodic, rayleigh_worst_ergodic_ra,
                             rayleigh_best_ergodic)

def main(snr_db=10., num_levels=1000, plot=True, export=False):
    #n = np.arange(2, 11)
    n = np.arange(2, 31)
    snr = 10**(snr_db/10.)
    best_case_ra = np.array([rayleigh_best_ergodic_ra(snr, _n, num_levels=num_levels) for _n in n])
    worst_case_ra = np.array([rayleigh_worst_ergodic_ra(snr, _n, num_levels=num_levels) for _n in n])
    best_case_exact = np.array([rayleigh_best_ergodic(snr, _n) for _n in n])
    comon = rayleigh_comon_ergodic(snr, n)
    indep = rayleigh_iid_ergodic(snr, n)
    if export:
        filename = "EC-rayleigh-snr{}-numLev{}.dat".format(snr_db, num_levels)
        results = {"bestExact": best_case_exact,
                   "bestLow": best_case_ra[:, 0], "bestUp": best_case_ra[:, 1],
                   "worstLow": worst_case_ra[:, 0], "worstUp": worst_case_ra[:, 1],
                   "comon": comon, "iid": indep, "n": n}
        export_data(results, filename)
    num_levels = [5, 10, 100, 1000, 10000]
    n_quant = 3
    best_case_quant = np.array([rayleigh_best_ergodic_ra(snr, n_quant, num_levels=_levels) for _levels in num_levels])
    if export:
        filename = "quantgap-rayleigh-snr{}-n{}.dat".format(snr_db, n_quant)
        results = {"numLevels": num_levels, "upper": best_case_quant[:, 1],
                   "lower": best_case_quant[:, 0],
                   "gap": np.diff(best_case_quant, axis=1).ravel()}
        export_data(results, filename)
    if plot:
        fig1, axs1 = plt.subplots()
        axs1.plot(n, best_case_ra, 'o--', c='b', label="Best Case RA")
        axs1.plot(n, worst_case_ra, 'o--', c='r', label="Worst Case RA")
        axs1.plot(n, comon, 'o--', c='orange', label="Comonotonic Exact")
        axs1.plot(n, best_case_exact, 'o--', label="Best Case Exact")
        axs1.plot(n, indep, 'o--', label="Independent")
        axs1.legend()
        fig2, axs2 = plt.subplots(subplot_kw={"projection": "3d"})
        best_case = rayleigh_best_ergodic_ra(snr, 3, return_ra=True, num_levels=1000)
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
