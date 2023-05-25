import rasterstats
import geopandas as gpd
import pandas as pd
import numpy as np
import fiona

def features_to_df(features, keys_names):
    list_of_dicts = []
    for feat in features:
        feat_dict = {}
        for k, v in keys_names.items():
            feat_dict[v] = feat['properties'][k]
        list_of_dicts.append(feat_dict)
    return pd.DataFrame(list_of_dicts)



fn_zones = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\hja_study_area\NHDPlusCatchment_HJA_Albers.shp"
fn_aspect = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\aspect_4cat.tif"
fn_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\nhd\nhdplushr\NHDPLUS_H_1709_HU4_RASTER\HRNHDPlusRasters1709_with_fac\elev_cm.tif"
fn_curv = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\curvature.tif"
fn_slp = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\slope_percent_rise.tif"
fn_out = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\predictors\\variables\static_vars.csv"

cmap = {1: 'ne', 2: 'se', 3: 'sw', 4: 'nw'}
stats_aspect = rasterstats.zonal_stats(fn_zones, fn_aspect, geojson_out=True, categorical=True, category_map=cmap)
gdf_aspect = gpd.GeoDataFrame.from_features(stats_aspect)

df_aspect = gdf_aspect[['GridCode', 'ne', 'sw', 'nw', 'se']]
df_aspect.fillna(0, inplace=True)
df_aspect[list(cmap.values())] = df_aspect[list(cmap.values())].div(df_aspect[list(cmap.values())].sum(axis=1), axis=0)
df_aspect.columns = ['GridCode', 'aspect_ne_pct', 'aspect_sw_pct', 'aspect_nw_pct', 'aspect_se_pct']

stats_dem = rasterstats.zonal_stats(fn_zones, fn_dem, geojson_out=True, stats=['min', 'max', 'median', 'mean'])
df_dem = features_to_df(stats_dem, {"GridCode": "GridCode", "min": "elev_min_cm", "max": "elev_max_cm", "median": "elev_median_cm", "mean": "elev_mean_cm"})
df = df_aspect.merge(df_dem, left_on="GridCode", right_on="GridCode")
stats_slp = rasterstats.zonal_stats(fn_zones, fn_slp, geojson_out=True, stats=['median', 'mean'])
df_slp = features_to_df(stats_slp, {"GridCode": "GridCode", "median": "slp_median_pct", "mean": "slp_mean_pct" })
df = df.merge(df_slp, left_on="GridCode", right_on="GridCode")
stats_curv = rasterstats.zonal_stats(fn_zones, fn_curv, geojson_out=True)
df_curv = features_to_df(stats_slp, {"GridCode": "GridCode", "median": "curv_median", "mean": "curv_mean" })
df = df.merge(df_curv, left_on="GridCode", right_on="GridCode")

print(df.head())
print(df.columns)
df.to_csv(fn_out, index=False)
# print(stats_dem[0]['properties']['GridCode'], stats_dem[0]['properties'].values())
# print(gdf_dem['properties']['GridCode'])
# print(stats_dem[0].items(), stats_dem[0].keys())

# df.to_csv(fn_out, index=False)