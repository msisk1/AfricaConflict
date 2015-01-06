'''
Created on Jan 6, 2015
This is a reworking of the conflict code to treat include the following data:
-New PRIO results (in PRIO_Added_12-2014 folder)
-coded conflict types


@author: msisk1
'''
import arcpy
import os, timeit, numpy, math
from collections import Counter

def getListOfFiles(folder, extension):
    included_extenstions = [extension ] ;
    file_list = [os.path.splitext(fn)[0] for fn in os.listdir(folder) if any([fn.endswith(ext) for ext in included_extenstions])];
    return file_list

