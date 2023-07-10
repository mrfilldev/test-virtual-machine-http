from flask import render_template

from flask import Flask, Markup, render_template

app = Flask(__name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


def line_chart():
    line_labels = labels
    line_values = values
    return render_template('statistics/show_statistics.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels,
                           values=line_values)


def get_statistics(g_user_flask):
    # role = g_user_flask.user_db['role']
    #
    # context = {
    #     'role': role,
    #     'text': 'statistics'
    # }
    # return render_template(
    #     'statistics/show_statistics.html',
    #     context=context
    # )
    return line_chart()
