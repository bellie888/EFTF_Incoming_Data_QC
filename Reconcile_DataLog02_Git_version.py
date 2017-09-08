# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
"""
Created on 4th April 2017

@author: Joseph Bell 

This script is for managing EFTF folders in Groundwater Branch.
GW have incoming data folder structure and metatdata system that can be accessed by all members as 
they find and store datasets from a variety of sources.

The folder structure is to remain the same for all 4 EFTF regions (+ Common) so that all users become familiar 
with the system and are quickly able to locate files they are looking for.
This script is only for the 'Original' Folder. We are building a similar scripts for the 'processed' folder

Users must also register their data in the 'IncomingDataLog' and fill in essential data on one row of the 
spreadsheet for each Dataset.

QC involves:
    1) ensure that none of the links in the 'IncomingDataLog' are broken.
    2) ensure that the folder contain a 'dataset' is registered directly under one of the 'fingers' of the folder structure
        a) report to console the datasets that are not registered directly under a structure finger
    3) search the folders and find data sets that are not registered:
        a) list the dataset and the name of the data owner - who is the person that imported the data in
        b) produce reports listing the deficiencies so the owners can be informed
    4) Optional:
        a) time the script took to run
        b) list of files that have spaces in their path (for ESRI files)
        c) list of users in that EFTF folder
        d) path lengths that are over 249 characters long - to avoid path length problems
    

The script referes to the 'standard folder stucture' on the water drive each time it is run. If the standard changes the
script pics this up.

The script looks up the 'u' number of the file owner from the file system, and then checks a built-in dictionary for their name.

###########

Note: for Git purposes, this script has had all the built-in long paths, peoples names, and 'u' numbers removed for security reasons. 
The original version is still available for use in GA

############

These scripts have been very well recieved by the data owners reponsible for location and metatdata of theur data. They end up with a 
short list of the datasets they need to give attention to, and are able to quickly get their data into order. 
The best way to ensure data complience is to provide tools to make it as easy as possible.

"""

#import logging
import win32api
import win32con
import win32security

import xlrd
import xlwt



from datetime import datetime
now = datetime.now()
now = now.strftime("%B %d, %Y")

import os, time
startTime = time.time()
userList = []
tailList = []

myFiles = list()
myUsers = list()
myFolders = list()


# LIST OF common folders
startFolder = r"your path to Original Folder"

# core folder structure - to ensure files are not registered directly under the core sturuture
# a list to hold the standard folder structure
skeleton = list()


standardFolders = r"Your link to the template folder structure"


stdFolder = list()


def removeEnd (thisPath):
    # remove the last part of a path name
    
    pth = os.path.dirname(thisPath)    
    return pth
    
# set up the local standard folder
localStandardFolder = removeEnd(startFolder)
localStandardFolder = removeEnd(localStandardFolder)




# refresh the list of standard folders from the groundwater folder structure
for folder, subs, files in os.walk(standardFolders):
    
     # replace the template location with this startfolder location
     # so that we have a standard template for the EFTF region we are checking
    thisFolder = folder
    
    thisFolder = thisFolder.replace(r'Your standard folder structure', localStandardFolder)

    
   
    # building a list of the standard Folders
    # the 
    stdFolder.append(thisFolder)

for item in stdFolder:
    if type(item) is None:
        print "Founf None"

''' Find the final fingers on the data structure.  '''
fingers = list()
#compare = list()
excludes = list()

## make a list to compare with - a copy of stdFolder
#for item in stdFolder:
#    compare.append(item)
# stdFolder = 
stdFolder.sort() 

for item in stdFolder:
    thisParent = removeEnd(item)
    
    if thisParent not in excludes:
        excludes.append(thisParent)
   

print 'excludes = hands and arms ..............................................'
for item in excludes:
    print item


print
print "fingers "


for item in stdFolder:
    if item not in excludes:
        fingers.append(item)
        print item
print 
#print "fingers"        
#for item in stdFolderFingers:
#    print item
#        




