import os
import time


dates = ["202206", "202209"]
utms = ["UTM10", "UTM11"]
# rasters = ["point_density", "point_intensity", "surface_model"]
rasters = ["point_density_all_points", "point_intensity_all_points"]

for date in dates:
    for utm in utms:
        for raster in rasters:
            dir_tiles = r"C:\\Users\\khafen\\DOI\\CDI - Toil Working Group - CDI_TOIL\\TOIL\\derived\\{0}\\{1}\\raster\\{2}".format(date, utm, raster)
            fn_out = '"C:\\Users\\khafen\\DOI\\CDI - Toil Working Group - CDI_TOIL\\TOIL\derived\\{0}\\{1}\\raster\\{2}.tif"'.format(date, utm, raster)
            fn_list = '"C:\\Users\\khafen\\DOI\\CDI - Toil Working Group - CDI_TOIL\\TOIL\\derived\\{0}\\{1}\\raster\\{2}\\tif_list.txt"'.format(date, utm, raster)
            cmd_txt = '"gdal_merge.py -o {} --optfile {}'
            cmd_txt = cmd_txt.format(fn_out, fn_list)
            t0 = time.time()
            print('STARTING:', date, utm , raster)
            os.chdir(dir_tiles)
            os.system(cmd_txt)
            print('DONE', time.time() - t0)

