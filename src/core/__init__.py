import json
import os
import errno
import requests

from typing import List
from pathlib import Path

from models import DeviceSettings, DeviceStatus, DeviceRuntimeState
from config.logger import logging, get_logger_name
from config.environment_tools import get_webapi_domain, get_webapi_port, get_ssl_ca_bundle
from config.flask_config import ResourceException
from core.gpio import set_gpio, RemoteGPIOSession, read_gpio_list, GPIORead
from core.i2c import set_dac_value


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeMachineHardwareAPI:
    _settings_file = Path('/data/coffee_machine_settings.json')

    def __init__(self):
        self.file_path = CoffeeMachineHardwareAPI._settings_file
        self._session = None

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
        gpio_numbers = list(GPIO_IN_PINS.values())
        session = self._session
        reads = read_gpio_list(gpio_numbers=gpio_numbers, sample_rate=SAMPLE_RATE, check_cycles=CHECK_CYCLES, session=session)
        status = DeviceStatus()

        # Check water LED
        water_gpio = GPIO_IN_PINS['WATER']
        water_led = self._read_single_status(gpio_reads=reads, gpio_number=water_gpio, fallback=True, status_name='Water LED')
        
        # Check coffee grounds LED
        coffee_grounds_gpio = GPIO_IN_PINS['COFFEE_GROUNDS_CONTAINER']
        coffee_grounds_led = self._read_single_status(gpio_reads=reads, gpio_number=coffee_grounds_gpio, fallback=True, status_name='Coffee Grounds Container LED')

        # Check one dose LED
        one_dose_gpio = GPIO_IN_PINS['ONE_DOSE']
        one_dose_led = self._read_single_status(gpio_reads=reads, gpio_number=one_dose_gpio, fallback=False, status_name='One Dose LED')

        # Check two doses LED
        two_doses_gpio = GPIO_IN_PINS['TWO_DOSES']
        two_doses_led = self._read_single_status(gpio_reads=reads, gpio_number=two_doses_gpio, fallback=False, status_name='Two Doses LED')

        # Check warning LED
        warning_gpio = GPIO_IN_PINS['WARNING']
        warning_led = self._read_single_status(gpio_reads=reads, gpio_number=warning_gpio, fallback=True, status_name='Warning LED')

        # Steam LED
        steam_gpio = GPIO_IN_PINS['STEAM']
        steam_led = self._read_single_status(gpio_reads=reads, gpio_number=steam_gpio, fallback=False, status_name='Steam LED')

        # Check maintenance LED
        maintenance_gpio = GPIO_IN_PINS['MAINTENANCE']
        maintenance_led = self._read_single_status(gpio_reads=reads, gpio_number=maintenance_gpio, fallback=True, status_name='Maintenance LED')

        # Check eco LED
        eco_gpio = GPIO_IN_PINS['ECO']
        eco_led = self._read_single_status(gpio_reads=reads, gpio_number=eco_gpio, fallback=False, status_name='Eco LED')

        # Set status
        status.water_tank_ready = water_led is False
        status.coffee_grounds_container_ready = coffee_grounds_led is False
        is_on = one_dose_led and two_doses_led
        runtime_state = DeviceRuntimeState.ON if is_on else DeviceRuntimeState.OFF
        status.coffee_machine_runtime_state = runtime_state.state_id
        is_ready = status.water_tank_ready and status.coffee_grounds_container_ready and is_on

        self._status = status

    def _read_single_status(self, gpio_reads: List[GPIORead], gpio_number: int, fallback: bool, status_name: str) -> bool:
        logger.debug('Start checking {}'.format(status_name))
        filtered_gpio_read = (r for r in gpio_reads if r.gpio_number == gpio_number)

        return_value = fallback
        if len(list(filtered_gpio_read) > 0):
            gpio_read = next(filtered_gpio_read)
            return_value = gpio_read.value
        else:
            logger.debug('GPIO {0} status was not found in result list. Returning fallback: {1}'.format(gpio_number, fallback))
        logger.debug('Check of {0} (GPIO {1}) done: {2}'.format(status_name, gpio_number, return_value))

        return return_value

    def use_session(self, session):
        self._session = session

    def set_water_in_percent(self, water_in_percent: int):
        address = I2C_ADDRESS_MAPPINGS['WATER']
        sensor_name = 'Water'
        bus_number = I2C_BUS_NUMBER
        try:
            set_dac_value(bus_number=bus_number, address=address, percent_value=water_in_percent, i2c_delay=I2C_DELAY, sensor_name=sensor_name)
        except ValueError as err:
            raise ResourceException(status_code=400, message='Percent value of sensor {0} is invalid: {1}'.format(sensor_name, water_in_percent))
    
    def set_coffee_strength_in_percent(self, coffee_strength_in_percent: int):
        address = I2C_ADDRESS_MAPPINGS['COFFEE_STRENGTH']
        sensor_name = 'Coffee Strength'
        bus_number = I2C_BUS_NUMBER
        try:
            set_dac_value(bus_number=bus_number, address=address, percent_value=coffee_strength_in_percent, i2c_delay=I2C_DELAY, sensor_name=sensor_name)
        except ValueError as err:
            raise ResourceException(status_code=400, message='Percent value of sensor {0} is invalid: {1}'.format(sensor_name, coffee_strength_in_percent))

    def make_coffee(self, doses: int):
        if doses == 1:
            pin = GPIO_OUT_PINS['ONE_DOSE']
        elif doses == 2:
            pin = GPIO_OUT_PINS['TWO_DOSES']
        else:
            msg = 'Kaffeeauftrag mit {doses} Dosen nicht möglich.'.format(doses=doses)
            logger.error(msg)
            raise ResourceException(status_code=405, message=msg)
        self.press_button(pin = pin)
    
    def toggle_power(self):
        pin = GPIO_OUT_PINS['POWER']
        self.press_button(pin = pin)
    
    def press_button(self, pin: int):
        session = self._session
        set_gpio(gpio_number=pin, value=False, duration_in_sec=BUTTON_PRESS_DURATION, session=session)
    

