[![logo](https://raw.githubusercontent.com/ecmwf-training/cams-act6/main/images/logoline.png)](https://atmosphere.copernicus.eu/6th-ecmwf-cams-esa-eumetsat-training-atmospheric-composition)

# Jupyter notebooks for the ECMWF CAMS, EUMETSAT & ESA training in atmospheric composition

This repository contains the Jupyter notebooks used for the practical sessions of the [6th joint ECMWF CAMS, ESA and EUMETSAT training in atmospheric composition](https://atmosphere.copernicus.eu/6th-ecmwf-cams-esa-eumetsat-training-atmospheric-composition),
held on 16-20 September 2024, at NILU, in Kjeller, Norway.

Each directory in this repository contains code, Jupyter notebooks and other (non-data) files related to the practical sessions.

The directories are numbered according to the order in which they appear in [the course programme](https://atmosphere.copernicus.eu/6th-ecmwf-cams-esa-eumetsat-training-atmospheric-composition)

## Table of contents
This is a list of the practical sessions based on Jupyter notebooks.

1. [Satellite observations](/01-satellite/): Explore satellite datasets including S3 Fire Radiative Power, plumes from S3 OCLI, emissions from GOME-2, IASI, TROPOMI NO2 and other species, Scar Burn from S2.
2. [In-situ obervations](/02-in-situ/): Process and visualise in-situ data, e.g. from the Pandora instrument. The instrument is a passive sensor used to monitor chemical species based on the Differential Optical Absorption Spectroscopy (DOAS) technique.
3. [Model data](/03-model/): Explore forecast and reanalysis datasets from the Copernicus Atmosphere Monitoring Service (CAMS)
4. [Emissions inventories](/04-emissions/): Download and visualise emssions data from inventories freely provided by CAMS.
5. [CAMS Model Output Statistics](/05-cams-mos/): Discover AI optimised forecasts combining in-situ and regional model data.
6. [Averaging Kernels](/06-ak/): Compare models with satellite data, e.g. for NO2 from [TROPOMI](https://www.tropomi.eu/), using the averaging kernels statistical algorithm.
7. [Aeroval model evaluation](/07-aeroval/): Evaluate models with surface measurements through [AeroVal](https://aeroval.met.no/)
8. [Air quality index](/08-aqi/): Calculate the air quality index forecast from $NO_2$, $O_3$, $SO_2$, $PM10$ and $PM2.5$ concentrations using model data.


## How to run the notebooks
The easiest way to run these notebooks is through the one of the many free cloud based Jupyter environments. Four such environments are suggested here. Most can be launched directly in the notebooks through links provided at the top of each notebook, see the below for example:

**Run the tutorial via free cloud platforms**: [![binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/ecmwf-training/cams-act6/main?labpath=jupyter-notebook-template.ipynb)
[![kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/ecmwf-training/cams-act6/blob/main/jupyter-notebook-template.ipynb)
[![colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ecmwf-training/cams-act6/blob/main/jupyter-notebook-template.ipynb)

### [Binder](https://mybinder.org/)
Binder will build a live environment in which to run notebooks. It may take some time to launch, given that each time a new environment is created from the environment.yml file in this repository. 

### [Kaggle](https://www.kaggle.com/code)
Kaggle is a free service with a pre-built environment for running notebooks. Unlike Binder, it is therefore quick to launch. You will need to create a free account, and upon access, you will need to "turn on the internet" in the settings.

### [Colab](https://colab.research.google.com/)
Colab is also a free service with a pre-built environment. Some libraries, such as Cartopy, are not included but can be installed from within the notebook (`!pip install cartopy`). Colab also requires free login.

### [WEkEO](https://www.wekeo.eu/)
WEkEO is the EU Copernicus DIAS reference service for environmental data. It includes a JupyterLab environment with limited free resources that can be scaled up with a paid plan. It also provides free access to many satellite and derived datasets. There is not one single link to directly open a notebook in WEkEO, but notebooks can be run in WEkEO by following these steps:

- browse to wekeo.eu
- Register for free, or login
- Open Jupyterlab
- Open Terminal
- Enter the command `git clone https://github.com/ecmwf-training/cams-act6`
- browse to the notebook in the directory tree on the left panel

### Run locally on your computer
Another option is to run the notebooks locally on your own computer. To do this you would need to install Python, Jupyter and the various packages listed in the [`environment.yml`](./environment.yml) file. All software necessary for running the notebooks can be freely installed.

## Access to data

-	[Copernicus Data Space](https://dataspace.copernicus.eu/). Access to data and services from the Sentinel missions.
-	[EUMETSAT Earth Observation Portal](https://eoportal.eumetsat.int/). Access to data disseminated by EUMETSAT.
-	[Atmosphere Data Store (ADS)](https://ads.atmosphere.copernicus.eu/). Access to data from the Copernicus Atmosphere Monitoring Service (CAMS). Having registered, obtain your [API key here](https://ads.atmosphere.copernicus.eu/how-to-api).
