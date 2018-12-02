from flask import Flask, Blueprint
from flask_cors import CORS
from flasgger import Swagger

from config.environment_tools import init_environment, get_environment_mode
from config.swagger import get_swagger_template

def create_app(env_path: str):
    app = Flask(__name__)
    CORS(app, allow_headers="*")
    init_environment(env_path=env_path)
    app.config.from_pyfile('default_config.py')
    mode = get_environment_mode()
    app.config.from_pyfile(mode.config_path)
    return app


def get_secret_key(app: Flask):
    return app.config['SECRET_KEY']


FLASK_APP = create_app(None)
SWAG = Swagger(FLASK_APP, template=get_swagger_template())