from models import DeviceJob, CreateDeviceJob


class DeviceJobController:
    def create_job(self, token:str) -> DeviceJob:
        return DeviceJob()
