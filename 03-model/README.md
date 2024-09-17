# Model outputs practical session instructions

In this session we will explore freely available model data provided by the [Copernicus Atmosphere Monitoring Service (CAMS)](https://atmosphere.copernicus.eu/). This data is available via the [Atmosphere Data Store (ADS)](https://ads-beta.atmosphere.copernicus.eu/).

## 1. Register with Atmosphere Data Store and obtain API key

 - Register a free account with the [Atmosphere Data Store](https://ads-beta.atmosphere.copernicus.eu/) (top right link).

 - Having registered with the ADS, follow the [instructions here](https://ads-beta.atmosphere.copernicus.eu/how-to-api) to obtain a key to use the Application Programming Interface (API) in order to download data from the ADS programmatically.

## 2. Explore the Atmosphere Data Store

Explore the various datasets on the [ADS](https://ads-beta.atmosphere.copernicus.eu/), including forecast products, emission inventories, reanalysis and other data types. Visit the `download data` tab of some products and try downloading small data samples.

## 3. Discover the CAMS learning materials

Discover the [Jupyterbook of data tutorials](https://ecmwf-projects.github.io/copernicus-training-cams) for examples of how to programmatically download, process, and visualize data from the ADS. The tutorials cover creating maps, animations, time series charts, and other plots.

## 4. Practical exercises

Now it is time for you to do your own data analysis. Follow the existing tutorials, and use them as templates, to carry-out the steps below to download, process and visualise CAMS model data.

### 4.1 CAMS Global Atmospheric Composition Forecast Practical

Browse the [CAMS global atmospheric composition forecast](https://ads-beta.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts?tab=overview) data and download the following:

 - 'variable': 'total_aerosol_optical_depth_550nm',
 - 'date': '2024-08-01/2024-08-31',
 - 'time': '12:00',
 - 'leadtime_hour': '0',
 - 'type': 'forecast',
 - 'format': 'netcdf',

Plot a global map of the first forecast time-step.

Create an animation of all forecast time steps.

Plot a time series for the grid point nearest to Oslo:

 - Lat = 59.91
 - Lon = 10.73

[SOLUTION](https://nbviewer.org/github/ecmwf-training/cams-act6/blob/main/03-model/cams-global-forecast.ipynb)

### 4.2 CAMS Global Reanalysis Practical

Browse the [CAMS global reanalysis monthly averaged fields](https://ads-beta.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4-monthly?tab=overview) data and download the following:

 - 'format': 'netcdf',
 - 'variable': 'dust_aerosol_optical_depth_550nm',
 - 'year': ['2003' to '2023'],
 - 'month': '06',
 - 'product_type': 'monthly_mean',

Calculate the climatology for June 2003 to 2023.

Calculate the anomaly for June 2020 with respect to this climatology.

[SOLUTION](https://nbviewer.org/github/ecmwf-training/cams-act6/blob/main/03-model/cams-global-reanalysis.ipynb)

### 4.3 CAMS Regional Air Quality Forecast Practical

Browse the [CAMS regional air quality forecast](https://ads-beta.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-forecasts?tab=overview) data and download the following:

 - start_date = '2024-07-30'
 - end_date = '2024-07-30'
 - time = '00:00'
 - lead_time_start = 0
 - lead_time_stop = 96
 - step_hours = 1
 - leadtime_hours = list(range(lead_time_start, lead_time_stop +  - lead_time_start, step_hours))
 - variables = ['ozone']
 - models = ['ensemble']
 - levels = [0]

Calculate the daily max and daily mean ozone concentrations at the surface.

Create a forecast plot for each day.

Plot a time series for all time steps over the 96 hour forecast over Oslo.

[SOLUTION](https://nbviewer.org/github/ecmwf-training/cams-act6/blob/main/03-model/cams-regional-forecast.ipynb)