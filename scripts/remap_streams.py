from osgeo import gdal
import numpy as np
import os


dir_in = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10"
fn_streams = 'be_devils_creek_concurrent_superimposed_fac_ch_esri.tif'
fn_out = 'be_devils_creek_concurrent_superimposed_fac_ch_esri_remap.tif'

driver = gdal.GetDriverByName('GTiff')

ds = gdal.Open(os.path.join(dir_in, fn_streams))
# ds_out = driver.CreateCopy(os.path.join(dir_in, fn_out), ds)

xsize = ds.RasterXSize
ysize = ds.RasterYSize

ds_out = driver.Create(os.path.join(dir_in, fn_out), xsize=xsize, ysize=ysize, eType=gdal.GDT_Byte)
print(type(ds_out), xsize, ysize)

nd = 0
dat = ds.GetRasterBand(1).ReadAsArray()
print(dat.shape, dat.max(), dat.min())
dat = np.where(dat >= 1, 1, nd)
print(dat.shape, dat.max(), dat.min())
ds_out.GetRasterBand(1).WriteArray(dat)
ds_out.GetRasterBand(1).SetNoDataValue(nd)

ds_out.SetGeoTransform(ds.GetGeoTransform())
ds_out.SetProjection(ds.GetProjection())
ds_out = None