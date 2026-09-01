import geopandas as gpd
import json
import os
import sys

os.makedirs('data/riesgos', exist_ok=True)

try:
    gdf = gpd.read_file('data/QUIM_Alm_sust_pel_peligro.shp')
except Exception as e:
    print(f"Error reading shapefile: {e}")
    sys.exit(1)

print("Geometry types:", gdf.geometry.type.unique())
print("Columns:", gdf.columns)
for col in ['PELIGRO', 'RIESGO', 'VULNERABIL']:
    if col in gdf.columns:
        print(f"{col} counts:")
        print(gdf.groupby(col).size())

risk_col = 'PELIGRO' if 'PELIGRO' in gdf.columns else 'RIESGO'

if risk_col not in gdf.columns:
    print("Risk column not found")
else:
    print(f"Using column: {risk_col}")
    
    levels = gdf[risk_col].unique()
    for level in levels:
        if level is None: continue
        clean_level = str(level).replace(' ', '').replace('ó', 'o').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ú', 'u')
        subset = gdf[gdf[risk_col] == level]
        if subset.crs and subset.crs.to_string() != 'EPSG:4326':
            subset = subset.to_crs('EPSG:4326')
            
        json_data = subset.to_json()
        
        js_content = f"var json_Quimicos_{clean_level} = {json_data};"
        with open(f"data/riesgos/Quimicos_{clean_level}.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Saved data/riesgos/Quimicos_{clean_level}.js")
