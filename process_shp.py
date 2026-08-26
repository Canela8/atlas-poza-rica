import geopandas as gpd
import json
import os

os.makedirs('data/riesgos', exist_ok=True)

# Read the shapefile
gdf = gpd.read_file('data/HIDRO_Inund_fluv_vulnerabilidad.shp')

# Find the vulnerability column
vul_col = None
for col in gdf.columns:
    if col.lower() in ['vuln', 'vulnerabil', 'nivel', 'riesgo', 'grado', 'vuln_fis', 'vuln_f']:
        vul_col = col
        break

if vul_col is None:
    print("Columns:", gdf.columns)
    for col in gdf.select_dtypes(include=['object']):
        print(f"{col}: {gdf[col].unique()}")
else:
    print(f"Vulnerability column found: {vul_col}")
    print(gdf[vul_col].unique())
    
    # Save a geojson for each level
    levels = gdf[vul_col].unique()
    for level in levels:
        if level is None: continue
        # Format the name
        clean_level = str(level).replace(' ', '').replace('ó', 'o').replace('á', 'a').replace('í', 'i').replace('é', 'e').replace('ú', 'u')
        subset = gdf[gdf[vul_col] == level]
        # Reproject to WGS84 (EPSG:4326) if it's not already
        if subset.crs and subset.crs.to_string() != 'EPSG:4326':
            subset = subset.to_crs('EPSG:4326')
            
        json_data = subset.to_json()
        
        # Write JS file
        js_content = f"var json_Inundacion_{clean_level} = {json_data};"
        with open(f"data/riesgos/Inundacion_{clean_level}.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Saved data/riesgos/Inundacion_{clean_level}.js")

