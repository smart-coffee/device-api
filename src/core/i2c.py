import time

from smbus2 import SMBus

from config.logger import logging, get_logger_name
from utils.basic import validate_percent_value


logger = logging.getLogger(get_logger_name(__name__))


def set_dac_value(self, bus_number: int, address: int, percent_value: int, i2c_delay, sensor_name: str='Unknown'):
    if address is None:
        logger.warning('Sensor {} i2c bus address is not configured.'.format(sensor_name))
        return

    validate_percent_value(value=percent_value)

    logger.debug('Instanciating SMBus: {}'.format(bus_number))
    bus = SMBus(bus_number)
    logger.debug('done.')
    reg_write_dac = 0x40
        
    # Create our 12-bit number representing relative voltage
    max_voltage = 0xFFF
    rate = percent_value / 100
    voltage = int(max_voltage * rate) & 0xFFF
    logger.debug('Voltage: {0} ({1} %)'.format(voltage, percent_value))

    # Shift everything left by 4 bits and separate bytes
    msg = (voltage & 0xff0) >> 4
    msg = [msg, (msg & 0xf) << 4]

    # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
    logger.debug('Writing block data to i2c address ', hex(address), ': [0] => ', hex(msg[0]), ', [1] => ', hex(msg[1]))
    bus.write_i2c_block_data(address, reg_write_dac, msg)
    time.sleep(i2c_delay)
    logger.debug('done.')
