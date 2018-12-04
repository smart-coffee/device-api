from models import DeviceStatus
from core import CM_API

class DeviceStatusController:
    def get_status(self, token:str) -> DeviceStatus:
        return CM_API.status
