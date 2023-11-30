
from app.routes import users_blueprint
from flask import Flask
import os

flask_app = Flask(__name__)
flask_app.register_blueprint(users_blueprint,url_prefix='/user')

if __name__ == '__main__':
    flask_app.run(debug=True, port=os.environ.get('USER_APP_PORT'),host='0.0.0.0')