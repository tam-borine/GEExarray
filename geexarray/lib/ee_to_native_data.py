# Import Dependencies
import ee, datetime
import pandas as pd

# Initialize
ee.Initialize()

# Set start and end date
startTime = datetime.datetime(2013, 2, 3)
endTime = datetime.datetime(2018, 4, 15)

# Create image collection
l8 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate(startTime, endTime)
precipitation = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD').filterDate(startTime, endTime)
probav = ee.ImageCollection('VITO/PROBAV/C1/S1_TOC_100M').filterDate(startTime, endTime)

# point = {'type':'Point', 'coordinates':[-99.545934,20.572173]};