def findUser (pth):

    # print "Creater = ", win32api.GetUserNameEx (win32con.NameSamCompatible)
    thisUserIs = win32api.GetUserNameEx (win32con.NameSamCompatible)
    thisUserIs = thisUserIs.replace("PROD\\", "" )
    #print "User ID = " + thisUserIs

    try:
        sd = win32security.GetFileSecurity (pth, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
    
        name, domain, type = win32security.LookupAccountSid (None, owner_sid)
    except:
        name = "error getting name " + pth
    
    return name


def getOwner(uNumber):
    #build your dictionary of users here
    uNumbers = {'u882717': 'Fred Blogs',
            
            }
            
    if uNumber in uNumbers:
        return uNumbers[uNumber]
    else:
        return uNumber
            
                


count = 0
skipped = 0
# these are the file extensions or file names that should be ingnored
#print 'LIST OF IGNORED FILE TYPES'
exclusions = ['.shx', '.sbx', '.shn', 'run.info', 'a000', 'sbn', 'cpg', 'IncomingDataLog.xlsx',
              'CopyDataThemeFoldersAsNeeded', 'dbf', 'sr.lock', '.xml', '.prj', '.log', 
              'About DLRM Spatial Data', 'About DLRM spatial data', '.lnk', '.ovr', 'arc000',
              'timestamps', 'Unregistered Datasets.xls', 'Data_request_log.xlsx', '.gdb\gdb',
              '~$IncomingDataLog.xlsx']

spacesInc = ['.shp', 'lyr', '.gdb', '.grd', '.asc']

print "Running . . . "
print

print
print
print
# check if the start folder exists
if not os.path.exists(startFolder):
    print startFolder + ' does not exist'
    quit()


#    
#    
#thisUsr = findUser(r"C:\\")
#print "This User = " + thisUsr
#print "LIST OF PATHS WITH SPACES IN THEM . . . "
noFilesWithSpaces = True
noFilesWithSkeltonAsParent = True

orphanFiles = list()
longPaths = list()

# build a big list of the files in the folder = myFiles
# at the same time look for spaces in paths
#at the same time look for files with skeleton folder as parent folder
count = 0
for folder, subs, files in os.walk(startFolder):
    
    for f in files:

        count += 1

        # build the path
        thisPath = str(folder) + "\\" + str(f)
        #print "This File " + thisPath
        
        # collect the long path names
        if len(thisPath) > 249:
            a = removeEnd(thisPath)
            if a not in longPaths:
                longPaths.append(a)
            
        
        #thisUsr = findUser(thisPath)
        myFiles.append(thisPath)
  
        # LIST OF FILES WITH SPACES
        #check for spaces in file name
#        if " " in thisPath:
#            if any(ext in f for ext in spacesInc):
#                if any(ext in thisPath for ext in exclusions):
#                    pass
#                else:
#                    userNo = findUser(thisPath)
#                    print thisPath + "       " + getOwner(userNo)
#                    noFilesWithSpaces = False
                    

            
print                   
#if noFilesWithSpaces:
#    print "    . . . . no files ESRI files found with spaces in file or path"



print
print
# a count of all the files
print "Total Counted Files= " + str(count)
        


myFiles.sort

# print "number of myFiles = " + str(len(myFiles))



loggedFolders = list()
dataNames = list()





"""
Open and read the Incoming Data Excel file
"""
book = xlrd.open_workbook(startFolder + '\IncomingDataLog.xlsx')
# print number of sheets

sheet = book.sheet_by_index(0)

# read header row
header = sheet.row_values(0)

# find the excel column with 'Saved folder name' in it
k = -1
for item in header:
    k += 1
    if "Saved" in item:
        savedCol2 = k
        #print "saved column is " + str(k)
print

n = sheet.nrows
print " Incoming data Log number of rows = " + str(sheet.nrows)

for i in range(1,sheet.nrows):
    thisRow = sheet.row_values(i)
    loggedFolders.append(thisRow[savedCol2])
    dataNames.append(thisRow[0])
    # print "READ LOG  " + thisRow[savedCol2] 

print
#print 'Data Log Data Names column +++++++++++++++++++++++++++++++++++++++++++' 
#for item in dataNames:
#    print str(item)
print



print
print
print "CHECK FOR BAD LINKS IN INCOMING DATA LOG"
print "Checks for broken links and folders nor registered under a finger/leaf"
print
noBrokenLinks = True
for link in loggedFolders:
    #print
    
#    item3 = item2.replace('\\prod.lan\active\proj\futurex\StuartCorridor\Data', 'C\:')
#    print 'item 3  ' + item3
    if 'Compilations' not in link:
    #print item2
        if not os.path.exists(link):
           print 
           noBrokenLinks = False
           print link + ' - is pointing to a folder that dosnt exist'
           
        if removeEnd(link) in excludes:
            print link + ' - is registered into the folder structure and not a finger - it is too high' 
        if removeEnd(link) not in fingers:
            print link + ' - this folder is not registered under a structure finger - it is deeper' 
if noBrokenLinks:
    print ' . . . no broken links in incoming data log'

print
print
print  




print

print "Now comparing data log to all the files . . . ."


print


print 'LIST OF FILES NOT IN THE INCOMING DATA LOG ++++++++++++++++++++++++++++++++++++++++++'
print ' NB . . . groups of files can be registered as their logical parent folder'

full = 0
second = 0
third = 0
forth = 0
fifth = 0
sixth = 0
seventh = 0
eighth = 0
ninth = 0
tenth = 0
unfnd = 0
filtered = 0
notFndList = list()
for item in myFiles:
    if item in loggedFolders:
        # found it in log
        full += 1
    else:
        #shorten the path and see if parent folder is in log
        tryShort01 = removeEnd(item)
        if tryShort01 in loggedFolders:
            second += 1
        else:
            #shorten the path and see if parent folder is in log
            tryShort02 = removeEnd(tryShort01)
            if tryShort02 in loggedFolders:
                third += 1
            else:
                tryShort03 = removeEnd(tryShort02)
                if tryShort03 in loggedFolders:
                    forth += 1
                else:
                    tryShort04 = removeEnd(tryShort03)
                    if tryShort04 in loggedFolders:
                         fifth += 1
                    else:
                        tryShort05 = removeEnd(tryShort04)
                        if tryShort05 in loggedFolders:
                             sixth += 1
                        else:
                            tryShort06 = removeEnd(tryShort05)
                            if tryShort06 in loggedFolders:
                                 seventh += 1
                            else: 
                                tryShort07 = removeEnd(tryShort06)
                                if tryShort07 in loggedFolders:
                                     eighth += 1
                                else:
                                    tryShort08 = removeEnd(tryShort07)
                                    if tryShort08 in loggedFolders:
                                        ninth += 1
                                    else:
                                        tryShort09 = removeEnd(tryShort08)
                                        if tryShort09 in loggedFolders:
                                            tenth += 1                                    
                                        else:
                                            unfnd += 1
                                            if any(ext in item for ext in exclusions):
                                                filtered += 1
                                                pass
                                            else:
                                                if removeEnd(item) not in notFndList:
                                                    
                                                    
                                                    #print item
                                                    #userNo = findUser(item)
                                                    #print getOwner(userNo)  
                                                    #print tryShort04
                                                    # making a list of unregistered data
                                                    notFndList.append(removeEnd(item))
                    
print
print


 #for item in notFndList:
#    userNo = findUser(item)
#    print item + "  =  " + getOwner(userNo)
print 'stats on how far up the partent tree until found'    
print            
print "total number of files myFiles= " + str(len(myFiles))
print "full = " + str(full)
print "second = " + str(second)
print "third = " + str(third)
print "forth = " + str(forth)
print "fifth = " + str(fifth)
print "sixth = " + str(sixth)
print "seventh = " + str(seventh)
print "eight = " + str(eighth)
print "ninth = " + str(ninth)
print "tenth = " + str(tenth)
print "unfound = " + str(unfnd)
print "Filtered out files= " + str(filtered)
print "Total added = " + str (full + second + third + forth + + fifth + sixth + seventh + eighth + ninth + tenth + unfnd)
print
print

print "dataset Folders or files to yet be registered = " + str(unfnd - filtered) 
print "  here they are . . . "

# sort the list of unfound
notFndList.sort()


# print unfound to console and to excel Unregistered Datasets.xls
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("unregistered")

i = 2
sheet1.write(1, 0, "Owner")
sheet1.write(1, 1, "Folder Path - files inside this path are not registered")
sheet1.write(0,0, "Script last run on " + now)
sheet1.col(0).width = 6000
for item in notFndList:
    if item not in fingers and item not in excludes:
        userNo = findUser(item)
        # console print  
        print item + "       " + getOwner(userNo)
        # excel print
        i += 1
        sheet1.write(i, 0, getOwner(userNo))
        sheet1.write(i, 1, item)
    
    
# try to remove the old excel file    
try:
    os.remove(startFolder + "\\" + "Unregistered Datasets.xls")
except:
    pass


    
book.save(startFolder + "\\" + "Unregistered Datasets.xls")    


print    
#print "filtered unfound list length = " + str(len(notFndList))
    

'''print out longs paths and owners '''
print 'Paths over 249 long '
for path in longPaths:
    uNumber = findUser(removeEnd(path))
    user = getOwner(uNumber)
    print path + '      ' + user


# optional
## get a list of all the users for this folder
#count = 0
#for folder, subs, files in os.walk(startFolder):
#    
#    for f in files:
#        count += 1
#        # define the full path
#        thisPath = str(folder) + "\\" + str(f)
#        
#        # look up the user
#        thisUsr = findUser(thisPath)
#        
#        # if a new user add to the list of users
#        if thisUsr not in myUsers:
#            myUsers.append(thisUsr)
#
#        # get the user number
#        try:
#            thisUsr = findUser(thisPath)
#            if thisUsr not in myUsers:
#                myUsers.append(thisUsr)
#        except:
#
#            print "skipped " + thisPath
#
#            skipped += 1
#print            
#print "Total Counted Files= " + str(count)
#print
#
#print "ANALYSIS OF USERS IN THIS FOLDER . . ."
#print "Number of Users  = " + str(len(myUsers))
##print "Skipped = " + str(skipped)
#
#
#
#
#myUsers.sort 
#print
#print "List of all Users in this folder . . ."          
#
#for item in myUsers:
#    nameThem = getOwner(item)
#    print str(item) + ' - ' + nameThem
#
#
#print



    

# see how long the script took
stopTime = time.time()
sec = stopTime - startTime
days = int(sec / 86400)
sec -= 86400*days
hrs = int(sec / 3600)
sec -= 3600*hrs
mins = int(sec / 60)
sec -= 60*mins
print 'The script took ', days, 'days, ', hrs, 'hours, ', mins, 'minutes ', '%.2f ' %sec, 'seconds'
