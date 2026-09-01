import geopandas as gpd
import json
import os
import sys

os.makedirs('data/riesgos', exist_ok=True)

try:
    gdf = gpd.read_file('data/HIDRO_Inund_fluv_riesgo.shp')
except Exception as e:
    print(f"Error reading shapefile: {e}")
    sys.exit(1)

# The user's QGIS map was actually colored using the PELIGRO column, 
# not RIESGO, which is why the red zones were missing.
risk_col = 'PELIGRO'

if risk_col not in gdf.columns:
    print("Columns:", gdf.columns)
else:
    print(f"Risk column found: {risk_col}")
    print(gdf[risk_col].unique())
    
    levels = gdf[risk_col].unique()
    for level in levels:
        if level is None: continue
        clean_level = str(level).replace(' ', '').replace('ó', 'o').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ú', 'u')
        subset = gdf[gdf[risk_col] == level]
        if subset.crs and subset.crs.to_string() != 'EPSG:4326':
            subset = subset.to_crs('EPSG:4326')
            
        json_data = subset.to_json()
        
        js_content = f"var json_Inundacion_{clean_level} = {json_data};"
        with open(f"data/riesgos/Inundacion_{clean_level}.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Saved data/riesgos/Inundacion_{clean_level}.js")
