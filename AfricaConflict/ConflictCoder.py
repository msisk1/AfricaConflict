'''
Created on Jan 6, 2015
This is a reworking of the conflict code to treat include the following data:
-New PRIO sensitivity and vulnerbility (in PRIO_Added_12-2014 folder)
-Pulling in gridded PRIO Population and infant mortality Data
-coded conflict types
-Most everything has been switched over to R

@author: msisk1
'''
import arcpy
import os, timeit #, numpy, math
#from collections import Counter


#Input variables
working_directory = "E:\\GISWork_2\\Conflict\\PDSI_July2014\\"
data_directory = working_directory + "DataLayers\\"



#Input data layers
grid_filename = "Grid_Cells_2d30s.shp"
grid_file       = working_directory + grid_filename
grid_layer = "grid_layer"
eachGrid_lyr = "eachGrid_lyr"


conflict_filename = "ConflictData.shp"
conflict_file   = data_directory + conflict_filename
conflict_layer = "conflict_layer"
each_conflict_lyr = "each_conflict_lyr"


## Output Files
output_directory = working_directory + "Outputs_01-2015\\"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print "Output directory created"

out_all_gwno_file_name = "2d30s_Monthly_conflictClasses.csv"
output_file = output_directory + out_all_gwno_file_name
out_all_gwno_header = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format("gymID","gridID","year","month","cnfts_t","cnfts_1","cnfts_2","cnfts_3","CC_conf")

## Field and Other Variables
index_field = "Id"
all_gwno_field = "all_GWNO"
year_month_field = "year_month"
conflict_type_field = "type_of_vi"


START_YEAR = 1980
END_YEAR = 2014 
max_loop = -1


## HELPER FUNCTIONS

def getListOfFiles(folder, extension):
    included_extenstions = [extension ] ;
    file_list = [os.path.splitext(fn)[0] for fn in os.listdir(folder) if any([fn.endswith(ext) for ext in included_extenstions])];
    return file_list

def deleteIfItExists(something, ARC):
    if ARC :
        if arcpy.Exists(something):
            arcpy.Delete_management(something)
    else :
        if os.path.exists(something):
            os.remove(something)

def buildYearMonthList():
    """
    Simply builds a list of year month combos for a given range set in the global constants
    Returns them as a list of strings
    """
    year_months_list = []
    for i in range(START_YEAR,END_YEAR):
        for j in range(1,13):
            ym = int("{0}{1:02d}".format(i,j))
            year_months_list.append(str(ym))
    return year_months_list


## REAL FUNCTIONS
def buildConflictFile():
    """
    As it currently is, this just builds a CSV for the conflict files using the three different types, everything 
    else is done in stata or R
    
    """
    log_writer = open(output_file, 'w')
    log_writer.write(out_all_gwno_header + "\n")
    counter = 0
    arcpy.MakeFeatureLayer_management(grid_file, grid_layer)
    arcpy.MakeFeatureLayer_management(conflict_file, conflict_layer)
    all_grids = arcpy.SearchCursor(grid_layer)
    all_year_months = buildYearMonthList()
    print "Total Number of Cells = {0}".format(str(arcpy.GetCount_management(grid_layer)))
    for each_grid in all_grids :
        eachID = each_grid.getValue(index_field)
        all_gwno = each_grid.getValue(all_gwno_field)
        if len(all_gwno) > 1:
            counter += 1
            
            if counter == max_loop :
                break
            print  "   ID {0} overlaps countries, begin processing...".format(eachID),
            print eachID, all_gwno,
            selc = "\"%s\" = %s " %(index_field, eachID) #Creates the selection string
            deleteIfItExists(eachGrid_lyr, True)
            arcpy.MakeFeatureLayer_management(grid_layer, eachGrid_lyr, selc) #Creates a new selection from the  selection criteria
            arcpy.SelectLayerByLocation_management(conflict_layer, "WITHIN", eachGrid_lyr, "", "NEW_SELECTION")
            total_conflicts_in_cell =  (int(arcpy.GetCount_management(conflict_layer).getOutput(0)))
            print total_conflicts_in_cell
            if total_conflicts_in_cell > 0 :
                for each_year_month in all_year_months:
                    year_month_selc = "\"{0}\" = \'{1}\'".format(year_month_field, each_year_month)
                    deleteIfItExists( each_conflict_lyr,True)
                    arcpy.MakeFeatureLayer_management(conflict_layer, each_conflict_lyr, year_month_selc) #Creates a new selection from the  selection criteria
                    total_conflicts_year_month = int(arcpy.GetCount_management(each_conflict_lyr).getOutput(0)) 
                    gwno_all = []
                    gwno_all_string = ""
                    if total_conflicts_year_month > 0:
                        all_confict_types = [0,0,0]
                        each_conflict_cursor = arcpy.SearchCursor(each_conflict_lyr)
                        for each_conflict in each_conflict_cursor :
                            each_gwno = each_conflict.getValue("gwno")
                            gwno_all.append(each_gwno)
                            conflict_type = each_conflict.getValue(conflict_type_field)
                            if conflict_type == 1 :
                                all_confict_types[0] +=1
                            elif conflict_type == 2 :
                                all_confict_types[1] +=1
                                
                            elif conflict_type == 3 :
                                all_confict_types[2] +=1
                        lst02 =  list(set(gwno_all))            #creates a version without duplicates
                        lst02.sort()
                        for x in lst02 :                        #creates a string without commas
                            gwno_all_string += str(x) +" "
                        #print "   {0} - {1} = {2}".format(each_year_month, total_conflicts_year_month,all_confict_types)
                        gymID = "{0}-{1}".format(eachID,each_year_month)
                        year = (each_year_month)[0:4]
                        month = (each_year_month)[-2:]
                        out_line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(gymID,eachID,year,month,total_conflicts_year_month,all_confict_types[0],all_confict_types[1],all_confict_types[2],gwno_all_string)
                        #print out_line
                        log_writer.write(out_line + "\n")
    log_writer.close()



## Main program

start = timeit.default_timer() #This is just to time how long the program run.  Can be safely Omitted

#buildConflictFile()

q = buildYearMonthList()
for a in q:
    print a

#Last bit just to create an time output
stop = timeit.default_timer()
seconds = stop - start
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print
print "Total Runtime = %d:%02d:%02d" % (h, m, s)
