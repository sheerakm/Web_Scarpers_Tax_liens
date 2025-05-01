from shapely.geometry import Point
# import geopandas as gpd
#
# # Load shapefile
# shapefile_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\miscellaneous\geolocating\tl_2024_us_county\tl_2024_us_county.shp"
# gdf = gpd.read_file(shapefile_path)
#
# # Ensure CRS is WGS 84 (EPSG:4326)
# if gdf.crs is None:
#     print("Warning: Shapefile has no CRS.")
# else:
#     gdf = gdf.to_crs(epsg=4326)
#
# # Create Spatial Index
# gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.simplify(0.0001))  # Reduce complexity slightly
# gdf_sindex = gdf.sindex  # Create spatial index
#
#
# def return_if_in_county(c, latitude, longitude):
#     point = Point(longitude, latitude)  # Longitude first!
#
#     # Fast bounding box filter using spatial index
#     possible_matches_index = list(gdf_sindex.intersection(point.bounds))
#
#     # Check only the filtered geometries
#     possible_matches = gdf.iloc[possible_matches_index]
#
#     # Perform accurate point-in-polygon test
#     county = possible_matches[possible_matches.contains(point)]
#
#     if not county.empty and county.iloc[0]['NAME'].lower() == c.lower():
#         return True
#     return False
#
#
# print(return_if_in_county('los angeles', 34, -118))

# import pickle
# import geopandas as gpd
#
# # Load shapefile
# shapefile_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\miscellaneous\geolocating\tl_2024_us_county\tl_2024_us_county.shp"
# gdf = gpd.read_file(shapefile_path)
#
# # Ensure CRS is WGS 84 (EPSG:4326)
# if gdf.crs is None:
#     print("Warning: Shapefile has no CRS.")
# else:
#     gdf = gdf.to_crs(epsg=4326)
#
# # Create Spatial Index (if not already created)
# gdf_sindex = gdf.sindex
#
# # Save the spatial index to a pickle file
# with open("spatial_index.pkl", "wb") as f:
#     pickle.dump(gdf_sindex, f)

import pickle
import geopandas as gpd

# Load shapefile
shapefile_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\miscellaneous\geolocating\tl_2024_us_county\tl_2024_us_county.shp"
gdf = gpd.read_file(shapefile_path)

# Ensure CRS is WGS 84 (EPSG:4326)
if gdf.crs is None:
    print("Warning: Shapefile has no CRS.")
else:
    gdf = gdf.to_crs(epsg=4326)

# Load the spatial index from the pickle file
with open("spatial_index.pkl", "rb") as f:
    gdf_sindex = pickle.load(f)


def return_if_in_county(c, latitude, longitude):
    point = Point(longitude, latitude)  # Longitude first!

    # Fast bounding box filter using spatial index
    possible_matches_index = list(gdf_sindex.intersection(point.bounds))

    # Check only the filtered geometries
    possible_matches = gdf.iloc[possible_matches_index]

    # Perform accurate point-in-polygon test
    county = possible_matches[possible_matches.contains(point)]

    if not county.empty and county.iloc[0]['NAME'].lower() == c.lower():
        return True
    return False


print(return_if_in_county('los angeles', 34, -118))


