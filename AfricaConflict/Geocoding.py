'''
Created on Dec 8, 2014

@author: msisk1
geocoder working for a particular format
using the gadm boundary files on admin 2 to map to particular gridcells

'''

import os, geopy, csv
from geopy import geocoders


coder = "GeoNames"

def getGeocodedLatLong(address):
    global coder
    if coder == "Google":
        geolocator2 = geocoders.GoogleV3()
    elif coder == "OSM":
        geolocator2 = geocoders.Nominatim(timeout = 5)
    elif coder == "GeoNames":
        geolocator2 = geocoders.GeoNames(country_bias=None, username="mlsisk", timeout=2, proxies=None)
    try:
        location = geolocator2.geocode(address)
        type_loc =  location.raw["fclName"]
        return [ location.latitude ,location.longitude],type_loc, True
    except geopy.exc.GeocoderServiceError as error_message:
        print error_message,
        return [0,0],"", False
    except:
        return [0,0],"", False
        

def stripCommas(in_string):
    out_string = in_string.replace(",",";")
    return out_string




location = "E:\\GISWork_2\\Conflict\\Protest\\"
protest_locations = location + "location_List_Mod.csv"
output_file = location + "Protect_Locations_Geocoded_{0}.csv".format(coder)
lat_name = "lat"
lon_name = "lon"
type_name = "type"



def running_section():
    ordered_field_names = []
    counter = 0
    print os.path.exists(protest_locations)
    reader = open(protest_locations,'r')
    header = reader.readline()
    writer = open(output_file,"w")
    print header
    csv_file = csv.DictReader(open(protest_locations, 'rb'), delimiter=',', quotechar='"')
    for each in csv_file.fieldnames:
        ordered_field_names.append(each) 
    ordered_field_names.append(lat_name)
    ordered_field_names.append(lon_name)
    ordered_field_names.append(type_name)
    out_header = ""
    first_field = True
    for each_field in ordered_field_names:
        if first_field:
            out_header = each_field
            first_field = False
        else:
            out_header = "{0}\t{1}".format(out_header,each_field)
    writer.write(out_header+"\n")
    print out_header
    for each_line in csv_file:
        counter +=1
        location = "{0}, {1}".format(each_line['location'],each_line['country'])
        ran = getGeocodedLatLong(location)
        if ran[1] == "":
            ran = getGeocodedLatLong(each_line['location'])
        coord = ran[0]
        place_type = stripCommas(ran [1])
        out_line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(each_line['ad'],each_line['location'],each_line['Freq'],each_line['country'],each_line['mult'],coord[0],coord[1],place_type)
        print out_line
        writer.write(out_line+"\n")
        #ad    location    Freq    country    mult    lat    lon    type
        #=======================================================================
        # line_split = each_line.split(",")
        # ad = line_split[0]
        # location = line_split[1]
        # number = line_split[2]
        # country = line_split[3]   
        # all_locations = mod_loc.split(";")
        # how_many = len(all_locations)
        # for each_location in all_locations:
        #     location = "{0}, {1}".format(each_location,country)
        #     ran = getGeocodedLatLong(location)
        #     coord = ran[0]
        #     place_type = stripCommas(ran [1])
        # out_line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(each_location,mod_loc,country,number,code,how_many,coord[0],coord[1],place_type)
        # print out_line
        # writer.write(out_line+"\n")
        #=======================================================================
    writer.close()

    
running_section()