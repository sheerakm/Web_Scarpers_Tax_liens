from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode("3302 S Harwood St, Dallas TX 75215-3434 ")



print(location.latitude, location.longitude)

location = geolocator.geocode("3302 S Harwood St, Dallas TX ")

print(location.latitude, location.longitude)
