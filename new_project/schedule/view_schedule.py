from datetime import datetime, timedelta, date

from flask import render_template

from new_project.db.models import TestScheduleOrder


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def view_schedule(g_user_flask):
    dts = [dt.strftime('%Y-%m-%d T%H:%M Z') for dt in
           datetime_range(datetime(year=2023, month=4, day=25, hour=14),
                          datetime(year=2023, month=4, day=25, hour=14 + 9),
                          timedelta(minutes=15))]
    list_test_orders = []
    new_order = TestScheduleOrder(
        1700, 5, 45
    )
    list_test_orders.append(new_order)
    new_order = TestScheduleOrder(
        2200, 4, 90
    )
    list_test_orders.append(new_order)
    new_order = TestScheduleOrder(
        3300, 5, 120
    )
    list_test_orders.append(new_order)

    list_test_orders = [
        'Кат.5 2350&#8381',
        '',
        'Кат.3 1200&#8381',
        '',
        'Кат.4 350&#8381',
        ''
    ]
    context = {
        'dts': dts,
        'date': date.today(),
        'list_test_orders': list_test_orders,
    }
    return render_template('schedule/view_schedule.html', context=context)
