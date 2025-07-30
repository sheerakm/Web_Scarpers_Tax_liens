from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapi")


def convert_location_to_x_y(address):
    geolocator = Nominatim(user_agent="geoapi", timeout= 2)

    location = geolocator.geocode(address)
    if location:


        return location.latitude, location.longitude
    else:
        return None, None


print(convert_location_to_x_y('500 EAST 147 STREET Bronx, NY 10455'))

