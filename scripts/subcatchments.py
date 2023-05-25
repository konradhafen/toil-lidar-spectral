from pcraster import *

# fn_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\be_devils_creek_concurrent_superimposed.map"
fn_dem = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\rs_nv5\202206\bare_earth\be_rasters\UTM10\Hydro_stream_enforced\be_streamenforced_hydro_superimposed.map"
fn_chn = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\streams\breitenbush\streams_from_channel_heads_d8_concurrent.map"
fn_fdr = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\fdr_d8.map"
fn_sub = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire\UTM10\subcatchments.map"

overwrite = True

dem = readmap(fn_dem)
chn = readmap(fn_chn)

if os.path.exists(fn_fdr) and not overwrite:
    fdr = readmap(fn_fdr)
else:
    fdr = lddcreate(dem, 1e31, 1e31, 1e31, 1e31)
    report(fdr, fn_fdr)

junct = ifthen(downstream(fdr, chn) != chn, boolean(1))
outlets = ordinal(cover(uniqueid(junct), 0))
# subcat = catchment(fdr, outlets)
# aguila(subcat)
maxOutlets = mapmaximum(outlets)
maxOutlets = cellvalue(maxOutlets, 0, 0)
maxOutlets = maxOutlets[0]
subcat = subcatchment(fdr, outlets)
report(subcat, fn_sub)
aguila(subcat)


# for outlet in range(1, maxOutlets + 1):
#     subcat
