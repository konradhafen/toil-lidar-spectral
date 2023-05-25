from osgeo import gdal
import numpy as np


fn_out = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\streams\breitenbush\streams_from_channel_heads_d8_mask.tif"
fn_in = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\streams\breitenbush\streams_from_channel_heads_d8.tif"

driver = gdal.GetDriverByName("GTiff")
ds_src = gdal.Open(fn_in)
ds_out = driver.CreateCopy(fn_out, ds_src)
nd = ds_out.GetRasterBand(1).GetNoDataValue()
data = ds_out.GetRasterBand(1).ReadAsArray()
data = np.where(data > 0, 1, nd)
ds_out.GetRasterBand(1).WriteArray(data)
ds_out = None