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
creatingDoFileFromVariableList()