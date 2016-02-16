# -*- coding: utf-8 -*-

from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go

def plot(date, v, day=True):
    temps = []
    dates = []
    max_values = []
    min_values = []
    avg_values = []
    with open('temperatures.log') as f:
        last_date = None
        day_temp = []
        log_date = None
        for l in f:
            log_date, temp = l[:-1].split(',')
            log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M')
            if date.date() == log_date.date() or not day:
                if day:
                    dates.append(log_date)
                temps.append(float(temp))

                if log_date.date() != last_date and last_date and not day:
                    dates.append(last_date)
                    min_values.append(min(day_temp))
                    avg_values.append((float(sum(day_temp))/len(day_temp)) - min(day_temp))
                    max_values.append(max(day_temp) - (float(sum(day_temp))/len(day_temp)))
                    day_temp = []

                day_temp.append(float(temp))
                last_date = log_date.date()

    if not day and len(day_temp) > 0:
        dates.append(last_date)
        min_values.append(min(day_temp))
        avg_values.append((float(sum(day_temp))/len(day_temp)) - min(day_temp))
        max_values.append(max(day_temp) - (float(sum(day_temp))/len(day_temp)))

    if day:
        img_file = date.strftime('%Y-%m-%d')
        title = 'Temp. {}'.format(date.strftime('%d/%m/%Y'))
        data = [go.Bar( x=dates, y=temps)]
        layout = go.Layout(
            title='{} ({})'.format(title, v),
            xaxis={
                'title': "time",
                'autorange': True,
                'tickangle': -90,
                'dtick': 3600000,
                'tickformat': "%H:%M"
            },
            yaxis={
                'type': "linear",
                'autorange': False,
                'title': "Temp. C",
                'range': [10, 30],
                'fixedrange': True,
                'tickmode': "linear",
                'dtick' :1
            },
        )
    else:
        img_file = date.strftime('%Y-%m')
        title = 'Temp. {}'.format(date.strftime('%B %Y'))
        max_trace = go.Bar(
            x=dates,
            y=max_values,
            name='max'
        )
        min_trace = go.Bar(
            x=dates,
            y=min_values,
            name='min'
        )
        avg_trace = go.Bar(
            x=dates,
            y=avg_values,
            name='avg'
        )
        data = [min_trace, avg_trace, max_trace]
        layout = go.Layout(
            title='{} ({})'.format(title, v),
            barmode='stack',
            xaxis={
                'title': "time",
                'autorange': True,
                'dtick': 24 * 3600000,
                'tickformat': "%d"
            },
            yaxis={
                'type': "linear",
                'autorange': False,
                'title': "Temp. C",
                'range': [10, 30],
                'fixedrange': True,
                'tickmode': "linear",
                'dtick' :1
            },
        )

    figure = go.Figure(data=data, layout=layout)

    return '{}.png'.format(py.plot(figure, filename='temp-{}'.format(img_file)))
