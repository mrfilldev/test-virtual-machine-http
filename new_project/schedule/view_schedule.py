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
            'start': '2023-05-03T16:00:00',
            'end': '2023-05-03T17:30:00',
            'resourceId': 'a'
        },
        {
            'title': 'Event 2',
            'start': '2023-05-03T17:30:00',
            'end': '2023-05-03T17:45:00',
            'resourceId': 'b'
        },
        {
            'title': 'Event 3',
            'start': '2023-05-03T18:15:00',
            'end': '2023-05-03T19:00:00',
            'resourceId': 'c'
        }
    ]
    resources = [
        {'id': 'a', 'title': 'Бокс 1'},
        {'id': 'b', 'title': 'Бокс 2'},
        {'id': 'c', 'title': 'Бокс 3'},
        {'id': 'd', 'title': 'Бокс 4'},
        {'id': 'e', 'title': 'Бокс 5'},
        {'id': 'f', 'title': 'Бокс 6'},
        {'id': 'g', 'title': 'Бокс 7'},
        {'id': 'h', 'title': 'Бокс 8'},
        {'id': 'i', 'title': 'Бокс 9'},
        {'id': 'j', 'title': 'Бокс 10'},
        {'id': 'k', 'title': 'Бокс 11'},
        {'id': 'l', 'title': 'Бокс 12'},
    ]
    carwash_start_time = '08:00:00'
    carwash_end_time = '23:00:00'
    date_today = '2023-05-03'
    now_iso = datetime.now().isoformat()

    context = {
        'events_carwash': events,
        'resources': resources,
        'carwash_start_time': carwash_start_time,
        'carwash_end_time': carwash_end_time,
        'date_today': date_today,
        'now_iso': now_iso
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
