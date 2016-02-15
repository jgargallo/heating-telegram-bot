# -*- coding: utf-8 -*-

from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go

def plot(date, day=True):
    temps = []
    dates = []
    with open('temperatures.log') as f:
        for l in f:
            log_date, temp = l[:-1].split(',')
            log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M')
            if date.date() == log_date.date() or not day:
                dates.append(log_date)
                temps.append(float(temp))

    if day:
        img_file = date.strftime('%Y-%m-%d')
        #plt.title('Temp. {}'.format(date.strftime('%d/%m/%Y')))
        #plt.xticks(dates, [d.strftime('%H:%M') for d in dates], rotation='vertical')
    else:
        img_file = date.strftime('%Y-%m')
        #plt.title('Temp. {}'.format(date.strftime('%B %Y')))

    data = [
        go.Scatter(
            x=dates,
            y=temps
        )
    ]

    return '{}.png'.format(py.plot(data, filename='temp-{}'.format(img_file)))
