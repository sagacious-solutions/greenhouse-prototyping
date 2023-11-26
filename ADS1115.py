# This module is a library for handling SDC40 co2 sensors on a Raspberry Pi
# https://sensirion.com/media/documents/48C4B7FB/64C134E7/Sensirion_SCD4x_Datasheet.pdf

import smbus2
import time

COMMAND = {
    'stop_periodic_measurement': 0x3f86,
    'start_periodic_measurement': 0x21b1,
    'reinit' : 0x3646
}

DEFAULT_ADS_ADDRESS               = 0x48
WAIT_FOR_READING_RETRY_SECS         = 0.5
WAIT_AFTER_START_PERIODIC_MEASURE   = 0.1
WAIT_FOR_MEASUREMENT_STOP_SECS      = 0.5
WAIT_FOR_REINIT_SECS                = 0.03
DEFAULT_RPI_I2C_BUS                 = 1
MAX_READ_RETRIES                    = 40

HUMIDITY_BYTES_START    = 6
BYTES_IN_READING        = 9
TEMP_BYTES_START        = 3
CO2_BYTES_START         = 0

class ADS1115 :
    def __init__ (self, address=DEFAULT_ADS_ADDRESS, bus_num=DEFAULT_RPI_I2C_BUS):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        # Allow a short pause to allow the bus to initialize.
        self.initialize_sensor()


    def initialize_sensor(self):
        # Stop measurement must be sent before reint can be sent
        self.__send_command(COMMAND['stop_periodic_measurement'])
        time.sleep(WAIT_FOR_MEASUREMENT_STOP_SECS)

    def __send_command(self, cmd) :
        [register_start, hex_command] = self.__split_hex_word(cmd)
        self.bus.write_byte_data(self.address, register_start, hex_command)

    @staticmethod
    def __split_hex_word(word, byte_count=2):
        bytes_value = word.to_bytes(byte_count, byteorder='big')

        return bytes_value
    

