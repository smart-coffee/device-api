from enum import Enum
from flask_restful import fields

from config import SWAG


@SWAG.definition('DeviceSettings')
class DeviceSettings:
    """
    file: /models/device-settings.yml
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


class DeviceRuntimeState(Enum):
    ON = (1)
    OFF = (2)
    STARTUP = (3)
    SHUTDOWN = (4)

    def __init__(self, state_id):
        self._state_id = state_id

    @property
    def state_id(self):
        return self._state_id


@SWAG.definition('DeviceStatus')
class DeviceStatus:
    """
    file: /models/device-status.yml
    """
    def __init__(self, *args, **kwargs):
        self.device_ready = True
        self.water_tank_ready = True
        self.water_tank_fill_level_in_percent = 53
        self.coffee_bean_container_ready = True
        self.coffee_bean_container_fill_level_in_percent = 71
        self.coffee_grounds_container_ready = True
        self.coffee_grounds_container_fill_level_in_percent = 23
        self.coffee_machine_runtime_state = DeviceRuntimeState.OFF.state_id
        self.device_eco_mode = False
        self.device_maintenance = False
        self.device_steam = False
    
    @property
    def device_runtime_state(self) -> DeviceRuntimeState:
        state_id = self.coffee_machine_runtime_state
        for state in DeviceRuntimeState:
            if state.state_id == state_id:
                return state
        raise ValueError('Unknown state.')
    
    def is_on(self):
        state = self.device_runtime_state
        return state == DeviceRuntimeState.ON
    
    def is_off(self):
        state = self.device_runtime_state
        return state == DeviceRuntimeState.OFF
        
    @staticmethod
    def get_fields():
        return {
            'device_ready': fields.Boolean,
            'water_tank_ready': fields.Boolean,
            'water_tank_fill_level_in_percent': fields.Integer,
            'coffee_bean_container_ready': fields.Boolean,
            'coffee_bean_container_fill_level_in_percent': fields.Integer,
            'coffee_grounds_container_ready': fields.Boolean,
            'coffee_grounds_container_fill_level_in_percent': fields.Integer,
            'coffee_machine_runtime_state': fields.Integer,
            'device_eco_mode': fields.Boolean,
            'device_maintenance': fields.Boolean,
            'device_steam': fields.Boolean
        }

@SWAG.definition('EditDeviceStatus')
class EditDeviceStatus:
    """
    file: /models/device-status-edit.yml
    """
    def __init__(self, *args, **kwargs):
        self.coffee_machine_runtime_state = None if not ('coffee_machine_runtime_state' in kwargs) else kwargs['coffee_machine_runtime_state']
        self.device_eco_mode = None if not ('device_eco_mode' in kwargs) else kwargs['device_eco_mode']
        self.device_maintenance = None if not ('device_maintencance' in kwargs) else kwargs['device_maintenance']
        self.device_steam = None if not ('device_steam' in kwargs) else kwargs['device_steam']
    
    @property
    def device_runtime_state(self) -> DeviceRuntimeState:
        state_id = self.coffee_machine_runtime_state
        for state in DeviceRuntimeState:
            if state.state_id == state_id:
                return state
        raise ValueError('Unknown state.')
    
    @staticmethod
    def get_fields():
        return {
            'coffee_machine_runtime_state': fields.Integer,
            'device_eco_mode': fields.Boolean,
            'device_maintenance': fields.Boolean,
            'device_steam': fields.Boolean
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


class I2CBus:
    def __init__(self, *args, **kwargs):
        self.bus_number = None if not ('bus_number' in kwargs) else kwargs['bus_number']
        self.bus_delay = None if not ('bus_delay' in kwargs) else kwargs['bus_delay']
        self.addresses = None if not ('addresses' in kwargs) else kwargs['addresses']