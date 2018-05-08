#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define model subdomains (lonlat boxes) for cams71 cities.
City/region coorninates from from [Natural Earth](http://www.naturalearthdata.com).

To run on PPI/lustre:
module load aerocom/anaconda3-stable
source activate geoviews

Development notebook at:
https://github.com/avaldebe/pynb/blob/master/CAMS71/cities/Natural%20Earth%20with%20GeoPandas.ipynb
"""

import numpy as np
import pandas as pd
import shapely as shp
import geopandas as gpd

from io import StringIO

"""
# Populated Places
> City and town points, from Tokyo to Wasilla, Cairo to Kandahar
http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/

"""
ne10m = '/lustre/storeB/project/fou/kl/emep/CAMS71/NE10m/ne_10m_populated_places_simple.shp'
ne = gpd.read_file(ne10m)

## Define cities

cities = """
Paris Berlin Athens Budapest Reykjavik
Dublin Rome Riga Vilnius Luxembourg
Valletta Amsterdam Rotterdam Oslo Warsaw
Lisbon Bucharest Bratislava Ljubljana Barcelona
Madrid Stockholm Bern Zurich London
Milan Lille Lyon Frankfurt
""".strip().split()

gdf = ne[ne.nameascii.isin(cities)][['nameascii','geometry']].rename(columns={'nameascii':'city'})
# Some cities are defined twice, with some quite strange locations

## Model grid

# MACC14 grid midpoints
grid = dict(
    x=dict(start=-30, stop=45, step=0.25 , name='lon', units='degrees_east'),
    y=dict(start= 30, stop=76, step=0.125, name='lat', units='degrees_north'),
)

# boundaries (first/last)
first_bnd = lambda start, step, **kwa: start-step*0.5
last_bnd = lambda stop, step, **kwa: stop+step*0.5

x0, x1 = first_bnd(**grid['x']), last_bnd(**grid['x'])
y0, y1 = first_bnd(**grid['y']), last_bnd(**grid['y'])

# model domain
domain = shp.geometry.Polygon([(x0,y0), (x0,y1), (x1,y1), (x1,y0)])

# discard points outside of the mkodel domain
df = gdf[gdf.within(domain)].copy().set_index('city').reindex(cities)
df['x'] = df.geometry.apply(lambda x: x.coords[0][0])
df['y'] = df.geometry.apply(lambda x: x.coords[0][1])

### 3x3 grid area

# 1st boundary
for k,v in grid.items():
    grid[k]['first'] = first_bnd(**v)

# round up/down to grid
minb = lambda x, first, step, **kwa: x-np.remainder(x-first,step)
maxb = lambda x, first, step, **kwa: minb(x+step,first,step)

# 1x1 grid:
df['minx'] = minb(df.x, **grid['x'])
df['miny'] = minb(df.y, **grid['y'])
df['maxx'] = maxb(df.x, **grid['x'])
df['maxy'] = maxb(df.y, **grid['y'])

# 3x3 grid
df['minx'] -= grid['x']['step']
df['miny'] -= grid['y']['step']
df['maxx'] += grid['x']['step']
df['maxy'] += grid['y']['step']

df.rename(
    columns=dict(minx='lon0',maxx='lon1',miny='lat0',maxy='lat1'),
    inplace=True,
)
df = df[['lon0','lon1','lat0','lat1']]
print(df)

# Write to file
df.to_csv('cams71city_9grid.csv', sep=',')

