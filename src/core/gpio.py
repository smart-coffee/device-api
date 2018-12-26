from typing import List
import RPi.GPIO as GPIO
import time


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
    
    def __hash__(self):
        return hash((self.gpio_number, self.value))
    
    def __lt__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self < gpio_number_other
    
    def __gt__(self, other):
        gpio_number_other = other.gpio_number
        gpio_number_self = self.gpio_number
        return gpio_number_self < gpio_number_other


def read_gpio_list(gpio_numbers: List[int], sample_rate: int = 100, check_cycles: int = 1) -> List[GPIORead]:
    if check_cycles < 1:
        raise ValueError('Check cycles must be greater than 0')
    
    read_cycles = []
    for i in range(0, check_cycles):
        single_read = _read_gpio_list_single_cycle(gpio_numbers=gpio_numbers, sample_rate=sample_rate)
        read_cycles.append(single_read)
    
    base_cycle = read_cycles[0]
    del read_cycles[0]

    for read_cycle in read_cycles:
        base_cycle = set(base_cycle).intersection(read_cycle)
    
    return base_cycle

    
def _read_gpio_list_single_cycle(gpio_numbers: List[int], sample_rate: int) -> List[GPIORead]:
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
    
    GPIO.cleanup()
    return reads

def set_gpio(gpio_number: int, duration_in_sec):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_number, GPIO.OUT)
    GPIO.output(gpio_number, True)
    time.sleep(duration_in_sec)
    GPIO.cleanup()