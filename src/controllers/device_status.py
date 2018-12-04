from models import DeviceStatus


class DeviceStatusController:
    def get_status(self, token:str) -> DeviceStatus:
        return DeviceStatus()
