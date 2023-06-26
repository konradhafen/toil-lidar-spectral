from osgeo import gdal, osr
import numpy as np


fn_in = r"C:\Users\khafen\OneDrive - DOI\main\Data\nhd\nhdplushr\NHDPLUS_H_1712_HU4_RASTER\HRNHDPlusRasters1712\elev_cm.tif"
fn_out = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\elevation\donner_blitzen_nhd\elev_cm_clip.tif"
fn_out2 = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\elevation\donner_blitzen_nhd\elev_cm_clip_unsampled.tif"
fn_in_lidar = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\202206\bare_earth\be_rasters\UTM11\Hydro_stream_enforced\be_streamenforced.tif"
fn_out_resize = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\elevation\nv5_derivatives\elevation\donner-blitzen\be_streamenforced_resize.tif"
fn_si = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\elevation\nv5_derivatives\elevation\donner-blitzen\superimposed.tif"

bounds_utm11 = (348000., 4733680., 367000., 4747000.)

utm11_srs = osr.SpatialReference()
utm11_srs.SetWellKnownGeogCS("NAD83")
utm11_srs.SetUTM(11, 1)

gdal.Warp(fn_out, fn_in, dstSRS=utm11_srs, xRes=0.5,  yRes=0.5, outputBounds=bounds_utm11, outputBoundsSRS=utm11_srs, resampleAlg='bilinear')
gdal.Warp(fn_out_resize, fn_in_lidar, outputBounds=bounds_utm11)

driver = gdal.GetDriverByName("GTiff")

ds_nhd = gdal.Open(fn_out)
ds_lidar = gdal.Open(fn_out_resize)
elev_nhd = ds_nhd.GetRasterBand(1).ReadAsArray()
elev_lidar = ds_lidar.GetRasterBand(1).ReadAsArray()
ndv = ds_lidar.GetRasterBand(1).GetNoDataValue()
elev_nhd = elev_nhd / 100.0
elev_lidar = np.where(elev_lidar == ndv, elev_nhd, elev_lidar)

ds_si = driver.Create(fn_si, xsize=ds_lidar.RasterXSize, ysize=ds_lidar.RasterYSize, bands=1, eType=gdal.GDT_Float32)
ds_si.SetGeoTransform(ds_lidar.GetGeoTransform())
ds_si.SetProjection(ds_lidar.GetProjection())
ds_si.GetRasterBand(1).WriteArray(elev_lidar)
ds_si.GetRasterBand(1).SetNoDataValue(ndv)

ds_si = None