class RemoteSession:
    def __init__(self, cm_hw_api: CoffeeMachineHardwareAPI, *args, **kwargs):
        self._api = cm_hw_api
        _relais_gpio = GPIO_OUT_PINS['RELAIS'] 
        self._gpio_session = RemoteGPIOSession(relais_gpio=_relais_gpio, relais_value=True)
    
    def open(self):
        self._api.use_session(self)
        self._gpio_session.open()
    
    def close(self):
        self._api.use_session(None)
        self._gpio_session.close()
    
    

I2C_BUS_NUMBER = 1

I2C_ADDRESS_MAPPINGS = {
    'WATER': 0x61,
    'COFFEE_STRENGTH': 0x60
}

I2C_DELAY = 0.05

# GPIO-OUT mappings
GPIO_OUT_PINS = {
    'ONE_DOSE': 17,
    'TWO_DOSES': 27,
    'STEAM': 14,
    'ECO': 18,
    'POWER': 4,
    'MAINTENANCE': 15,
    'RELAIS': 21
}

# GPIO-IN mappings
GPIO_IN_PINS = {
    'ECO': 23,
    'MAINTENANCE': 22,
    'WARNING': 24,
    'STEAM': 10,
    'TWO_DOSES': 8,
    'ONE_DOSE': 26,
    'WATER': 19,
    'COFFEE_GROUNDS_CONTAINER': 11 
}

# Reads a single GPIO-IN signal X amount of times and then continues with the next GPIO-IN signal
SAMPLE_RATE = 500

# 1 x "Check cycle" = read a list of GPIO-IN signals 1 time
# 2 x "Check cycle" = read a list of GPIO-IN signals 2 times and merge the results
# If the result of multiple read cycles aren't equal, the missmatching results will be filtered out
# Higher check cycles will increase the accuracy but also increase the duration of the operation
CHECK_CYCLES = 5

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