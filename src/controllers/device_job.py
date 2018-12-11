from models import DeviceJob, CreateDeviceJob
from core import CM_API, WEB_API
from config.flask_config import ResourceException


class DeviceJobController:
    def create_job(self, token:str, create_job: CreateDeviceJob) -> DeviceJob:
        status = CM_API.status
        if not status.device_ready:
            raise ResourceException(status_code=405, message='Device is not ready.')
        settings = CM_API.settings
        create_job_body = {
            **(create_job.__dict__),
            **(settings.__dict__)
        }
        doses = create_job.doses
        CM_API.make_coffee(doses=doses)
        response = WEB_API.create_job(token, create_job_body)
        response_json = response.json()

        return DeviceJob(**response_json)
