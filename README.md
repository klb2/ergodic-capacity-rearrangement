# Bounds on the Ergodic Capacity for Dependent Fading Channels

This repository contains supplementary material for the paper "Calculation of
Bounds on the Ergodic Capacity for Fading Channels with Dependency Uncertainty"
(Karl-L.  Besser and Eduard Jorswieck, 2021 IEEE International Conference on
Communications (ICC), 2021, [doi:10.1109/ICC42927.2021.9500869](https://doi.org/10.1109/ICC42927.2021.9500869)).

The idea is to give an interactive version of the calculations and presented
concepts to the reader. One can also change different parameters and explore
different behaviors on their own.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/klb2%2Fergodic-capacity-rearrangement/master)


## File List
The following files are provided in this repository:

* [Ergodic Capacity Bounds.ipynb](https://mybinder.org/v2/gl/klb2%2Fergodic-capacity-rearrangement/master?filepath=Ergodic%20Capacity%20Bounds.ipynb):
  Jupyter notebook that contains the plots from the paper.
* `rayleigh_fading.py`: Python module that contains all functions for the
  Rayleigh fading example.
* `best_case_rayleigh.py`: Python module that contains the functions to
  calculate the exact best case for homogeneous Rayleigh fading. The code is
  taken from
  [https://gitlab.com/klb2/reliability-bounds-dependent-fading-channels](https://gitlab.com/klb2/reliability-bounds-dependent-fading-channels).
* `run_simulations.py`: Python script to run the Rayleigh fading example. Use
  `python run_simulations.py --help` to get an overview of the options.
* `mixed_marginals.py`: Python module that contains all functions for the
  example with mixed marginal distributions. This can be run to reproduce the
  results of the mixed marginal example.
* `ergodic_capac_ra.py`: Python module that contains the wrapper around the RA
  that was implemented in R.
* `RAergodic.R`: R script that contains a modified version of the RA. The code
  is modified from the original implementation, which is part of the
  [qrmtools](https://cran.r-project.org/package=qrmtools) R package.


## Usage
### Running it online
The easiest way is to use services like [Binder](https://mybinder.org/) to run
the notebook online. Simply navigate to
[https://mybinder.org/v2/gl/klb2%2Fergodic-capacity-rearrangement/master](https://mybinder.org/v2/gl/klb2%2Fergodic-capacity-rearrangement/master)
to run the notebooks in your browser without setting everything up locally.

### Local Installation
If you want to run it locally on your machine, Python3 and Jupyter are needed.
The present code was developed and tested with the following versions:
- Python 3.8.5
- R 4.0.2
- Jupyter 1.0.0
- numpy 1.19.2
- scipy 1.5.2
- rpy2 3.3.5
- qrmtools 0.0-13

Make sure you have [Python3](https://www.python.org/downloads/) and
[R](https://www.r-project.org/) installed on your computer.
You can then install the required packages (including Jupyter) by running
```bash
pip3 install -r requirements.txt
jupyter nbextension enable --py widgetsnbextension ipympl
R -e "install.packages('qrmtools', repos='https://cloud.r-project.org/')"
```
This will install all the needed packages which are listed in the requirements 
file. The second line enables the interactive controls in the Jupyter
notebooks.

Finally, you can run the Jupyter notebooks with
```bash
jupyter notebook 'Ergodic Capacity Bounds.ipynb'
```


## Acknowledgements
This research was supported in part by the Deutsche Forschungsgemeinschaft
(DFG) under grant JO 801/23-1.


## License and Referencing
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

You can use the following BibTeX entry
```bibtex
@inproceedings{Besser2021icc,
	address = {Montreal, QC, Canada},
	author = {Besser, Karl-Ludwig and Jorswieck, Eduard A.},
	booktitle = {ICC 2021 -- IEEE International Conference on Communications (ICC)},
	month = {6},
	publisher = {IEEE},
	title = {Calculation of Bounds on the Ergodic Capacity for Fading Channels with Dependency Uncertainty},
	year = {2021},
	doi = {10.1109/ICC42927.2021.9500869},
}
```

Parts of this code are based on the
[qrmtools](https://cran.r-project.org/package=qrmtools) R package, which is
also released under the GPLv3 license.
