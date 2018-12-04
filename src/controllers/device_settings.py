from models import DeviceSettings


class DeviceSettingsController:
    def get_settings(self, token:str) -> DeviceSettings:
        return DeviceSettings()
    
    def edit_settings(self, token:str, new_settings:DeviceSettings) -> DeviceSettings:
        return new_settings
