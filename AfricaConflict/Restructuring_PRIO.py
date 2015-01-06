'''
Created on Jan 6, 2015

@author: msisk1
'''

import csv, string




def reorderCSV(in_file, name):
    csv_file = csv.DictReader(open(in_file, 'rb'), delimiter=',', quotechar='"')
    out_file = wd + name + "_processed.csv"
    out_writer = open(out_file, "w")
    date_names = []
    name_names = []
    for each in csv_file.fieldnames:
        if each.isdigit() == True:
            date_names.append(each)
        else:
            name_names.append(each)
    #print date_names
    out_header = "{0},{1},{2},{3}".format(name_names[0],name_names[1],"Year",name)
    out_writer.write(out_header+"\n")
    for line in csv_file:
        code = line[name_names[0]]
        name = line[name_names[1]]
        if "," in name:  #removes extra commas from the strings
            print name, 
            name = string.replace(name, ',',';')
            print name
        for each_year in date_names:
            each_value = line[each_year]
            new_line = "{0},{1},{2},{3}".format(code,name,each_year,each_value)
            out_writer.write(new_line+"\n")
    out_writer.close()
#        print line["Name"]
        



wd = "E:\\GISWork_2\\Conflict\\PRIO_Added_12-2014\\"
capacity_in = wd + "2014 capacity scores.csv"
sensitivity_in = wd +  "2014 sensitivity scores.csv"





reorderCSV(capacity_in, "capacity")
reorderCSV(sensitivity_in, "sensitivity")








