'''
This module will establish a can and serial connection.
'''

import can
import serial
from .constants import (SERIAL_PORT, SERIAL_BAUDRATE, CAN_BUSTYPE, CAN_CHANNEL, CAN_BITRATE)
from .loggers import (error_logger)

class Dummy_serial():
    def __init__(self,*args):
        pass
    def write(self,*args):
        pass
    def inWaiting():
        pass

try:
    can_bus = can.interface.Bus(bustype=CAN_BUSTYPE, channel=CAN_CHANNEL,bitrate=CAN_BITRATE)
except:
    can_bus = None
    error_logger.error("Can Bus connection Problem")


try:
    ser = serial.Serial(
            port = SERIAL_PORT,
            baudrate = SERIAL_BAUDRATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            xonxoff=True,
            timeout=0,
        )
except:
    ser = Dummy_serial()
    error_logger.error("Serial connection Problem")
