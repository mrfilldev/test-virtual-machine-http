from datetime import datetime, timedelta, date

from flask import render_template, jsonify

from new_project.db.models import TestScheduleOrder


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def view_schedule(g_user_flask):
    # Pass schedule data to template
    events = [
            {
                'title': 'Event 1',
                'start': '2023-05-02T16:00:00',
                'end': '2023-05-02T17:30:00',
                'resourceId': 'a'
            },
            {
                'title': 'Event 2',
                'start': '2023-05-02T17:30:00',
                'end': '2023-05-02T17:45:00',
                'resourceId': 'b'
            },
            {
                'title': 'Event 3',
                'start': '2023-05-02T18:15:00',
                'end': '2023-05-02T19:00:00',
                'resourceId': 'c'
            }
        ]
    context = {
        'events': events
    }
    return render_template('schedule/view_schedule.html', context=context)


def create_carwash(request):
    print('\n################################################################\n')
    dict_of_form = request.form.to_dict(flat=False)
    print(dict_of_form)
    print('################################################################\n')

    for k, v in dict_of_form.items():
        print(k, '-> ', v)

    print('\n################################################################\n')

    data = request.form.to_dict()
    print(data)
    # обработка данных и формирование ответа
    response = {'status': 'success'}
    return jsonify(response)
