import pandas as pd
from gdptools import ODAPCatData
import xarray as xr

cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
params = pd.read_json(cat_params)
grids = pd.read_json(cat_grid)

print(params.loc[params['id'] == 'daymet4', ['id', 'variable', 'long_name', 'URL']])


fn_nc = r"C:\Users\khafen\Downloads\daymet_v4_daily_na_prcp_1980.nc"

xr.open_dataset(fn_nc)