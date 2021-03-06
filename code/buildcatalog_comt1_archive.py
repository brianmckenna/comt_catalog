#!/home/testbed/python27_epd/bin/python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>
#-----------------------------------------------------------------------
# This program will auto-generate a catalog from a google doc spreadsheet
#
# Steps to Use this Script:
#-----------------------------------------------------------------------
#
# 1) Load Libraries, etc.

import os
import netCDF4
import gspread
import pyugrid
import XMLdataset
import subprocess
  
os.chdir('/home/testbed/comt_catalog/code')
#-----------------------------------------------------------------------
#
# 2) Read Generic Header and Footer File

f = open('header.xml','r')
header = f.read()
f.close() 
    
f = open('footer.xml','r')
footer = f.read()
f.close()      
    
catalog = header
  
#-----------------------------------------------------------------------
#
# 3) Connect to Google Doc

c = gspread.Client(auth=('rsignell@yahoo.com', 'sura_ftp'))
c.login()
w = c.open_by_key(key='0AmAEVaW9GoHedFZHU3Z4c1pyMkozWmJxSUlGSDk3eVE')
wks = w.worksheet('comt_1_archive')
rows = wks.get_all_records(empty2zero=False)

#-----------------------------------------------------------------------
#
# 4) Loop through rows of google doc spreadsheet
#    -> Determine if Simulation is to be Included in Catalog
#    -> If it is, then add it to Catalog
#    -> At the end of the google doc, close the catalog

wrow = 1
for row in rows:
    wrow += 1
    usethis = row['Include in Catalog?']
    if usethis == 'y':
      id = row['Unique ID']
      runSummary = row['Summary Description']
      datasetName = row['Dataset Name 2']
      group = row['Group']
      organization = row['Organization']
      model = row['Model']
      cdmdatatype = row['CDM Type']
      dir = row['Data path']
      ncmlName = row['NCML Filename']
      ncmlFile = os.path.join(dir,ncmlName)
      Meta = row['Metadata Link']
      xml = XMLdataset.XMLdataset(ncmlFile=ncmlFile, datasetName=datasetName, 
            runSummary=runSummary, urlPath=dir, datasetID=id, 
            cdm_data_type=cdmdatatype)
      catalog = catalog + xml

      print wrow
      print id
      print cdmdatatype

#-----------------------------------------------------------------------
#
# 5) Add Footer, write Catalog and Update System

catalog = (catalog + footer).encode('utf-8')

f = open('/home/testbed/comt_catalog/catalogs/comt_1_archive_summary.xml','w')
f.write(catalog)
f.close()

#-----------------------------------------------------------------------
#
# 6) Push to Github

os.chdir('/home/testbed/comt_catalog')
def git(*args):
    return subprocess.check_call(['/usr/local/bin/git'] + list(args))

git ("add", "-A", ":/")
git ("commit", "-am", "updated catalogs")
git ("push")

#os.chdir('/var/www/thredds_instance/content/thredds/testbed2_catalog')
#git ("pull")
