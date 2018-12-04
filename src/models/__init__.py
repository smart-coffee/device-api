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
        self.coffee_strength_in_percent = -1 if not ('coffee_strength_in_percent' in kwargs) else kwargs['coffee_strength_in_percent']
        self.water_in_percent = -1 if not ('water_in_percent' in kwargs) else kwargs['water_in_percent']
        self.doses = -1 if not ('doses' in kwargs) else kwargs['doses']
    
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
        self.id = None if not ('id' in kwargs) else kwargs['id']
        self.create_date = None if not ('create_date' in kwargs) else kwargs['create_date']
        self.square_date = None if not ('square_date' in kwargs) else kwargs['square_date']
        self.coffee_machine_id = None if not ('coffee_machine_id' in kwargs) else kwargs['coffee_machine_id']
        self.coffee_strength_in_percent = None if not ('coffee_strength_in_percent' in kwargs) else kwargs['coffee_strength_in_percent']
        self.water_in_percent = None if not ('water_in_percent' in kwargs) else kwargs['water_in_percent']
        self.price = None if not ('price' in kwargs) else kwargs['price']
        self.doses = None if not ('doses' in kwargs) else kwargs['doses']
        self.coffee_product_id = None if not ('coffee_product_id' in kwargs) else kwargs['coffee_product_id']
    
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
