import pandas as pd
import geopandas as gpd

# Load GeoJSON file
geojson_file = 'water/water.geojson'
gdf = gpd.read_file(geojson_file)

# Load CSV file
csv_file = 'water/water.csv'
csv_data = pd.read_csv(csv_file)

# Step 1: Check geometry types in GeoJSON
print(gdf.geom_type.value_counts())  # This will tell you the types of geometries (e.g., Point, Polygon)

# Step 2: Extract coordinates
# For Points, you can directly use .x and .y
if gdf.geometry.iloc[0].geom_type == 'Point':  # Check if all geometries are Point
    gdf['longitude'] = gdf.geometry.x
    gdf['latitude'] = gdf.geometry.y
else:
    # For Polygons or MultiPolygons, use the centroid to get a representative point
    gdf['longitude'] = gdf.geometry.centroid.x
    gdf['latitude'] = gdf.geometry.centroid.y

# Step 3: Merge with CSV (assuming the Shape__Area is in the CSV)
combined_df = pd.concat([gdf[['longitude', 'latitude']], csv_data], axis=1)

# Step 4: Filter Out Small Lakes
combined_df = combined_df[combined_df['Shape__Area'] >= 100000000]
combined_df = combined_df[combined_df['perennial'] == "Perennial"]
rows, columns = combined_df.shape

print(f"Number of rows: {rows}")

# Step 4: Save the combined data to a new CSV
output_file = 'combined_output.csv'
combined_df.to_csv(output_file, index=False)

print(f"Combined data saved to {output_file}")
