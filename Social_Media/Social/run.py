
from app.routes import social_blueprint
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

flask_app = Flask(__name__)
flask_app.register_blueprint(social_blueprint,url_prefix='/social')

if __name__ == '__main__':
    flask_app.run(debug=True,port = os.environ.get('SOCIAL_APP_PORT'),host='0.0.0.0')