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
    return render_template('schedule/view_schedule.html')


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
