from models import DeviceStatus, EditDeviceStatus, DeviceRuntimeState
from core import CM_API, RemoteSession
from config.flask_config import ResourceException
from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class DeviceStatusController:
    def get_status(self, token:str) -> DeviceStatus:
        return CM_API.status
    
    def set_status(self, token:str, status:EditDeviceStatus) -> DeviceStatus:
        session = RemoteSession(cm_hw_api=CM_API)
        session.open()
        try:
            state = status.device_runtime_state
            current_status = CM_API.status
            if not(state is None):
                logger.info('Changing runtime state.')
                if state == DeviceRuntimeState.ON:
                    current_status = self.turn_on(token, current_status)
                elif state == DeviceRuntimeState.OFF:
                    current_status = self.turn_off(token, current_status)

            eco_mode = status.device_eco_mode
            if not(eco_mode is None):
                logger.info('Changing eco mode.')
                if eco_mode:
                    current_status = self.turn_eco_mode_on(current_status)
                elif not eco_mode:
                    current_status = self.turn_eco_mode_off(current_status)

            maintenance = status.device_maintenance
            if not(maintenance is None):
                logger.info('Changing maintenance.')
                if maintenance:
                    current_status = self.turn_maintenance_on(current_status)
                elif not maintenance:
                    current_status = self.turn_maintenance_off(current_status)

            steam = status.device_steam
            if not(steam is None):
                logger.info('Changing steam.')
                if steam:
                    current_status = self.turn_steam_on(current_status)
                elif not steam:
                    current_status = self.turn_steam_off(current_status)

            new_status = CM_API.status
            new_status.coffee_machine_runtime_state = state.state_id
        except ValueError as err:
            raise ResourceException(status_code=404, message=str(err))
        finally:
            session.close()
            
        return new_status

    def turn_on(self, token: str, status: DeviceStatus) -> DeviceStatus:
        if status.is_on():
            logger.info('Coffee Machine is already on.')
            return status
        logger.info('Coffee Machine Runtime State: ON')
        CM_API.toggle_power()
        return CM_API.status
    
    def turn_off(self, token: str, status: DeviceStatus) -> DeviceStatus:
        if status.is_off():
            logger.info('Coffee Machine is already off.')
            return status
        logger.info('Coffee Machine Runtime State: OFF')
        CM_API.toggle_power()
        return CM_API.status
    
    def turn_eco_mode_on(self, status: DeviceStatus) -> DeviceStatus:
        if status.device_eco_mode:
            logger.info('Coffee Machine eco mode is already on.')
            return status
        logger.info('Coffee Machine ECO: ON')
        CM_API.toggle_eco()
        return CM_API.status
    
    def turn_eco_mode_off(self, status: DeviceStatus) -> DeviceStatus:
        if not status.device_eco_mode:
            logger.info('Coffee Machine eco mode is already off.')
            return status
        logger.info('Coffee Machine ECO: OFF')
        CM_API.toggle_eco()
        return CM_API.status

    def turn_maintenance_on(self, status: DeviceStatus) -> DeviceStatus:
        if status.device_maintenance:
            logger.info('Coffee Machine maintenance is already on.')
            return status
        logger.info('Coffee Machine Maintenance: ON')
        CM_API.toggle_maintenance()
        return CM_API.status
    
    def turn_maintenance_off(self, status: DeviceStatus) -> DeviceStatus:
        if not status.device_maintenance:
            logger.info('Coffee Machine maintenance is already off.')
            return status
        logger.info('Coffee Machine Maintenance: OFF')
        CM_API.toggle_maintenance()
        return CM_API.status
    
    def turn_steam_on(self, status: DeviceStatus) -> DeviceStatus:
        if status.device_steam:
            logger.info('Coffee Machine steam is already on.')
            return status
        logger.info('Coffee Machine Steam: ON')
        CM_API.toggle_steam()
        return CM_API.status
    
    def turn_steam_off(self, status: DeviceStatus) -> DeviceStatus:
        if not status.device_steam:
            logger.info('Coffee Machine steam is already off.')
            return status
        logger.info('Coffee Machine Steam: OFF')
        CM_API.toggle_steam()
        return CM_API.status