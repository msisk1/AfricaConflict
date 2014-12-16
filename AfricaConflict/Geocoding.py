'''
Created on Dec 8, 2014

@author: msisk1
geocoder working for a particular format
using the gadm boundary files on admin 2 to map to particular gridcells

'''

import os, geopy
from geopy import geocoders


coder = "Google"

def getGeocodedLatLong(address):
    global coder
    if coder == "Google":
        geolocator2 = geocoders.GoogleV3()
    elif coder == "OSM":
        geolocator2 = geocoders.Nominatim(timeout = 5)
    elif coder == "GeoNames":
        geolocator2 = geocoders.GeoNames(country_bias=None, username="mlsisk", timeout=1, proxies=None)
    try:
        location = geolocator2.geocode(address)
        return [ location.latitude ,location.longitude], True
    except geopy.exc.GeocoderServiceError as error_message:
        print error_message,
        return [0,0],False
    except:
        return [0,0],False
        



location = "E:\\GISWork_2\\Conflict\\Protest\\"
protest_locations = location + "Protest_Locations2.csv"
output_file = location + "Protect_Locations_Geocoded_{0}.csv".format(coder)

counter = 0

print os.path.exists(protest_locations)
reader = open(protest_locations,'r')
header = reader.readline()
out_header = "{0},{1},{2},{3},{4},{5}".format("Mod_Loc","Country","Number","code","numPlaces","Coordinates")
out_header = "{0},{1},{2},{3},{4},{5},{6},{7}".format("each_loc","Mod_Loc","Country","Number","code","numPlaces","Lat","Long")

writer = open(output_file,"w")
writer.write(out_header+"\n")
print header

for each_line in reader:
    coords = []
    counter +=1
    line_split = each_line.split(",")
    mod_loc = line_split[0]
    country = line_split[1]
    number = line_split[2]
    code = line_split[3][:-1]
    #print mod_loc, country, number, code   
    all_locations = mod_loc.split(";")
    how_many = len(all_locations)
    for each_location in all_locations:
        location = "{0}, {1}".format(each_location,country)
        ran = getGeocodedLatLong(location)
        coord = ran[0]
    out_line = "{0},{1},{2},{3},{4},{5},{6},{7}".format(each_location,mod_loc,country,number,code,how_many,coord[0],coord[1])
    print out_line
    writer.write(out_line+"\n")
    

    
print counter