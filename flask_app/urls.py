from config.config import Config

from application import create_app

app = create_app()

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.run(host='127.0.0.1', port=8080)
