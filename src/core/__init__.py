import json
import os
import errno
import requests
import time

import RPi.GPIO as GPIO

from pathlib import Path
from smbus2 import SMBus

from models import DeviceSettings, DeviceStatus
from config.logger import logging, get_logger_name
from config.environment_tools import get_webapi_domain, get_webapi_port, get_ssl_ca_bundle
from config.flask_config import ResourceException


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeMachineHardwareAPI:
    _settings_file = Path('/data/coffee_machine_settings.json')

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

    def set_water_in_percent(self, water_in_percent: int):
        address = I2C_ADDRESS_MAPPINGS['WATER']
        bus_number = I2C_BUS_NUMBER
        self.set_dac_value(bus_number=bus_number, address=address, percent_value=water_in_percent, sensor_name='Water')
    
    def set_coffee_strength_in_percent(self, coffee_strength_in_percent: int):
        address = I2C_ADDRESS_MAPPINGS['COFFEE_STRENGTH']
        bus_number = I2C_BUS_NUMBER
        self.set_dac_value(bus_number=bus_number, address=address, percent_value=coffee_strength_in_percent, sensor_name='Coffee Strength')

    def make_coffee(self, doses: int):
        if doses == 1:
            pin = GPIO_PINS['ONE_DOSE']
        elif doses == 2:
            pin = GPIO_PINS['TWO_DOSES']
        else:
            msg = 'Kaffeeauftrag mit {doses} Dosen nicht möglich.'.format(doses=doses)
            logger.error(msg)
            raise ResourceException(status_code=405, message=msg)
        self.press_button(pin = pin)
    
    def toggle_power(self):
        pin = GPIO_PINS['POWER']
        self.press_button(pin = pin)
    
    def press_button(self, pin: int):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        time.sleep(BUTTON_PRESS_DURATION)
        GPIO.cleanup()
    
    def set_dac_value(self, bus_number: int, address: int, percent_value: int, sensor_name: str='Unknown'):
        if address is None:
            logger.warning('Sensor {} i2c bus address is not configured.'.format(sensor_name))
            return

        if percent_value > 100:
            raise ResourceException(status_code=400, message='Percent value of sensor {} can not be greater than 100.'.format(sensor_name))


        bus = SMBus(bus_number)
        reg_write_dac = 0x40
        
        # Create our 12-bit number representing relative voltage
        max_voltage = 0xFFF
        rate = percent_value / 100
        voltage = int(max_voltage * rate) & 0xFFF

        # Shift everything left by 4 bits and separate bytes
        msg = (voltage & 0xff0) >> 4
        msg = [msg, (msg & 0xf) << 4]

        # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
        bus.write_i2c_block_data(address, reg_write_dac, msg)
        time.sleep(I2C_DELAY)

I2C_BUS_NUMBER = 1

I2C_ADDRESS_MAPPINGS = {
    'WATER': None,
    'COFFEE_STRENGTH': 0x60
}

I2C_DELAY = 0.05

GPIO_PINS = {
    'ONE_DOSE': 26,
    'TWO_DOSES': 12,
    'STEAM': None,
    'ECO': None,
    'POWER': 16,
    'MAINTENANCE': None
}

BUTTON_PRESS_DURATION = 2

ROUTES = {
    'COFFEE_MACHINE': '{base_url}/api/coffee/machines/{id}',
    'COFFEE_PRODUCT': '{base_url}/api/coffee/products/{id}',
    'CREATE_JOB': '{base_url}/api/users/current/jobs',
    'IS_USER': '{base_url}/api/auth/refresh',
    'IS_ADMIN': '{base_url}/api/users'
}


class WebAPI:
    def __init__(self, domain: str, port: int, ssl_ca_bundle: str):
        self._domain = domain
        self._port = port
        self._ssl_ca_bundle = ssl_ca_bundle
    
    @property
    def url(self):
        return '{domain}:{port}'.format(domain=self._domain, port=self._port)

    def is_user(self, token: str):
        is_user_url = ROUTES['IS_USER'].format(base_url=self.url)
        is_user_response = self.post(is_user_url, token)
        return is_user_response

    def is_admin(self, token: str):
        is_admin_url = ROUTES['IS_ADMIN'].format(base_url=self.url)
        is_admin_response = self.get(is_admin_url, token)
        return is_admin_response

    
    def get_coffee_machine(self, token: str, coffee_machine_id: int):
        coffee_machine_url = ROUTES['COFFEE_MACHINE'].format(base_url=self.url, id=coffee_machine_id)
        coffee_machine_response = self.get(coffee_machine_url, token)
        return coffee_machine_response

    def get_coffee_product(self, token: str, coffee_product_id: int):
        coffee_product_url = ROUTES['COFFEE_PRODUCT'].format(base_url=self.url, id=coffee_product_id)
        coffee_product_response = self.get(coffee_product_url, token)
        return coffee_product_response

    def create_job(self, token: str, job_json):
        create_job_url = ROUTES['CREATE_JOB'].format(base_url=self.url)
        return self.post(create_job_url, token, job_json)
    
    def get(self, url: str, token: str):
        headers = {"x-access-token":token}
        verify = self._ssl_ca_bundle
        response = requests.get(url, headers=headers, verify=verify)
        self._check_response(response)
        return response
    
    def post(self, url: str, token: str, json=None):
        headers = {"x-access-token":token}
        verify = self._ssl_ca_bundle
        response = requests.post(url, headers=headers, verify=verify, json=json)
        self._check_response(response)
        return response

    def _check_response(self, response):
        status_code = response.status_code
        if 200 <= status_code <= 302:
            return
        json_obj = response.json()
        raise ResourceException(status_code=status_code, message=json_obj['message'])

CM_API = CoffeeMachineHardwareAPI()
CM_API.init_settings()
CM_API.read_settings()

domain=get_webapi_domain()
port=get_webapi_port()
ssl_ca_bundle=get_ssl_ca_bundle()
WEB_API = WebAPI(domain=domain, port=port, ssl_ca_bundle=ssl_ca_bundle)