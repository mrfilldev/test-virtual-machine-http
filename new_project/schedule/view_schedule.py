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
            'resourceId': '4'
        },
        {
            'title': 'Event 2',
            'start': '2023-05-03T17:30:00',
            'end': '2023-05-03T17:45:00',
            'resourceId': '6'
        },
        {
            'title': 'Event 3',
            'start': '2023-05-03T18:15:00',
            'end': '2023-05-03T19:00:00',
            'resourceId': '7'
        }
    ]
    resources = [
        {'id': 1, 'title': 'Бокс 1'},
        {'id': 2, 'title': 'Бокс 2'},
        {'id': 3, 'title': 'Бокс 3'},
        {'id': 4, 'title': 'Бокс 4'},
        {'id': 5, 'title': 'Бокс 5'},
        {'id': 6, 'title': 'Бокс 6'},
        {'id': 7, 'title': 'Бокс 7'},
        {'id': 8, 'title': 'Бокс 8'},
        {'id': 9, 'title': 'Бокс 9'},
        {'id': 10, 'title': 'Бокс 10'},
        {'id': 11, 'title': 'Бокс 11'},
        {'id': 12, 'title': 'Бокс 12'},
    ]
    carwash_start_time = '08:00:00'
    carwash_end_time = '23:00:00'
    date_today = '2023-05-03'
    now_iso = datetime.now().isoformat()

    context = {
        'orders': events,
        'boxes': resources,
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
