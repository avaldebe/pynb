# [CAMS50][cams50]

> The regional air quality (RAQ) production of the Copernicus Atmosphere Monitoring Service (CAMS) is based on seven state-of-the-art numerical air quality models developed in Europe : CHIMERE from INERIS (France), [EMEP][emepctm] from MET Norway (Norway), EURAD-IM from University of Cologne (Germany), LOTOS-EUROS from KNMI and TNO (Netherlands), MATCH from SMHI (Sweden), MOCAGE from METEO-FRANCE (France) and SILAM from FMI (Finland). Common to all models, the meteorological parameters settings (coming from the ECMWF global weather operating sytem), the boundary conditions for chemical species (coming fron the CAMS IFS-MOZART global production), the emissions coming from CAMS emission (for anthropic emissions over Europe and for biomass burning).

[cams50]: http://www.regional.atmosphere.copernicus.eu
[emepctm]: https://github.com/metno/emep-ctm

## 2015 validated reanalysis

CAMS50 runs a reanalysis with validated obrvations 2 years after the fact.
On the 2015 Validated ReAnalysis, or VRA2015 for short,
the EMEP analysis results failed to capture O3 and PM10 exedances.
PM10 was not assimilated, so no surprice there.
The O3 exedances were missed as the assimation system was set to
reject observations larger than 150 ug/m3.

The effect of the O3 rejection limit and PM10 assimilation
on the exedances statistics is explored in the following notebooks:

- [Collocation](collocation.ipynb) of model results to observation sites
- [Exceedances](exceedances.ipynb) on VRA2015 and complementary runs.

#### conda environment at work
The notebooks and scripts on this folder use geoviews and geopandas modules.
This are privided by the geoviews environment on PPI/lustre.

Activate this environment before you start the notebook as follows:
```bash
# load anaconda module
module load aerocom/anaconda3-stable

# activate enviroment
source activate geoviews

# start jupyter
jupyter notebook --no-browser --ip=$HOSTNAME.met.no
```
