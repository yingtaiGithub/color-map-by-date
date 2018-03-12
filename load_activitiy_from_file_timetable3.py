# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:11:36 2018

@author: HUB
"""
import os
import datetime
from datetime import timedelta
from collections import Counter

import numpy as np
import pandas as pd

def get_count(row, dict_data):
    time_segment_year = str(row[1])
    time_segment_month = str(row[2]).zfill(2)
    time_segment_day = str(row[3]).zfill(2)
    time_segment_hour = str(row[4]).zfill(2)
    time_segment_minute = str(row[5]).zfill(2)
    time_segment = time_segment_year + " "+ time_segment_month + " " + time_segment_day + " " + time_segment_hour + " " + time_segment_minute
    count = dict_data[time_segment]

    return count


def main():
    MAP_YEAR = 2017
    date_first_sample = datetime.datetime(year = MAP_YEAR, day = 01, month = 01, hour = 0, minute = 0)
    nb_10_minutes = 6*24*365
    first_call = 0
    first_run = 1
    last_call = nb_10_minutes
    #np.empty([2, 2], dtype=int)
    time_segments_array = np.zeros((nb_10_minutes,10), dtype = np.int16 )

    #time_segments_array = np.chararray((nb_minutes,10))

    # Explore current directory and generate a wave file list
    wave_file_list = []
    file_list = os.listdir(os.curdir)
    nb_files = len(file_list)


    for i in range(nb_files):
        file_name = file_list[i]
        file_ext = file_name[-4:]
        if file_ext =='.wav':
            wave_file_list.append(file_name)
            print(file_ext)
    nb_wave_files = len(wave_file_list)

    # Generate a one year array with a row for each 10 minutes
    for j in range(nb_10_minutes):
        time_segment = date_first_sample + timedelta(minutes = j*10)
        time_segments_array[j,1] = time_segment.strftime("%Y")
        time_segments_array[j,2] = time_segment.strftime("%m")
        time_segments_array[j,3] = time_segment.strftime("%d")
        time_segments_array[j,4] = time_segment.strftime("%H")
        time_segments_array[j,5] = time_segment.strftime("%M")

    df = pd.DataFrame(time_segments_array)

    # Load number of bat contacts for each time segment
    # Read and format time stamp of each record
    tested_time_string_list = []
    for l in range(nb_wave_files):
        tested_raw_time_string = wave_file_list[l]
        tested_year = tested_raw_time_string[7:11]
        tested_month = tested_raw_time_string[12:14]
        tested_day = tested_raw_time_string[15:17]
        tested_hour = tested_raw_time_string[18:20]
        tested_rounded_minutes = tested_raw_time_string[21:22]+"0"
        tested_time_string = tested_year + " "+ tested_month + " " + tested_day + " " + tested_hour + " " + tested_rounded_minutes
        print (tested_time_string)
        tested_time_string_list.append(tested_time_string)

    tested_time_string_dict = Counter(tested_time_string_list)
    df['count'] = df.apply(lambda row: get_count(row, tested_time_string_dict), axis=1)

    time_segment = pd.date_range(date_first_sample + datetime.timedelta(), periods=nb_10_minutes, freq='10min')
    output_array = pd.DataFrame(time_segment)
    output_array['newcol'] = df['count']

    # save to xlsx file
    filepath = 'Bat_time.xlsx'

    output_array.to_excel(filepath, index=False)


# 0:03:41.971000

if __name__ == "__main__":
    time1 = datetime.datetime.now()
    main()
    time2 = datetime.datetime.now()
    print (time2-time1)