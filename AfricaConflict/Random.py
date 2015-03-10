'''
Created on Jan 8, 2015

@author: msisk1
'''
import os, csv


def creatingDoFileFromVariableList():
    os.chdir("E:\\GISWork_2\\Conflict\\PRIO_Added_12-2014\\")
    csv_dic = csv.DictReader(open("Old_DataLables.txt", 'rb'), delimiter=',', quotechar='"')
    out_writer = open("NewStataCommands.do", "w")
    for line in csv_dic:
        new_line = "label variable {0} \"{1}\"".format(line["name"], line["label"].rstrip())
        print new_line
        out_writer.write(new_line + "\n")
    out_writer.close()


def sortingAndCollatingLocationFile():
    os.chdir("E:\\GISWork_2\\Conflict\\Protest\\")
    csv_dic = csv.DictReader(open("Locations_with_CCodes.csv", 'rb'), delimiter=',', quotechar='"')
    out_writer = open("just_protests_and_Dates2.csv", "w")
    out_header = "{0},{1},{2},{3},{4},{5}".format("gridcell","year","month","ccode","id","gym")
    out_writer.write(out_header + "\n")
#    for each in csv_dic.fieldnames:
#        print each
    for each_line in csv_dic:
        each_codes = each_line["GridIDs"]
        if each_codes != "NA":
            all_gridcell = each_codes.split(" ")
            for each_gridcell in all_gridcell:
                gym = "{0}-{1}{2}".format( each_gridcell, each_line["startyear"],each_line["startmonth"].zfill(2))
                new_line =  "{0},{1},{2},{3},{4},{5}".format( each_gridcell, each_line["startyear"],each_line["startmonth"],each_line["ccode"],each_line["id"],gym)
                #print new_line
                out_writer.write(new_line + "\n")
    out_writer.close()
    
    
    print "finished raw file"


#creatingDoFileFromVariableList()


sortingAndCollatingLocationFile()
