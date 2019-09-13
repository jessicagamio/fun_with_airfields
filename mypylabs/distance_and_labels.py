#!/usr/bin/env python3

from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import simplekml
from myairfieldpack import airport_tables


### collect user input on airfield code
def user_input(word):
    code = input("Enter " + word + " airfield code: ")
    airfield_name = airport_tables.search_airfield(code, airport_tables.dbname)
    return airfield_name + ' airport'


### run geopy to retrieve location info on airfields; arg of user input is passed
def airfield_location(code):
    geolocator = Nominatim()
    location = geolocator.geocode(code)
    location_list = list(location)
    return location_list


### pass location list info and split text; returns airfield name
def name(location_list):
    location_name = str(location_list[0])
    airfield_name = location_name.split(',')
    return airfield_name[0]


### get lat lon for location
def lat_lon(location_list):
    airfield_coordinates = location_list[-1]
    lat = airfield_coordinates[0]
    lon = airfield_coordinates[1]
    return lat, lon


### ask user for unit of measurement
def measure():
    measurement = ""
    while measurement not in ['mi', 'km', 'm', 'nm']:
        measurement = input("Unit to measure distance? Enter mi (miles), km (kilometers), m (meters), or nm (nautical miles): ")
        if measurement not in ['mi', 'km', 'm', 'nm']:
            print("Please enter a valid unit of measurement.")
    return measurement


### measure distance between 2 locations
def airfield_distance(measurement, latlon_dep, latlon_arr):
    if measurement == 'mi':
        distance = vincenty(latlon_dep, latlon_arr).miles
    elif measurement == 'km':
        distance = vincenty(latlon_dep, latlon_arr).km
    elif measurement == 'm':
        distance = vincenty(latlon_dep, latlon_arr).meters
    elif measurement == 'nm':
        distance = vincenty(latlon_dep, latlon_arr).nautical
    return distance


### get the departure airfield info
def airfield_info_departure(departure):
    location_dep = airfield_location(departure)
    name_dep = name(location_dep)
    lat_dep, lon_dep = lat_lon(location_dep)
    departure_info = (name_dep, lon_dep, lat_dep)
    return departure_info


### get the arrival airfield info
def airfield_info_arrival(arrival):
    location_arr = airfield_location(arrival)
    name_arr = name(location_arr)
    lat_arr, lon_arr = lat_lon(location_arr)
    arrival_info = (name_arr, lon_arr, lat_arr)
    return arrival_info


### get coordinates for both airfields, make label for kml
def coordinates():
    print("Let's take a trip!\n")
    for i in range(0, 2):
        if i == 0:
            print("Where are you flying out of?")
            dep = user_input('departure')
            departure_info = airfield_info_departure(dep)
            name_dep, lon_dep, lat_dep = departure_info
            latlon_dep = (lat_dep, lon_dep)
            print("You're flying from " + name_dep + "\n")
            print()
        elif i == 1:
            print("Where would you like to go?")
            arr = user_input('arrival')
            arrival_info = airfield_info_arrival(arr)
            name_arr, lon_arr, lat_arr = arrival_info
            latlon_arr = (lat_arr, lon_arr)
            print("You're landing in " + name_arr + "\n")

    route = [departure_info, arrival_info]
    m = measure()
    dist = airfield_distance(m, latlon_dep, latlon_arr)
    label = "The distance between " + name_dep + " and " + name_arr + " is " + f"{dist:0.2f} " + m
    print(label + "\n")
    print("Have a great trip! Bon voyage!")
    return route, label

def main():
    kml = simplekml.Kml()

    route, label = coordinates()

    # parsing out the route list of tuples for kml line
    name_dep, lon_dep, lat_dep = route[0]
    name_arr, lon_arr, lat_arr = route[1]

    # create variable for distance in balloon label
    distance = label

    # create kml line using departure and arrival coordinates
    line = kml.newlinestring()
    line.coords = [(lon_dep, lat_dep), (lon_arr, lat_arr)]
    line.tessellate = 1
    line.style.linestyle.width  = 3

    # creates a pop up balloon that illustrates the distance between points
    line.style.balloonstyle.text = distance
    line.style.balloonstyle.bgcolor = simplekml.Color.white
    line.style.balloonstyle.textcolor = simplekml.Color.black

    # create label and icon for route line
    for name, lon, lat in route:
        target = kml.newpoint()
        target.name = name
        target.style.iconstyle.scale = 1
        target.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/airports.png'
        target.style.iconstyle.color = simplekml.Color.red
        target.coords = [(lon, lat)]
    kml.save('airfields.kml')

if __name__ == '__main__':
    main()