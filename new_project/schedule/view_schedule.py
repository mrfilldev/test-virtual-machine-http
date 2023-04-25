from flask import render_template


def view_schedule(g_user_flask):
    context = {

    }
    return render_template('schedule/view_schedule.html', context=context)
