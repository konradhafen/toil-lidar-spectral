import pandas as pd


fn_out = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\predictors\\variables\static_vars_nhd.csv"
fn_net = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\network\\nhd_id_gridcode_node.csv"

# read in file with all gridcodes for aoi
fn_aoi = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\predictors\\variables\static_vars.csv"
df_aoi = pd.read_csv(fn_aoi)

# read in catchments attribute table for huc4
fn_cat = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\hja_study_area\NHDPlusCatchment.csv"
df_cat = pd.read_csv(fn_cat)

# keep gridcode and NHDPlusID
df_cat = df_cat[['GridCode', 'NHDPlusID']].copy()

# subset catchments attribute table to gridcodes within aoi
df = df_cat.merge(df_aoi, left_on="GridCode", right_on="GridCode")

# read NHDPlusFlowlineVAA
fn_vaa = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\hja_study_area\NHDPlusFlowlineVAA.csv"
df_vaa = pd.read_csv(fn_vaa)
print(df_vaa.columns)

# keep total drainage area, reach length, reach slope and join
keep_cols = ['NHDPlusID', 'FromNode', 'ToNode', 'ArbolateSu', 'AreaSqKm', 'TotDASqKm', 'Slope']
df = df.merge(df_vaa[keep_cols], left_on="NHDPlusID", right_on="NHDPlusID")

# read NHDFlowline
fn_fl = r"C:\Users\khafen\DOI\CDI - Toil Working Group - CDI_TOIL\CDI\data\geospatial\nhdplushr\hja_study_area\NHDFlowline.csv"
df_fl = pd.read_csv(fn_fl)
df = df.merge(df_fl[['NHDPlusID', 'LengthKM']], left_on="NHDPlusID", right_on="NHDPlusID")

df.to_csv(fn_out, index=False)
df[['NHDPlusID', 'GridCode', 'FromNode', 'ToNode', 'LengthKM', 'ArbolateSu']].to_csv(fn_net, index=False)