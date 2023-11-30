
from app.routes import posts_blueprint
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

flask_app = Flask(__name__)
flask_app.register_blueprint(posts_blueprint,url_prefix='/post')

if __name__ == '__main__':
    flask_app.run(debug=True,port = os.environ.get('POST_APP_PORT'))