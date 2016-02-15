# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from matplotlib.dates import DayLocator

def plot(date, day=True):
    temps = []
    dates = []
    plt.clf()
    with open('temperatures.log') as f:
        for l in f:
            log_date, temp = l[:-1].split(',')
            log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M')
            if date.date() == log_date.date() or not day:
                dates.append(log_date)
                temps.append(float(temp))

    plt.ylabel('Temp. C')
    plt.plot(dates, temps)

    if day:
        img_file = date.strftime('%Y-%m-%d.png')
        plt.title('Temp. {}'.format(date.strftime('%d/%m/%Y')))
        plt.xticks(dates, [d.strftime('%H:%M') for d in dates], rotation='vertical')
    else:
        img_file = date.strftime('%Y-%m.png')
        plt.title('Temp. {}'.format(date.strftime('%B %Y')))
        loc = DayLocator()
        plt.gcf().autofmt_xdate()

    #plt.show()
    plt.savefig(img_file)

    return img_file
