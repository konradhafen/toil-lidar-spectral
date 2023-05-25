import pandas as pd
import geopandas as gpd
from gdptools import WeightGen, AggGen, ODAPCatData
import time
import os


t0 = time.time()

cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
fn_cats = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\hja_study_area\NHDPlusCatchment_HJA.shp"
out_path = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\predictors"
catchments = gpd.read_file(fn_cats)
print("CRS:", catchments.crs)
params = pd.read_json(cat_params)
grids = pd.read_json(cat_grid)
agg_writer = "csv"
file_prefix = "gridmet"
fn_weights = os.path.join(out_path, 'weights', file_prefix + '_weights.' + agg_writer)
replace = {"%": 'percent', "W m-2": 'W-per-m2', 'kg/kg': 'kg-per-kg', 'm/s': 'm-per-s'}


# Create a dictionary of parameter dataframes for each variable
_id = "gridmet"
tvars = ["tmmn", "tmmx", "pr", "rmin", "rmax", "srad", "vs", "pet", "etr", "sph", "vpd"]
var_params = [params.query("id == @_id & variable == @_var").to_dict(orient="records")[0] for _var in tvars]

param_dict = dict(zip(tvars, var_params))

# Create a dictionary of grid dataframes for each variable
var_grid = []
for var in tvars:
    gridid = param_dict.get(var).get("grid_id")
    var_grid.append(grids.query("grid_id == @gridid").to_dict(orient="records")[0])
grid_dict = dict(zip(tvars, var_grid))

user_data = ODAPCatData(
    param_dict=param_dict,
    grid_dict=grid_dict,
    f_feature=catchments,
    id_feature='GridCode',
    period=["1980-01-01", "2020-12-31"]
)

wght_gen = WeightGen(
    user_data=user_data,
    method="parallel",
    output_file=fn_weights,
    weight_gen_crs=6931
)

wghts = wght_gen.calculate_weights()

agg_gen = AggGen(
    user_data=user_data,
    stat_method="masked_mean",
    agg_engine="serial",
    agg_writer=agg_writer,
    weights=fn_weights,
    out_path=out_path,
    file_prefix=file_prefix
)
ngdf, ds_out = agg_gen.calculate_agg()

df = pd.read_csv(os.path.join(out_path, file_prefix + '.' + agg_writer))
df_counts = df.groupby(['varname', 'units'], as_index=False).size()
df_counts.replace(replace, inplace=True)

varnames = df_counts['varname'].values.tolist()

for v in varnames:
    df_temp = df.loc[df['varname'] == v]
    df_temp.drop(df.columns[[0, 1, 3, 4]], axis=1, inplace=True)
    u = df_counts.loc[df_counts['varname'] == v, 'units'].values
    print('units:', u, type(u))
    df_temp.to_csv(os.path.join(out_path, 'variables', file_prefix + "_" + v + "_" + u[0] + "_1980-2020.csv"), index=False)

tEnd = time.time()
print("Total time:", tEnd - t0)