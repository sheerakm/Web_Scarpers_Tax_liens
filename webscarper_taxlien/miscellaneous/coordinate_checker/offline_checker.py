import geopandas as gpd
from shapely.geometry import Point

# Load and prepare state geometries
import geopandas as gpd

# Load state shapefile and normalize
states = gpd.read_file(
    r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\miscellaneous\coordinate_checker\tl_2021_us_state\tl_2021_us_state.shp"
).to_crs(epsg=4326)
states["NAME"] = states["NAME"].str.lower()

# Load county shapefile
counties = gpd.read_file(
    r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\miscellaneous\coordinate_checker\tl_2021_us_county\tl_2021_us_county.shp"
).to_crs(epsg=4326)

# Map STATEFP to state name
state_fips_to_name = states.set_index("STATEFP")["NAME"]
counties["STATE_NAME"] = counties["STATEFP"].map(state_fips_to_name)

# Normalize names
counties["STATE_NAME"] = counties["STATE_NAME"].str.lower()
counties["NAME"] = counties["NAME"].str.lower()


def is_point_in_county(lat, lon, state_name, county_name):
    point = Point(lon, lat)
    state_name = state_name.lower()
    county_name = county_name.lower()

    # Filter to the specific county in the state
    subset = counties[
        (counties['STATE_NAME'] == state_name) &
        (counties['NAME'] == county_name)
    ]

    if subset.empty:
        return False

    return subset.iloc[0].geometry.contains(point)

def get_county_for_point(lat, lon):
    point = Point(lon, lat)
    match = counties[counties.contains(point)]
    if match.empty:
        return {"county": 'outside'}
    return {
        "county": match.iloc[0]['NAME'],
        "state": match.iloc[0]['STATE_NAME']
    }


# print(get_county_for_point(33.38, -117.45))
#
# exit()
def is_point_in_state(lat, lon, state_name):
    point = Point(lon, lat)
    state_name = state_name.lower()

    # Filter to the specific state
    state_row = states[states['NAME'] == state_name]
    if state_row.empty:
        return False  # Invalid state name

    return state_row.iloc[0].geometry.contains(point)


def get_state_for_point(lat, lon):
    point = Point(lon, lat)
    match = states[states.contains(point)]
    if match.empty:
        return 'Outside'
    return match.iloc[0]['NAME']


#
#
# print(get_state_for_point(40.7128, -74.0060))  # 'New York'
#
#
# print(is_point_in_state(34.05, -168.25, "California"))  # True
# print(is_point_in_state(34.05, -118.25, "Texas"))       # False
# print(is_point_in_state(40.0, -75.0, "Pennsylvania"))   # True
#
# print(get_state_for_point(48.2, -124.58))

if __name__ == '__main__':
    import json

    import firebase_admin
    from firebase_admin import credentials, firestore


    # Initialize Firebase
    cred = credentials.Certificate(
        "../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db = firestore.client()

    # Read the Excel file

    # county_doc_ref = db.collection("States").document("California").collection("Counties").document(
    #     'Los Angeles')


    states_ref = db.collection("States")
    states_docs = states_ref.stream()
    print("WTF")

    for state in states_docs:
        state_id = state.id
        if state_id.lower() < "new york":
            continue
        print(state_id)
        counties_ref = states_ref.document(state_id).collection("Counties")
        counties_doc = counties_ref.stream()

        for county in counties_doc:
            county_id = county.id
            parcels_ref = counties_ref.document(county_id).collection("Parcels")
            parcels = parcels_ref.stream()

            for parcel in parcels:
                parcel_id = parcel.id
                parcel_data = parcel.to_dict()
                print('---------------')
                print(parcel_data)

                lon = parcel_data.get("longitude")
                lat = parcel_data.get("latitude")


                if "longitude" in parcel_data and "latitude" in parcel_data:
                    if parcel_data.get("longitude") and parcel_data.get("latitude"):
                        print(lat, lon)
                        print(get_county_for_point(float(lat), float(lon))['county'].lower(), '1')
                        print(county_id, '2')
                        if get_county_for_point(float(lat), float(lon))['county'].lower() != county_id.lower():

                            print('deleted')
                            parcels_ref.document(parcel_id).update({
                                "longitude": None,
                                "latitude": None
                            })
                        else:
                            print("didn't delete")

