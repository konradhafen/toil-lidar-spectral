import richdem as rd
import os
from pysheds.grid import Grid
import geopandas as gpd


dir_src = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced"
dir_der = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\digitized"
dir_out = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\streams\breitenbush"

fn_dem = os.path.join(dir_src, "be_streamenforced_hydro.tif")  # hydrologically altered dem from dem processing script
fn_head = os.path.join(dir_der, "channel_heads_breitenbush.tif")  # raster of channel heads
fn_chn = os.path.join(dir_out, 'streams_from_channel_heads_d8.tif')

overwrite = False

if not os.path.exists(fn_chn) or overwrite:
    dem = rd.LoadGDAL(fn_dem)
    chd = rd.LoadGDAL(fn_head)
    accum = rd.FlowAccumulation(dem, method='D8', weights=chd)
    rd.SaveGDAL(fn_chn, accum)


grid = Grid.from_raster(fn_dem)
dem = grid.read_raster(fn_dem)
chn = grid.read_raster(fn_chn)

dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
fdr = grid.flowdir(dem, dirmap=dirmap)
branches = grid.extract_river_network(fdr, chn>=1, dirmap=dirmap)

print(type(branches))

gdf = gpd.GeoDataFrame.from_features(branches['features'])
# print(branches)
print(gdf.shape)
# print(gdf.columns)
gdf.to_file(os.path.join(dir_out, 'network.gpkg'))