import richdem as rd
import os


wd = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced"
# fn_dem = os.path.join(wd, "be_streamenforced_roadbreach.tif")
fn_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent_burn.tif"
fn_fac = os.path.join(wd, "be_streamenforced_facD8.tif")
fn_fac_di = os.path.join(wd, "be_streamenforced_facDi.tif")
# fn_hydro = os.path.join(wd, "be_streamenforced_hydro.tif")
fn_hydro = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent_hydro.tif"

overwrite = False

if os.path.exists(fn_hydro) and not overwrite:
    hydro = rd.LoadGDAL(fn_hydro)

else:
    dem = rd.LoadGDAL(fn_dem)
    hydro = rd.BreachDepressions(dem, in_place=False)
    hydro = rd.FillDepressions(dem, epsilon=True, in_place=False)
fac = rd.FlowAccumulation(hydro, method='D8')
fac_di = rd.FlowAccumulation(hydro, method='Dinf')
# slope = rd.TerrainAttribute(dem, attrib="slope_degrees")
# planform_curvature = rd.TerrainAttribute(dem, attrib='planform_curvature')
# profile_curvature = rd.TerrainAttribute(dem, attrib='profile_curvature')
# curvature = rd.TerrainAttribute(dem, attrib='curvature')

# rd.SaveGDAL(fn_fac, fac)
# rd.SaveGDAL(os.path.join(wd, fn_fac_di), fac_di)
rd.SaveGDAL(fn_hydro, hydro)
# rd.SaveGDAL(os.path.join(wd, "be_streamenforced_planform.tif"), planform_curvature)
# rd.SaveGDAL(os.path.join(wd, "be_streamenforced_profile.tif"), profile_curvature)
# rd.SaveGDAL(os.path.join(wd, "be_streamenforced_curvature.tif"), curvature)
# rd.SaveGDAL(os.path.join(wd, "be_streamenforced_slope.tif"), slope)
# rd.SaveGDAL(os.path.join(wd, "be_streamenforced_pitdepth.tif"), hydro - dem)
