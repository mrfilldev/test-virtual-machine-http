from flask import render_template


def get_statistics(g_user_flask):
    role = g_user_flask.db['role']

    context = {
        'role': role,
        'text': 'statistics'
    }
    return render_template(
        'statistics/show_statistics.html',
        context=context
    )
