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
