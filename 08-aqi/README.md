Air Quality Index
=================
In this training session we will use the [Global Air Quality Index](cams_glob_eaqi.ipynb) notebook to compute the forecasts of the global air quality index (AQI). The computation of the AQI forecast is based on the forecast concentration of the following pollutants: $O_3, NO_2, SO_2, PM2.5, PM10$. The index is computed according to the [European Air Quality Index](https://en.wikipedia.org/wiki/Air_quality_index#Europe) definition. The concentration of the pollutants will be time averaged and transformed in $\mu g \cdot m^{-3}$ and finally classified in one of six levels, from *Good* to *Extremly poor*, according to the threshold levels defined in the European Air Quality Index. The air quality index is the highest value of the concentration levels of the pollutants. For instance, if the concentration level in a grid cell for $NO_2, SO_2, PM2.5, PM10$ is *Good* but for $O_3$ is *Mediocre*, then the air quality index for that grid cell is *Mediocre*.   




