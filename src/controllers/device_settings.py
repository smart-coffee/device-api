from models import DeviceSettings
from core import CM_API


class DeviceSettingsController:
    def get_settings(self, token:str) -> DeviceSettings:
        return CM_API.settings
    
    def edit_settings(self, token:str, new_settings:DeviceSettings) -> DeviceSettings:
        CM_API.settings = new_settings
        return CM_API.settings
