import json
import os
import errno

from pathlib import Path
from models import DeviceSettings, DeviceStatus

from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeMachineHardwareAPI:
    _settings_file = Path('coffee_machine_settings.json')

    def __init__(self):
        self.file_path = CoffeeMachineHardwareAPI._settings_file

    @property
    def settings(self) -> DeviceSettings:
        self.read_settings()
        return self._settings

    @settings.setter
    def settings(self, new_settings: DeviceSettings):
        settings_as_dict = new_settings.__dict__
        with open(self.file_path, 'w') as f:
            json.dump(settings_as_dict, f)
        self.read_settings()

    @property
    def status(self) -> DeviceStatus:
        self.read_status()
        return self._status

    def init_settings(self):
        if self.file_path.exists():
            logger.debug('{file} found.'.format(file=self.file_path))
            return
        logger.debug('{file} not found. Initializing with default settings.'.format(file=self.file_path))
        self.settings = DeviceSettings()

    def read_settings(self):
        if not self.file_path.exists():
            self.init_settings()
        logger.debug('Reading config from: {file} '.format(file=self.file_path))
        with open(self.file_path, 'r') as f:
            settings_as_dict = json.load(f)
            settings = DeviceSettings(**settings_as_dict)
            self._settings = settings
    
    def read_status(self):
        self._status = DeviceStatus()
        logger.warning('Should read status of coffee machine here and set it to self._status')


CM_API = CoffeeMachineHardwareAPI()
CM_API.init_settings()
CM_API.read_settings()