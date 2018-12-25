from models import DeviceJob, CreateDeviceJob
from core import CM_API, WEB_API
from config.flask_config import ResourceException
from utils.basic import validate_percent_value, get_percent_value


from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))

class DeviceJobController:
    def create_job(self, token:str, create_job: CreateDeviceJob) -> DeviceJob:
        status = CM_API.status
        if not status.device_ready:
            raise ResourceException(status_code=405, message='Kaffeemaschine ist nicht bereit.')
        settings = CM_API.settings
        create_job_body = {
            **(create_job.__dict__),
            **(settings.__dict__)
        }
        water_in_percent = create_job.water_in_percent
        water_in_percent = get_percent_value(value=water_in_percent, accuracy=0)
        coffee_strength_in_percent = create_job.coffee_strength_in_percent
        coffee_strength_in_percent = get_percent_value(value=coffee_strength_in_percent, accuracy=0)
        doses = create_job.doses
        logger.debug('Doses: {0}, Water: {1}, Coffee: {2}'.format(doses, water_in_percent, coffee_strength_in_percent))
        CM_API.set_water_in_percent(water_in_percent=water_in_percent)
        CM_API.set_coffee_strength_in_percent(coffee_strength_in_percent=coffee_strength_in_percent)
        CM_API.make_coffee(doses=doses)
        response = WEB_API.create_job(token, create_job_body)
        response_json = response.json()

        return DeviceJob(**response_json)
