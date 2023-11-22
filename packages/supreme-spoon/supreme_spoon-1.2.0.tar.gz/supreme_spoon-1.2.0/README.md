# supreme-SPOON
supreme-**S**teps to **P**rocess S**O**SS **O**bservatio**N**s

**supreme-SPOON** is an end-to-end pipeline for NIRISS/SOSS time series observations (TSOs).
The pipeline is divided into four stages:
 - Stage 1: Detector Level Processing 
 - Stage 2: Spectroscopic Processing
 - Stage 3: 1D Spectral Extraction
 - Stage 4: Light Curve Fitting (optional)

## Installation Instructions
The latest release of **supreme-SPOON** can be downloaded from PyPI by running:

    pip install supreme_spoon

The default pip installation only includes Stages 1 to 3. Stage 4 can be included via specifying the following option during installation:

    pip install supreme_spoon[stage4]

Note that the radvel package may fail to build during the installation of Stage4. If so, simply run ```pip install cython```, and then proceed with the **supreme-SPOON** installation as before.

The latest development version can be grabbed from GitHub (inlcludes all pipeline stages):

    git clone https://github.com/radicamc/supreme-spoon
    cd supreme_spoon
    python setup.py install

Note that **supreme-SPOON** is currently compatible with python 3.10.4 and v1.8.5 of the official JWST DMS. If you wish to run a 
different version of jwst, certain functionalities of **supreme-SPOON** may not work.

## Usage Instructions
The **supreme-SPOON** pipeline can be run in a similar fashion to the JWST DMS, by individually calling each step.
Alternatively, Stages 1 to 3 can be run at once via the ```run_DMS.py``` script.

1. Copy the ```run_DMS.py``` script and the ```run_DMS.yaml``` config file into your working directory.
2. Fill out the yaml file with the appropriate inputs.
3. Once happy with the input parameters, enter ```python run_DMS.py run_DMS.yaml``` in the terminal.

To use the light curve fitting capabilities (if installed), simply follow the same procedure with the fit_lightcurves.py and .yaml files. 

## Citations
If you make use of this code in your work, please cite [Radica et al. (2023)](https://ui.adsabs.harvard.edu/abs/2023arXiv230517001R/abstract) and [Feinstein et al. (2023)](https://ui.adsabs.harvard.edu/abs/2023Natur.614..670F/abstract). 

### Additional Citations
If you use the ATOCA extraction algorithm, please also cite [Radica et al. (2022)](https://ui.adsabs.harvard.edu/abs/2022PASP..134j4502R/abstract) 
and [Darveau-Bernier et al. (2022)](https://ui.adsabs.harvard.edu/abs/2022PASP..134i4502D/abstract).

If you make use of the light curve fitting routines, also include the following citations for 
[juliet](https://ui.adsabs.harvard.edu/abs/2019MNRAS.490.2262E/abstract), 
[batman](https://ui.adsabs.harvard.edu/abs/2015PASP..127.1161K/abstract), 
[dynesty](https://ui.adsabs.harvard.edu/abs/2020MNRAS.493.3132S/abstract), and 
[Kipping et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013MNRAS.435.2152K/abstract) for the limb-darkening sampling. 
If you use Gaussian Processes please cite [celerite](https://ui.adsabs.harvard.edu/abs/2017AJ....154..220F/abstract), 
and if you use ExoTiC-LD for limb darkening priors cite [Grant & Wakeford (2022)](https://doi.org/10.5281/zenodo.7437681). 
Please also see the ExoTiC-LD documentation for information on the types of stellar grids available and ensure to correctly download and cite the desired models.

Lastly, you should cite the libraries upon which this code is built, namely:
[numpy](https://ui.adsabs.harvard.edu/abs/2020Natur.585..357H/abstract), 
[scipy](https://ui.adsabs.harvard.edu/abs/2020NatMe..17..261V/abstract),
[astropy](https://ui.adsabs.harvard.edu/abs/2013A%26A...558A..33A/abstract), and of course
[jwst](https://zenodo.org/record/7038885/export/hx).
