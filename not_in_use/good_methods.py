
def login():
    try:
        username = request.form['username']
        password = request.form['pass'].encode('utf-8')
        user = users.find_one({'name': username})

        if user is None:
            return redirect(url_for('index'))  # , #ecode='101')
            # Получаем данные из формы
        # print('user', user)
        # print('pass', user['password'])

        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('orders_list'))
        # return redirect(url_for('index'), ecode='102')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'



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
