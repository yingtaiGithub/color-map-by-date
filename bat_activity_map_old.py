# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:11:36 2018

@author: HUB
"""
# Import pandas
from __future__ import division
import cv2
import pandas as pd
import astral
import datetime
import time
import numpy as np
import math
import os


FT_PER_METRE = 3.2808399

# Construct our location.  Longitude west and latitude south are negative.
Coulonges = astral.Location(info=("Coulonges", "France", 46.472389, -0.604935, "GMT", 157/FT_PER_METRE))

# Assign spreadsheet filename to `file`
#file = 'C_E7_static.xlsx'

# Load spreadsheet
#xl = pd.ExcelFile(file)

# Load a sheet into a DataFrame by name: data_frame
#data_frame = xl.parse('Sheet1')
# Read shape of the data_frame
#data_frame_shape = data_frame.shape
# Pick the number of row from the shape
#data_number_rows = data_frame_shape[0]

# Background_height = number of 10 minutes segments in one day
BACKGROUND_HEIGHT = 24*6

# Background_width = number of days in one year
BACKGROUND_WIDTH = 365

# Year of the sampled data
MAP_YEAR = 2017

#initial_map_date = datetime.date(year = MAP_YEAR, day = 01, month = 01) 
initial_map_date = datetime.datetime(year = MAP_YEAR, day = 01, month = 01, hour = 0, minute = 0) 
# time delta = jours
TEN_MINUTES = 1/144

# Create an empty array filled with zeros 
background = np.zeros((BACKGROUND_HEIGHT, BACKGROUND_WIDTH), np.uint8)

cwd = os.getcwd()
asps = []
for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.endswith('.wav'):
            asps.append(file)
nb_files = len(asps)

# loop for each day of the year to compute the hours of sunset and sunrise 
for i in range(BACKGROUND_WIDTH):
    # Increment the day with i days
    map_date = initial_map_date + datetime.timedelta(i)
    # Compute the sunrise and sunset for the map_date
    sun_info = Coulonges.sun(date=map_date )
    # Extract the values of sunset and sunrise
    sunrise = sun_info["sunrise"]
    sunset = sun_info["sunset"]
    # Remove the GMT info in the values of sunset and sunrise (not supported by excel)
    sunset = sunset.replace(tzinfo=None)
    sunrise = sunrise.replace(tzinfo=None)
    #tested_day = sunrise.timetuple().tm_yday

    pixel_sunset_time = int((sunset.hour*60 + sunset.minute)/10)
    pixel_sunrise_time = int((sunrise.hour*60 + sunrise.minute)/10)
    
    # Write the position of sunrise and sunset for map_date in the background
    background[pixel_sunset_time,i-1] = 255
    background[pixel_sunrise_time,i-1] = 255
    
# Loop in each time element (10 minutes) to define the activity level recorded during this time
#for j in range (0,BACKGROUND_WIDTH):
 #   for k in range (0,BACKGROUND_HEIGHT):
  #      min_date = initial_map_date + datetime.timedelta(j+TEN_MINUTES*k)
   #     max_date = initial_map_date + datetime.timedelta(j + TEN_MINUTES * (k + 1))
for l in range (0,nb_files):
    tested_file_name = asps[l]
    tested_year = int(tested_file_name[0:4])
    tested_month = int(tested_file_name[5:7])
    tested_day = int(tested_file_name[8:10])
    tested_hour = int(tested_file_name[11:13])
    tested_minute = int(tested_file_name[14:16])
    tested_date = datetime.datetime(year = tested_year, month = tested_month, day = tested_day, hour = tested_hour, minute = tested_minute )
    
    x_pos = (tested_date-initial_map_date).days
    y_pos = int((tested_hour+tested_minute)/6)
    print('x_pos =',x_pos)
    print('y_pos =',y_pos)
    background[y_pos,x_pos] = background[y_pos,x_pos] + 100
            
cv2.imshow('image',background)
cv2.waitKey(0)
'''
# Create 2 new columns filled with 0
data_frame = data_frame.assign(sunset = 0)
data_frame = data_frame.assign(sunrise = 0)
data_frame = data_frame.assign(day_of_year = 0)
data_frame = data_frame.assign(wind_influence = 0)
data_frame = data_frame.assign(temp_influence = 0)
data_frame = data_frame.assign(hour_influence = 0)
data_frame = data_frame.assign(day_influence = 0)
data_frame = data_frame.assign(average_activity = 0)
data_frame = data_frame.assign(high_wind_activity = 0)
# Compute sunset and sun rise and insert it in the ne columns
for i in range(data_number_rows):
    # Set sunrise, sunset and year day
    tested_date = data_frame.iloc[i][0] 
    sun_info = Coulonges.sun(date=tested_date )
    sunrise = sun_info["sunrise"]
    sunset = sun_info["sunset"]
    sunset = sunset.replace(tzinfo=None)
    sunrise = sunrise.replace(tzinfo=None)
    tested_day = sunrise.timetuple().tm_yday
    
    # Compute wind influence
    wind_speed = data_frame.iloc[i][1]
    wind_driven_activity = 1/(1+math.exp((wind_speed - WIND_TRESHOLD)*WIND_SLOPE)) # wind speed must be under 100 m/s
    high_wind_driven_activity = 1/(1+math.exp((wind_speed - HIGH_WIND_TRESHOLD)*HIGH_WIND_SLOPE)) # wind speed must be under 100 m/s
    # Compute wind influence
    wind_temp = data_frame.iloc[i][3]
    temp_driven_activity = - 1/(1+math.exp((wind_temp - MIN_TEMP_TRESHOLD)*MIN_TEMP_SLOPE))+ 1/(1+math.exp((wind_temp - MAX_TEMP_TRESHOLD)*MAX_TEMP_SLOPE))
    
    # Compute hour influence
    # Decimal_sunset_hour
    sunset_hour = sunset.hour
    sunset_minute = math.floor(float(sunset.minute)/0.6)/100
    decimal_sunset_hour = sunset_hour+sunset_minute
     # Decimal_sunrise_hour
    sunrise_hour = sunrise.hour
    sunrise_minute = math.floor(float(sunrise.minute)/0.6)/100
    decimal_sunrise_hour = sunrise_hour+sunrise_minute
    # Decimal_tested_hour
    tested_hour = tested_date.hour
    tested_minute = math.floor(float(tested_date.minute)/0.6)/100
    decimal_tested_hour = tested_hour+tested_minute
    hour_driven_activity = 1/(1 + math.exp((decimal_tested_hour - decimal_sunrise_hour)*MIN_HOUR_SLOPE))+(1 - 1 /(1 + math.exp((decimal_tested_hour - decimal_sunset_hour)*MAX_HOUR_SLOPE)))
    
    # Compute day influence
    print(tested_day)
    day_driven_activity = ((1-1/(1 + math.exp((tested_day - MIN_DATE_TRESHOLD)*MIN_DATE_SLOPE))) + 1 /(1 + math.exp((tested_day - MAX_DATE_TRESHOLD)*MAX_DATE_SLOPE)))-1
    print(day_driven_activity)
    
    # Compute average activity
    average_activity = wind_driven_activity * temp_driven_activity * hour_driven_activity * day_driven_activity
    high_wind_activity = high_wind_driven_activity * temp_driven_activity * hour_driven_activity * day_driven_activity
    
    # Write data in the newly created columns
    data_frame.iloc[i,5] = sunset
    data_frame.iloc[i,6] = sunrise
    data_frame.iloc[i,7] = sunrise.timetuple().tm_yday
    data_frame.iloc[i,8] = wind_driven_activity
    data_frame.iloc[i,9] = temp_driven_activity
    data_frame.iloc[i,10] = hour_driven_activity
    data_frame.iloc[i,11] = day_driven_activity
    data_frame.iloc[i,12] = average_activity
    data_frame.iloc[i,13] = high_wind_activity

# Compute bat activity level

    
# Set output file name
writer = pd.ExcelWriter('weather_sunset_sunrise.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
data_frame.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
'''