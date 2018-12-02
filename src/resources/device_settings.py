from typing import List

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

API_PREFIX = 'settings'
DEVICE_SETTINGS_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(DEVICE_SETTINGS_BP)


class SettingsResource(Resource):

    #@token_required()
    def get(self):
        return "Hello world"


api.add_resource(SettingsResource, '/device/{rsc}'.format(rsc=API_PREFIX))