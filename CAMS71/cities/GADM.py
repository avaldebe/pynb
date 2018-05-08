#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define model subdomains (lonlat boxes) for cams71 cities.
City/region administrative boundaries from [GADM](https://gadm.org).

To run on PPI/lustre:
module load aerocom/anaconda3-stable
source activate geoviews

Development notebook at:
https://github.com/avaldebe/pynb/blob/master/CAMS71/cities/GADM%20with%20GeoPandas.ipynb
"""

import numpy as np
import pandas as pd
import shapely as shp
import geopandas as gpd
from io import StringIO

# Define cities

cityDef = u"""city,ISO,adm,region
Vienna    ,AUT,2,Wien
Brussels  ,BEL,2,Bruxelles
Sofia     ,BGR,2,Stolichna
Zagreb    ,HRV,2,Zagreb
Nicosia   ,CYP,1,Nicosia
Prague    ,CZE,2,Praha - východ;Praha - západ;Praha 1;Praha 10;Praha 11;Praha 12;Praha 13;Praha 14;Praha 15;Praha 16;Praha 17;Praha 18;Praha 19;Praha 2;Praha 20;Praha 21;Praha 22;Praha 3;Praha 4;Praha 5;Praha 6;Praha 7;Praha 8;Praha 9
Copenhagen,DNK,2,København
Tallinn   ,EST,2,Tallinn
Helsinki  ,FIN,4,Helsinki
Paris     ,FRA,2,Paris;Hauts-de-Seine;Val-de-Marne;Seine-Saint-Denis
Berlin    ,DEU,1,Berlin
Athens    ,GRC,3,Athens
Budapest  ,HUN,2,Budapesti
Reykjavik ,ISL,2,Reykjavík
Dublin    ,IRL,1,Dublin
Rome      ,ITA,3,Roma
Riga      ,LVA,2,Riga
Vilnius   ,LTU,2,Vilniaus
Luxembourg,LUX,3,Luxembourg
Valletta  ,MLT,0,Malta
Amsterdam ,NLD,2,Amsterdam
Rotterdam ,NLD,2,Rotterdam
Oslo      ,NOR,2,Oslo
Warsaw    ,POL,2,Warsaw
Lisbon    ,PRT,2,Lisboa
Bucharest ,ROU,2,Municipiul Bucuresti
Bratislava,SVK,2,Bratislava I;Bratislava II;Bratislava III;Bratislava IV;Bratislava V
Ljubljana ,SVN,2,Ljubljana
Barcelona ,ESP,4,Barcelona
Madrid    ,ESP,4,Madrid
Stockholm ,SWE,2,Stockholm
Bern      ,CHE,2,Bern
Zurich    ,CHE,2,Zürich
London    ,GBR,2,Barking and Dagenham;Bexley;Brent;Bromley;Camden;Croydon;Ealing;Enfield;Greenwich;Hackney;Hammersmith and Fulham;Haringey;Harrow;Havering;Hillingdon;Hounslow;Islington;Lambeth;Lewisham;Merton;Newham;Redbridge;Richmond upon Thames;Southwark;Sutton;Tower Hamlets;Waltham Forest;Wandsworth
Milan     ,ITA,3,Milano
Lille     ,FRA,3,Lille
Lyon      ,FRA,3,Lyon
Frankfurt ,DEU,2,Frankfurt am Main
"""

df = pd.read_csv(
    StringIO(cityDef), sep=',', index_col='city',
    converters=dict(
        city=str.strip,
        region=lambda x: x.split(';'),
    )
)

# GADM
"""
GADM provides maps and spatial data for all countries and their sub-divisions.
You can browse our maps or download the data to make your own maps.
  https://gadm.org/index.html

[...] the whole world you can download version 2.8 as a single layer
[ESRI geodatabase](https://biogeo.ucdavis.edu/data/gadm2.8/gadm28.gdb.zip)
[...]
  https://gadm.org/download_world.html
"""
gdb = '/lustre/storeB/project/fou/kl/emep/CAMS71/gadm28.gdb.zip'
print('reading %s'%gdb)
gadm = gpd.read_file(gdb)

# Select cities

region = list(df.ISO)
vnames = 'ISO geometry NAME_0 NAME_1 NAME_2 NAME_3 NAME_4'.split()
region = gadm[gadm['ISO'].isin(region)][vnames]

region['city'] = ''
print('Shapes by city/region:')
for city, row in df.iterrows():
    key = 'NAME_%s'%row.adm
    ind = region[key].isin(row.region)
    region.loc[ind,'city'] = city
    print("  %-10s %3d"%(city,sum(ind)))

region = region[region.city !='']

## City boundary box, one shape by city/region

gdf = region.dissolve(by='city').geometry.bounds
df = gdf[['minx','maxx','miny','maxy']].reindex(df.index)

# Model grid

## MACC14 grid midpoints
grid = dict(
    x=dict(start=-30, stop=45, step=0.25 , name='lon', units='degrees_east'),
    y=dict(start= 30, stop=76, step=0.125, name='lat', units='degrees_north'),
)

## 1st boundary
first_bnd = lambda start, step, **kwa: start-step*0.5
for k,v in grid.items():
    grid[k]['first'] = first_bnd(**v)

## round up/down to grid
minb = lambda x, first, step, **kwa: x-np.remainder(x-first,step)
maxb = lambda x, first, step, **kwa: minb(x+step,first,step)

df['minx'] = minb(df.minx, **grid['x'])
df['miny'] = minb(df.miny, **grid['y'])
df['maxx'] = maxb(df.maxx, **grid['x'])
df['maxy'] = maxb(df.maxy, **grid['y'])

df.rename(
    columns=dict(minx='lon0',maxx='lon1',miny='lat0',maxy='lat1'),
    inplace=True,
)
print(df)

# Write to file
df.to_csv('cams71city_GADM.csv', sep=',')
