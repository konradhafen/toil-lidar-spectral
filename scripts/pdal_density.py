from osgeo import gdal
import pdal
import pandas as pd
import os


dir_las = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\point_cloud\tilecls\UTM10"
dir_den = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\point_density_ground\UTM10"
dir_int = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\point_intensity_ground\UTM10"
dir_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydroflattened"

fn_tiles = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\Tile_Schemas\00a_Breitenbush\breitenbush_tiles.csv"

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
    pipeline |= pdal.Filter.range(limits="NumberOfReturns[1:1], Classification[1:2]")
    pipeline |= pdal.Filter.radialdensity(radius=1.0)
    pipeline |= pdal.Writer.gdal(filename=os.path.join(dir_den, tile + '.tif'), dimension="RadialDensity", output_type="mean", resolution=0.5, origin_x=oX, origin_y=oY, width=ds.RasterXSize, height=ds.RasterYSize)
    pipeline != pdal.Writer.gdal(filename=os.path.join(dir_int, tile + '.tif'), dimension="Intensity", output_type="mean", resolution=0.5, origin_x=oX, origin_y=oY, width=ds.RasterXSize, height=ds.RasterYSize)
    
    ds = None
    
    count = pipeline.execute()
    metadata = pipeline.metadata
    log = pipeline.log
    print(log)
    i += 1
    print(i, 'of', len(tiles), 'DONE')

