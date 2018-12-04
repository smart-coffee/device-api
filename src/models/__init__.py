from flask_restful import fields

from config import SWAG


@SWAG.definition('DeviceSettings')
class DeviceSettings:
    """
    file: /models/device_settings.yml
    """
    def __init__(self, *args, **kwargs):
        self.coffee_machine_id = -1 if not ('coffee_machine_id' in kwargs) else kwargs['coffee_machine_id']
        self.coffee_product_id = -1 if not ('coffee_product_id' in kwargs) else kwargs['coffee_product_id']
        self.price = -1 if not ('price' in kwargs) else kwargs['price']
    
    @staticmethod
    def get_fields():
        return {
            'coffee_machine_id': fields.Integer,
            'coffee_product_id': fields.Integer,
            'price': fields.Integer
        }

@SWAG.definition('DeviceStatus')
class DeviceStatus:
    """
    file: /models/device_status.yml
    """
    def __init__(self, *args, **kwargs):
        self.device_ready = False
        self.water_tank_ready = False
        self.water_tank_fill_level_in_percent = 1
        self.coffee_bean_container_ready = False
        self.coffee_bean_container_fill_level_in_percent = 1
        self.coffee_grounds_container_ready = False
        self.coffee_grounds_container_fill_level_in_percent = 1
    
    @staticmethod
    def get_fields():
        return {
            'device_ready': fields.Boolean,
            'water_tank_ready': fields.Boolean,
            'water_tank_fill_level_in_percent': fields.Integer,
            'coffee_bean_container_ready': fields.Boolean,
            'coffee_bean_container_fill_level_in_percent': fields.Integer,
            'coffee_grounds_container_ready': fields.Integer,
            'coffee_grounds_container_fill_level_in_percent': fields.Integer
        }


@SWAG.definition('CreateDeviceJob')
class CreateDeviceJob:
    """
    file: /models/device-job-create.yml
    """
    def __init__(self, *args, **kwargs):
        self.coffee_strength_in_percent = 1
        self.water_in_percent = 1
        self.doses = 1
    
    @staticmethod
    def get_fields():
        return {
            'coffee_strength_in_percent': fields.Integer,
            'water_in_percent': fields.Integer,
            'doses': fields.Integer
        }


@SWAG.definition('DeviceJob')
class DeviceJob:
    """
    file: /models/device-job.yml
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.create_date = None
        self.square_date = None
        self.coffee_machine_id = None
        self.coffee_strength_in_percent = None
        self.water_in_percent = None
        self.price = None
        self.doses = None
        self.coffee_product_id = None
    
    @staticmethod
    def get_fields():
        return {
            'id': fields.Integer,
            'create_date': fields.Integer,
            'square_date': fields.Integer,
            'coffee_machine_id': fields.Integer,
            'coffee_strength_in_percent': fields.Integer,
            'water_in_percent': fields.Integer,
            'price': fields.Integer,
            'doses': fields.Integer,
            'coffee_product_id': fields.Integer
        }


class CoffeeMachine:
    def __init__(self, device_settings: DeviceSettings, *args, **kwargs):
        self.settings = device_settings