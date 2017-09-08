# EFTF_Incoming_Data_QC
Script that manages the incoming data folder for compliance to metadata standards and structure
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
