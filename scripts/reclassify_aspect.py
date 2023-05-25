from osgeo import gdal
import numpy as np


fn_aspect = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\aspect.tif"
fn_south = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\aspect_south.tif"
fn_west = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\aspect_west.tif"
fn_cat = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\1709\aspect_4cat.tif"

driver = gdal.GetDriverByName("GTiff")

ds_aspect = gdal.Open(fn_aspect)
ds_south = driver.CreateCopy(fn_south, ds_aspect)
ds_west = driver.CreateCopy(fn_west, ds_aspect)
ds_cat = driver.CreateCopy(fn_cat, ds_aspect)

aspect = ds_aspect.GetRasterBand(1).ReadAsArray()
ndv = ds_aspect.GetRasterBand(1).GetNoDataValue()

south = np.where((aspect > 90.) & (aspect < 270.), 1, 0)
south = np.where(aspect == ndv, ndv, south)
ds_south.GetRasterBand(1).WriteArray(south)

west = np.where((aspect > 180.) & (aspect < 360.), 1, 0)
west = np.where(aspect == ndv, ndv, west)
ds_west.GetRasterBand(1).WriteArray(west)

aspect[np.where((aspect >= 0.0) & (aspect <= 90.0))] = 1
aspect[np.where((aspect > 90.0) & (aspect <= 180.0))] = 2
aspect[np.where((aspect > 180.0) & (aspect <= 270.0))] = 3
aspect[np.where((aspect > 270.0) & (aspect <= 360.0))] = 4
ds_cat.GetRasterBand(1).WriteArray(aspect)

ds_cat = None
ds_west = None
ds_south = None
ds_aspect = None