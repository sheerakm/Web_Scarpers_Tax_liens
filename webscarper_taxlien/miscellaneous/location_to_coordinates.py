from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapi")


def convert_location_to_x_y(address):
    geolocator = Nominatim(user_agent="geoapi")

    location = geolocator.geocode(address)
    if location:


        return location.latitude, location.longitude
    else:
        return None, None


print(convert_location_to_x_y('8315 HILLCROFT DR LOS ANGELES CA 91304 2113'))

