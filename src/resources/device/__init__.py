from typing import List

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api, marshal_with, Resource

from utils.http import token_required
from models import DeviceSettings
from controllers.device_settings import DeviceSettingsController

API_PREFIX = 'device'
DEVICE_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(DEVICE_BP)


class DeviceSettingsResource(Resource):
    def __init__(self):
        self.controller = DeviceSettingsController()

    @token_required()
    @swag_from('/resources/device/description/device_settings_get.yml')
    @marshal_with(DeviceSettings.get_fields())
    def get(self, token:str):
        return self.controller.get_settings(token)
    
    @token_required()
    @swag_from('/resources/device/description/device_settings_put.yml')
    @marshal_with(DeviceSettings.get_fields())
    def put(self, token:str):
        data = request.get_json()
        new_settings = DeviceSettings(**data)
        return self.controller.edit_settings(token, new_settings)

api.add_resource(DeviceSettingsResource, '/{rsc}/settings'.format(rsc=API_PREFIX))