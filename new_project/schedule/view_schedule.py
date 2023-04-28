from datetime import datetime, timedelta, date

from flask import render_template

from new_project.db.models import TestScheduleOrder


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def view_schedule(g_user_flask):
    # Pass schedule data to template
    return render_template('schedule/view_schedule.html')
