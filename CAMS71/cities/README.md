# [CAMS71][cams71]

> The CAMS Policy Portal provides an overview of the information and services available of interest for policy users.
>
> Information, products and tools are intended to identify the contribution of different sources to exceedances of air quality limit values and to help in the design of policy responses to prevent severe air pollution episodes.

[cams71]: http://policy.atmosphere.copernicus.eu

## City definitions
On the first prototypes, the city definitions were derived from the
administrative boundaries found on [GADM][].
Then, the city boundaries were exctended to match the
[EMEP/MSC-W model][emepctm] domain used for on the ensemble simulations.
See [notebook](GADM%20with%20GeoPandas.ipynb) and [script](GADM.py).

On the next version of the service, the city defiitions will be simplified
to a 3x3 model grids arround the city centre.
See [notebook](Natural%20Earth%20with%20GeoPandas.ipynb) and [script](grid9.py).

[GADM]: https://gadm.org
[emepctm]: https://github.com/metno/emep-ctm

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
