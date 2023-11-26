# This module is a library for handling SDC40 co2 sensors on a Raspberry Pi
# https://sensirion.com/media/documents/48C4B7FB/64C134E7/Sensirion_SCD4x_Datasheet.pdf

import smbus2
import time

COMMAND = {
    'stop_periodic_measurement': 0x3f86,
    'start_periodic_measurement': 0x21b1,
    'reinit' : 0x3646
}

DEFAULT_SDC40_ADDRESS               = 0x62
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

class SDC40 :
    def __init__ (self, address=DEFAULT_SDC40_ADDRESS, bus_num=DEFAULT_RPI_I2C_BUS):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        # Allow a short pause to allow the bus to initialize.
        self.initialize_sensor()


    def initialize_sensor(self):
        # Stop measurement must be sent before reint can be sent
        self.__send_command(COMMAND['stop_periodic_measurement'])
        time.sleep(WAIT_FOR_MEASUREMENT_STOP_SECS)
        self.__send_command(COMMAND['reinit'])
        time.sleep(WAIT_FOR_REINIT_SECS)

        # Once reinitialized we can start measurement mode on sensor
        self.__send_command(COMMAND['start_periodic_measurement'])
        time.sleep(WAIT_AFTER_START_PERIODIC_MEASURE)

    def get_readings(self):
        retries = 0
        data = None
        
        while (not data and retries < MAX_READ_RETRIES) :
            try :
                data = self.bus.read_i2c_block_data(self.address, 0, BYTES_IN_READING)
            except Exception as e :
                time.sleep(WAIT_FOR_READING_RETRY_SECS)
                retries += 1

                if (retries >= MAX_READ_RETRIES) :
                    print('Max read retries reached. Sensor read failed.')
                    raise e
                
        return self.SENSOR_DATA(data)


    def __send_command(self, cmd) :
        [register_start, hex_command] = self.__split_hex_word(cmd)
        self.bus.write_byte_data(self.address, register_start, hex_command)

    @staticmethod
    def __split_hex_word(word, byte_count=2):
        bytes_value = word.to_bytes(byte_count, byteorder='big')

        return bytes_value
    

    class SENSOR_DATA :
        def __init__ (self, data) :
            self.co2_ppm = self.__bytes_to_word(data, CO2_BYTES_START)

            temp_c_word = self.__bytes_to_word(data, TEMP_BYTES_START)
            self.temp_c = -45 + 175 * (temp_c_word / ((2 ** 16) - 1))
            self.temp_f = self.temp_c * 9 / 5 + 32

            rhWord = self.__bytes_to_word(data, HUMIDITY_BYTES_START)
            self.rh = 100 * (rhWord / ((2 ** 16) - 1))

        def __str__(self):
            return (
                f'Co2: {self.co2_ppm} PPM\n' 
                f'Temperature: {self.temp_c} °C\n'
                f'Relative Humidity: {self.rh} %'
            )

        @staticmethod
        def __bytes_to_word(bytes, offset):
            """ Gets 2 bytes from a list of bytes and returns it as a word"""
            return bytes[offset] * 256 + bytes[offset + 1]