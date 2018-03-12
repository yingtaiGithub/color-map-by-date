from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


def split_date(row):
    # row['day'] = row['Date'].date()
    # row['time'] = row['Date'].time()
    row['min_in_day'] = ((row['Date'].hour *60 + row['Date'].minute)/10 + 72) % 144
    row['day_in_year'] = row['Date'].dayofyear
    row['sunset_min_in_day'] = ((row['sunset'].hour *60 + row['sunset'].minute)/10 + 72) % 144
    row['sunrise_min_in_day'] = ((row['sunrise'].hour *60 + row['sunrise'].minute)/10 + 72) % 144

    return row

def main():
    # Getting first days of every month and calculate days in year for these first days. And Making a list to be a ticker of y axis in map.
    first_days = [datetime.strptime('2017-%s-1'%item, '%Y-%m-%d') for item in range(1,13)]
    first_daysinyear = [item.timetuple().tm_yday for item in first_days]
    hours_split = ["%s:00" %str(item) for item in range(12, 24)] + ["%s:00" %str(item).zfill(2) for item in range(0, 12)]

    # Read csv file and calculate days_in_year and minutes_in_day from 'Date' column for ever rows and create 2 new columns with two kinds of values for plotting map.
    df = pd.read_excel(input_file)
    df = df[['Date', 'sunrise', 'sunset', 'Pipip']]
    df = df[df.Date.notnull()]
    df = df.apply(split_date, axis=1)


    # Draw color map. It uses 'day_in_year' and 'min_in_day' columns of df for '(x, y)' location and 'Pipip' column for color.
    cmap = cm.get_cmap('Spectral') # Colour map (there are many others)
    fig, ax = plt.subplots(1)
    colors = [color_panel.get(str(x), "#ffef9a") for x in list(df['Pipip'])]
    ax.scatter(list(df['day_in_year']), list(df['min_in_day']), c=colors, s=100, cmap=cmap, edgecolor='None', marker='s')
    ax.set_xlabel('Month')
    ax.set_ylabel('Hour')

    # Draw lines for 'sunset' and 'sunrise'
    ax.plot(df['day_in_year'],df['sunset_min_in_day'], 'w--')
    ax.plot(df['day_in_year'], df['sunrise_min_in_day'], 'w--')

    # Add texts; 'sunset' and 'sunrise'
    text_position = [(250, df['sunset_min_in_day'].min()), (250, df['sunrise_min_in_day'].max())]
    ax.text(text_position[0][0], text_position[0][1], 'sunset', color='white')
    ax.text(text_position[1][0], text_position[1][1], 'sunrise', color='white')

    # Setting ticker to x and y axis.
    plt.xticks(first_daysinyear, range(1, 13))
    plt.yticks([x*6 for x in range(24)], hours_split)

    plt.show()

if __name__ == "__main__":
    color_panel = {"0": '#4473c5', "1": "#698bbb", "2":"#8ba4b8", "3": "#b5bcaa", "4": "#d9d5a6", "5": "#ffef9a"}
    input_file = "C_E7_static.xlsx"
    time1 = datetime.now()
    main()
    time2 = datetime.now()
    print ("Execution Time: ", time2-time1)