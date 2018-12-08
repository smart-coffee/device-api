import requests

from models import DeviceSettings
from core import CM_API, WEB_API


class DeviceSettingsController:
    def get_settings(self, token:str) -> DeviceSettings:
        return CM_API.settings
    
    def edit_settings(self, token:str, new_settings:DeviceSettings) -> DeviceSettings:
        coffee_machine_id = new_settings.coffee_machine_id
        coffee_product_id = new_settings.coffee_product_id

        coffee_machine = WEB_API.get_coffee_machine(token, coffee_machine_id)
        coffee_product = WEB_API.get_coffee_product(token, coffee_product_id)

        CM_API.settings = new_settings
        return CM_API.settings
