# [CAMS50][cams50]

> The regional air quality (RAQ) production of the Copernicus Atmosphere Monitoring Service (CAMS) is based on seven state-of-the-art numerical air quality models developed in Europe : CHIMERE from INERIS (France), [EMEP][emepctm] from MET Norway (Norway), EURAD-IM from University of Cologne (Germany), LOTOS-EUROS from KNMI and TNO (Netherlands), MATCH from SMHI (Sweden), MOCAGE from METEO-FRANCE (France) and SILAM from FMI (Finland). Common to all models, the meteorological parameters settings (coming from the ECMWF global weather operating sytem), the boundary conditions for chemical species (coming fron the CAMS IFS-MOZART global production), the emissions coming from CAMS emission (for anthropic emissions over Europe and for biomass burning).

[cams50]: http://www.regional.atmosphere.copernicus.eu
[emepctm]: https://github.com/metno/emep-ctm

## 2016 validated reanalysis

CAMS50 runs a reanalysis with validated obrvations 2 years after the fact.
The results for the 2016 Validated ReAnalysis, or VRA2016 for short,
and complementary runs are compared to the provided observation datasts
on the follwwing notebooks:

- [Stations](stations.ipynb) datasets pre-processing
- [Collocation](collocation.ipynb) of model results to observation sites
- [Classification](classification.ipynb) and location of surface stations
- [Stats](stats.ipynb) performance statistics of VRA2016 and complementary runs
- [Exceedances](exceedances.ipynb) on VRA2016 and complementary runs

## Datasets
- `eeaVRA`: validated surface obs for data assimilation
- `eeaVAL`: validated surface obs for model evaluataion
- `cifsBC`: CIFS boundary conditions
- `emepHC`: hindcast run (no DA), operational version (CAMS50.201801)
- `emepSS`: hindcast run (no DA), operational version (CAMS50.201801)
- `emepEM`: hindcast run (no DA), operational version (CAMS50.201801), new TNO-CAMS 2015 emissions
- `emepCM09`: hindcast run (no DA), development version (dev@59c7d07), EMEP 2009 chemical mechanism (EmChem09)
- `emepCM16`: hindcast run (no DA), development version (dev@59c7d07), EMEP 2016 chemical mechanism (EmChem16x)
- `emepAN`: (re)analysis run (DA: NO2,O3,SO2), operational version (CAMS50.201801; DA16)
- `emepCO`: (re)analysis run (DA: NO2,O3,SO2,CO), operational version (CAMS50.201801; DA16) low rejection threshold (350 ug/m3)
- `emepCOv2`: (re)analysis run (DA: NO2,O3,SO2,CO), operational version (CAMS50.201801; DA16) higher rejection threshold (700 ug/m3)
- `emepPM`: (re)analysis run (DA: NO2,O3,SO2,PM25,PM10), development version (CAMS50.201801; DA17 PM2.5/10 wo/feedback)
- `emepPMv2`: (re)analysis run (DA: NO2,O3,SO2,PM25,PM10), development version (CAMS50.201801; DA17 PM2.5 wo/feedback, PM10 w/feedback)
- `emepPMv3`: (re)analysis run (DA: NO2,O3,SO2,CO,PM10), development version (CAMS50.201801; DA17 PM10 w/feedback, no PM2.5)


#### conda environment at work
The notebooks and scripts on this folder use pandas and geoviews modules.
This are privided by the altair environment on PPI/lustre.

Activate this environment before you start the notebook as follows:
```bash
# load anaconda module
module load aerocom/anaconda3-stable

# activate enviroment
source activate geoviews

# start jupyter notebook
jupyter notebook --no-browser --ip=$HOSTNAME.met.no
```
