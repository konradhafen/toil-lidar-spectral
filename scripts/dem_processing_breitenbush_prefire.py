import richdem as rd
import os


wd = r"C:\Users\khafen\OneDrive - DOI\main\Data\TOIL\elevation\breitenbush_pre_fire"
fn_dem = os.path.join(wd, "be_devils_creek.tif")
fn_hydro = os.path.join(wd, "be_devils_creek_hydro.tif")

hydro = rd.LoadGDAL(fn_hydro)

dem = rd.LoadGDAL(fn_dem)
hydro = rd.BreachDepressions(dem, in_place=False)
hydro = rd.FillDepressions(dem, epsilon=True, in_place=False)

rd.SaveGDAL(fn_hydro, hydro)