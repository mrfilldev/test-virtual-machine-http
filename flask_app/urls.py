# -*- coding: utf-8 -*-
import traceback
import boto3
from bson import json_util
from flask import Flask, render_template, url_for, request, session, redirect, Response
import carwash_list
import carwash_order
import ping_carwash_box
from config.config import Config
from flask_app.forms import LoginForm
from flask_bootstrap import Bootstrap
import json
from types import SimpleNamespace
# from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__,
            static_url_path='',
            static_folder='/static',
            # template_folder='/templates'
            )
bootstrap = Bootstrap(app)

# app.config["MONGO_URI"] = Config.url
# mongo = PyMongo(app)

# load_dotenv()

URL_DEV = Config.URL_DEV
API_KEY = Config.API_KEY  # ['123456', '7tllmnubn49ghu5qrep97']

##################################################################
queue_orders = 'https://message-queue.api.cloud.yandex.net/b1gjm9f9sf1pbis8lhhp/dj600000000bqnoc01b1/test-tanker' \
               '-carwsh-orders'
client = boto3.client(
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,  # os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,  # os.getenv('AWS_SECRET_ACCESS_KEY'),
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    region_name='ru-central1'
)
queue_url = client.create_queue(QueueName='test-tanker-carwsh-orders').get('QueueUrl')
########################################################################
users = Config.col_users
orders = Config.col_orders


@app.route('/carwash/ping')
async def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)

    if apiKey in API_KEY:
        status = ping_carwash_box.main(request)
        response = Response(status=status, mimetype="application/json")

    else:
        result = 'Error, Something is wrong...'
        status = 401

        response = Response(result, status=status, mimetype="application/json")
    print(response)
    return response


@app.route('/carwash/list')
async def return_carwash_list():
    try_apiKey = request.args.get('apikey')
    print('try_apiKey: ' + try_apiKey)
    if try_apiKey in API_KEY:
        result = carwash_list.main(request)
        status = 200
    else:
        result = 'Error, Something is wrong...'
        status = 401
    response = Response(result, status=status, mimetype="application/json")
    return response


@app.route('/carwash/order', methods=['POST'])
@app.route('/tanker/order', methods=['POST'])
async def make_carwash_order():
    try:
        carwash_order.main(request)
        return Response(status=200)
    except Exception as e:
        # write to log
        traceback.print_exc()
        print(f'caught {type(e)}: e', e)  # добавить логгер
        return Response(status=400)


# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)
#


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            existing_user = users.find_one({'name': request.form['username']})

            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                users.insert_one({'name': request.form['username'], 'password': hashpass})
                session['username'] = request.form['username']
                return redirect(url_for('index'))

            return 'That username already exists!'

        return render_template('users/register.html')
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        username = request.form['username']
        password = request.form['pass'].encode('utf-8')
        user = users.find_one({'name': username})

        if user is None:
            return redirect(url_for('index'))  # , #ecode='101')
            # Получаем данные из формы
        print('user', user)
        print('pass', user['password'])

        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('admin'))
        # return redirect(url_for('index'), ecode='102')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    try:
        if 'username' in session:
            session.pop('username', None)
        return render_template('users/logged_out.html')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/admin', methods=['POST', 'GET'])
async def admin():
    # user = {'nickname': 'no name'}  # выдуманный пользователь-заглушка

    posts = []
    for i in orders.find():
        print('order: ', i)
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        print('data: ', type(data), data, '\n')
        order = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        posts.append(order)

    return render_template(
        'admin.html',
        locker=True,
        #   user=user,
        posts=posts
    )


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.run(host='127.0.0.1', port=8080)

#
