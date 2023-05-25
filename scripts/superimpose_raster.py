from osgeo import gdal
import os

fn_base = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent.tif"
fn_si = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced\be_streamenforced_hydro_concurrent.tif"
fn_out = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced\be_streamenforced_hydro_superimposed.tif"

driver = gdal.GetDriverByName("GTiff")

ds_base = gdal.Open(fn_base)
ds_si = gdal.Open(fn_si)
ds_out = driver.CreateCopy(fn_out, ds_base, strict=1)

data_out = ds_out.GetRasterBand(1).ReadAsArray()
data_si = ds_si.GetRasterBand(1).ReadAsArray()

data_out[data_si > 0.0] = data_si[data_si > 0]

ds_out.GetRasterBand(1).WriteArray(data_out)
ds_out = None