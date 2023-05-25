from whitebox import WhiteboxTools
import os

wbt = WhiteboxTools()
wbt.set_whitebox_dir('C:/WBT')

wd = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced"
fn_dem = os.path.join(wd, "be_streamenforced_roadbreach.tif")
fn_fil = os.path.join(wd, "be_streamenforced_roadbreach_fill.tif")
fn_d8 = os.path.join(wd, "be_streamenforced_roadbreach_d8.tif")

# wbt.fill_depressions(fn_dem, fn_fil, fix_flats=True)
wbt.d8_pointer(fn_dem, fn_d8)

print('DONE')
