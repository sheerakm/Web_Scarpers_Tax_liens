# untested code

from geopy.geocoders import Nominatim


# for example 'United States'

def is_coordinate_in_usa(latitude, longitude, location_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    import time
    time.sleep(1.1)
    location = geolocator.reverse((latitude, longitude), language='en', exactly_one=True)


    if location:
        # Check if 'United States' is in the address
        address = location.raw.get('address', {})
        print(address)
        country = address.get('country', '')

        if location_name in country:
            return True
        else:
            return False
    return False

latitude = 26
longitude= -80

print(is_coordinate_in_usa(latitude, longitude, 'United States'))

