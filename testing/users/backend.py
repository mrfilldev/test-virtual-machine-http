import json
import uuid
import datetime
import smtplib
from types import SimpleNamespace

from bson import json_util
from flask import render_template, url_for, redirect, jsonify, abort, request

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash, CategoryAuto, Prices


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def get_obj(obj):
    obj = json.dumps(obj, default=default)
    obj = json.loads(obj, object_hook=lambda d: SimpleNamespace(**d))
    return obj


def send_mail(dest_email, text, subject):
    email = "moidex.work@yandex.ru"
    password = "jlgovnsgsqlcfzkz"
    dest_email = dest_email
    subject = subject
    email_text = text + "\n\nМойдекс\n"

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest_email,
                                                           subject,
                                                           email_text)

    server = smtplib.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()


def list_workers(g_user_flask):
    all_users = database.col_users.find({})
    workers_list = []
    if g_user_flask.user_db['role'] != 'admin':
        for i in all_users:
            user_obj = get_obj(i)
            if user_obj.role == 'network_worker' and user_obj.networks[0] == g_user_flask.user_db['networks'][0]:
                workers_list.append(user_obj)
            print('user_obj: ', user_obj, '\n')
    else:
        return redirect(url_for('admin_blueprint.admin_users'))
    print(workers_list)
    context = {
        'user_list': workers_list,
    }
    return render_template('users/users_list.html', context=context)


def user_detail(g_user_flask, user_id):
    user = database.col_users.find_one({'_id': str(user_id)})  # dict
    user_obj = get_obj(user)
    print('user_obj: ', user_obj, '\n')
    if request.method == 'POST':
        print('\n################################################################\n')
        dict_of_form = request.form.to_dict(flat=False)
        print(dict_of_form)
        print('################################################################\n')
        for k, v in dict_of_form.items():
            print(k, '-> ', v)
        print('\n################################################################\n')
        try:
            user = {'_id': user_id}
            print('user: ', user)

            set_fields = {'$set': {
                'PinnedCarwashId': dict_of_form['PinnedCarwashId'],
            }}
            print(set_fields)
            update = database.col_users.update_one(user, set_fields)
            print(update)
        except Exception as e:
            print("Error updating : ", e)

        context = {}
        print('context: ', context)
        return redirect(url_for('users_blueprint.users_list'))

    all_carwashes = database.col_carwashes.find({'network_id': g_user_flask.user_db['networks'][0]})
    carwashes = []
    for carwash in all_carwashes:
        carwash_obj = get_obj(carwash)
        carwashes.append(carwash_obj)
    print('carwashes: ', carwashes)

    all_networks = database.col_networks.find({})
    networks = []
    for network in all_networks:
        network_obj = get_obj(network)
        if network_obj._id in g_user_flask.user_db['networks']:
            networks.append(network_obj)

    context = {
        'user': user_obj,
        'carwashes': carwashes,
        'networks': networks,
    }
    return render_template('users/user_detail.html', context=context)


def add_carwash_worker(g_user_flask):
    print('test')
    if request.method == 'POST':
        print('\n################################################################\n')
        dict_of_form = request.form.to_dict(flat=False)
        print(dict_of_form)
        print('################################################################\n')
        try:
            send_mail()
        except Exception as e:
            print('error: ', e)
    context = {}
    return render_template('users/user_create.html', context=context)
