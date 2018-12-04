import json

from typing import List

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api, marshal_with, Resource

from utils.http import token_required, get_post_response
from models import DeviceSettings, DeviceStatus, DeviceJob, CreateDeviceJob
from controllers.device_settings import DeviceSettingsController
from controllers.device_status import DeviceStatusController
from controllers.device_job import DeviceJobController

API_PREFIX = 'device'
DEVICE_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(DEVICE_BP)


class DeviceSettingsResource(Resource):
    def __init__(self):
        self.controller = DeviceSettingsController()

    @token_required()
    @swag_from('/resources/device/description/device_settings_get.yml')
    @marshal_with(DeviceSettings.get_fields())
    def get(self, token:str) -> DeviceSettings:
        return self.controller.get_settings(token)
    
    @token_required()
    @swag_from('/resources/device/description/device_settings_put.yml')
    @marshal_with(DeviceSettings.get_fields())
    def put(self, token:str) -> DeviceSettings:
        data = request.get_json()
        new_settings = DeviceSettings(**data)
        return self.controller.edit_settings(token, new_settings)


class DeviceStatusResource(Resource):
    def __init__(self):
        self.controller = DeviceStatusController()

    @token_required()
    @swag_from('/resources/device/description/device_status_get.yml')
    @marshal_with(DeviceStatus.get_fields())
    def get(self, token:str) -> DeviceStatus:
        return self.controller.get_status(token)


class DeviceJobResource(Resource):
    def __init__(self):
        self.controller = DeviceJobController()
    
    @token_required()
    @swag_from('/resources/device/description/device_job_post.yml')
    def post(self, token:str):
        data = request.get_json()
        new_job = CreateDeviceJob(**data)
        created_job = self.controller.create_job(token, new_job)
        response = get_post_response(body=created_job, content_type='application/json', api='/{rsc}/job'.format(rsc=API_PREFIX), obj_id=created_job.id)
        return response


api.add_resource(DeviceSettingsResource, '/{rsc}/settings'.format(rsc=API_PREFIX))
api.add_resource(DeviceStatusResource, '/{rsc}/status'.format(rsc=API_PREFIX))
api.add_resource(DeviceJobResource, '/{rsc}/job'.format(rsc=API_PREFIX))