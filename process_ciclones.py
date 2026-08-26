import geopandas as gpd
import json
import os

os.makedirs('data/riesgos', exist_ok=True)

gdf = gpd.read_file('data/HIDRO_Ciclon_tropical_vulnerabilidad.shp')

vul_col = None
for col in gdf.columns:
    if col.lower() in ['vuln', 'vulnerabil', 'nivel', 'riesgo', 'grado']:
        vul_col = col
        break

if vul_col is None:
    print("Columns:", gdf.columns)
else:
    print(f"Vulnerability column found: {vul_col}")
    print(gdf[vul_col].unique())
    
    levels = gdf[vul_col].unique()
    for level in levels:
        if level is None: continue
        clean_level = str(level).replace(' ', '').replace('ó', 'o').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ú', 'u')
        subset = gdf[gdf[vul_col] == level]
        if subset.crs and subset.crs.to_string() != 'EPSG:4326':
            subset = subset.to_crs('EPSG:4326')
            
        json_data = subset.to_json()
        
        js_content = f"var json_Ciclones_{clean_level} = {json_data};"
        with open(f"data/riesgos/Ciclones_{clean_level}.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Saved data/riesgos/Ciclones_{clean_level}.js")
