from models import DeviceStatus, EditDeviceStatus, DeviceRuntimeState
from core import CM_API, RemoteSession
from config.flask_config import ResourceException

class DeviceStatusController:
    def get_status(self, token:str) -> DeviceStatus:
        return CM_API.status
    
    def set_status(self, token:str, status:EditDeviceStatus) -> DeviceStatus:
        session = RemoteSession(cm_hw_api=CM_API)
        session.open()

        state = status.device_runtime_state
        if state == DeviceRuntimeState.ON:
            self.turn_on(token)
        if state == DeviceRuntimeState.OFF:
            self.turn_off(token)

        new_status = CM_API.status
        new_status.coffee_machine_runtime_state = state.state_id
        session.close()
        return new_status

    def turn_on(self, token: str) -> DeviceStatus:
        status = CM_API.status
        if status.is_on():
            raise ResourceException(status_code=405, message='Kaffeemaschine ist nicht bereit.')
        CM_API.toggle_power()
        return CM_API.status
    
    def turn_off(self, token: str) -> DeviceStatus:
        status = CM_API.status
        if status.is_off():
            raise ResourceException(status_code=405, message='Kaffeemaschine ist nicht bereit.')
        CM_API.toggle_power()
        return CM_API.status