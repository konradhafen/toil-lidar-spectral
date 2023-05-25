from osgeo import gdal
import numpy as np

fn_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent.tif"
fn_dist = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\streams\breitenbush\distance_to_stream_d8_concurrent.tif"
fn_out = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent_burn.tif"

driver = gdal.GetDriverByName("GTiff")
ds_dem = gdal.Open(fn_dem)
ds_dist = gdal.Open(fn_dist)
ds_out = driver.CreateCopy(fn_out, ds_dem)

data_dist = ds_dist.GetRasterBand(1).ReadAsArray()
ds_out.GetRasterBand(1).SetNoDataValue(-9999.0)
data_out = ds_out.GetRasterBand(1).ReadAsArray()

maxdist = data_dist.max()
maxdepth = 100.0

# data_out[data_dist >= 0] = data_out[data_dist >= 0] - ((data_dist[data_dist >= 0] - maxdist) / maxdist) * maxdepth
print(data_out.shape, data_dist.shape)
data_out = np.where(data_dist >= 0.0, data_out + ((data_dist - maxdist) / maxdist) * maxdepth, data_out)

ds_out.GetRasterBand(1).WriteArray(data_out)

ds_out = None
