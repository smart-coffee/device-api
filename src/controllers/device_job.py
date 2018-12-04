from models import DeviceJob, CreateDeviceJob
from core import CM_API


class DeviceJobController:
    def create_job(self, token:str, create_job: CreateDeviceJob) -> DeviceJob:
        job_id = 1
        job_create_date = 12345
        job_square_date = None
        settings = CM_API.settings
        return DeviceJob(id=job_id, create_date=job_create_date, square_date=job_square_date, **(create_job.__dict__), **settings.__dict__)
