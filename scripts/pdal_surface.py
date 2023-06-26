from osgeo import gdal
import pdal
import pandas as pd
import os


date = "202206"
utm = "UTM11"

dir_las = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\{0}\point_cloud\tilecls\{1}".format(date, utm)
dir_dsm = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\derived\{0}\{1}\raster\surface_model".format(date, utm)
dir_dem = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\{0}\bare_earth\be_rasters\{1}\Hydroflattened".format(date, utm)

if utm == "UTM10":
    fn_tiles = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\Tile_Schemas\00a_Breitenbush\breitenbush_tiles.csv"
elif utm == "UTM11":
    fn_tiles = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\Tile_Schemas\00b_Donner_Blitzen\donner_blitzen_tiles.csv"
    if date == "202209":
        dir_dem = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\TOIL\nv5_original_data_and_reports\{0}\bare_earth\be_rasters\{1}".format(date, utm)


df_tiles = pd.read_csv(fn_tiles)
tiles = list(df_tiles['Tile'].unique())

i = 0
for tile in tiles:
    fn_dem = os.path.join(dir_dem, 'be_' + tile + '.tif')
    ds = gdal.Open(fn_dem)
    geot = ds.GetGeoTransform()
    oX = geot[0]
    oY = geot[3] + (ds.RasterYSize * geot[5])
    
    pipeline = pdal.Reader(os.path.join(dir_las, tile + '.las'))
    pipeline |= pdal.Filter.range(limits="ReturnNumber[1:1], Classification[1:2]")
    pipeline |= pdal.Filter.radialdensity(radius=1.0)
    pipeline |= pdal.Writer.gdal(filename=os.path.join(dir_dsm, tile + '.tif'), output_type="idw", resolution=0.5, origin_x=oX, origin_y=oY, width=ds.RasterXSize, height=ds.RasterYSize)
    
    ds = None
    
    count = pipeline.execute()
    metadata = pipeline.metadata
    log = pipeline.log
    print(log)
    i += 1
    print(i, 'of', len(tiles), 'DONE')

