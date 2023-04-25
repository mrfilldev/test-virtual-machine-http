from datetime import datetime, timedelta, date

from flask import render_template


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def view_schedule(g_user_flask):
    dts = [dt.strftime('%Y-%m-%d T%H:%M Z') for dt in
           datetime_range(datetime(year=2023, month=4, day=25, hour=14), datetime(year=2023, month=4, day=25, hour=14 + 9),
                          timedelta(minutes=15))]


    context = {
        'dts': dts,
        'date': date.today()

    }
    return render_template('schedule/view_schedule.html', context=context)
