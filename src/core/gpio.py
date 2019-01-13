from typing import List
import RPi.GPIO as GPIO
import time


class RemoteGPIOSession:
    def __init__(self, relais_gpio, relais_value, *args, **kwargs):
        self._relais_gpio = relais_gpio
        self._relais_value = relais_value
        self._opened = False
        self._closed = False
    
    def is_open(self):
        return self._opened
    
    def is_closed(self):
        return self._closed
    
    def open(self):
        self._opened = True
        self._closed = False
        gpio = self._relais_gpio
        value = self._relais_value
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, value)
    
    def close(self):
        GPIO.cleanup()
        self._opened = False
        self._closed = True


class GPIORead:
    def __init__(self, gpio_number: int, value: bool, time_in_milli: int):
        self.gpio_number = gpio_number
        self.value = value
        self.time_in_milli = time_in_milli
    
    def __repr__(self):
        #return str(self.__dict__)
        gpio_number_str = str(self.gpio_number).zfill(2)
        time_str = self.time_in_milli
        value_str = self.value
        return '{0} {1}: {2}'.format(gpio_number_str, time_str, value_str)

    def __eq__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        if gpio_number_self != gpio_number_other:
            return False
        
        value_other = other.value
        value_self = self.value
        return value_self == value_other

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash((self.gpio_number, self.value))
    
    def __lt__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self < gpio_number_other

    def __le__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self <= gpio_number_other

    def __gt__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self > gpio_number_other

    def __ge__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self >= gpio_number_other


def read_gpio_list(gpio_numbers: List[int], sample_rate: int = 100, check_cycles: int = 1, session = None) -> List[GPIORead]:
    if check_cycles < 1:
        raise ValueError('Check cycles must be greater than 0')
    
    read_cycles = []
    for i in range(0, check_cycles):
        single_read = _read_gpio_list_single_cycle(gpio_numbers=gpio_numbers, sample_rate=sample_rate, session=session)
        read_cycles.append(single_read)
    
    base_cycle = read_cycles[0]
    del read_cycles[0]

    for read_cycle in read_cycles:
        base_cycle = set(base_cycle).intersection(read_cycle)
    
    return base_cycle

    
def _read_gpio_list_single_cycle(gpio_numbers: List[int], sample_rate: int, session) -> List[GPIORead]:
    if session is None:
        GPIO.setmode(GPIO.BCM)
    for gpio in gpio_numbers:
        GPIO.setup(gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    reads = []
    for gpio in gpio_numbers:
        _found_high = False
        for i in range(0, sample_rate):
            _val = GPIO.input(gpio)
            if _val == GPIO.HIGH:
                _found_high = True
                _time_in_milli = int(round(time.time() * 1000))
                reads.append(GPIORead(gpio_number=gpio, value=True, time_in_milli=_time_in_milli))
                break
        if not _found_high:
            _time_in_milli = int(round(time.time() * 1000))
            reads.append(GPIORead(gpio_number=gpio, value=False, time_in_milli=_time_in_milli))
    
    if session is None:
        GPIO.cleanup()
    return reads


def set_gpio(gpio_number: int, value: bool, duration_in_sec, session = None):
    if session is None:
        GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(gpio_number, GPIO.OUT)
    GPIO.output(gpio_number, value)

    if not (duration_in_sec is None):
        time.sleep(duration_in_sec)
        GPIO.output(gpio_number, not value)

    if session is None:
        GPIO.cleanup()
