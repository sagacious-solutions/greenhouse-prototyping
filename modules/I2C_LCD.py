from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface,PinMapping

import busio
import board


class I2C_LCD :
    def __init__ (self, num_cols=20, num_rows=4, pinMap1=True, backlight_on=True):
        self.backlight_on = backlight_on
        self.cols = num_cols
        self.row = num_rows
        self.pin_map = PinMapping.MAPPING1 if pinMap1 else PinMapping.MAPPING2
        self.comm_port = busio.I2C(board.SCL, board.SDA)
        self.i2c_add = 0x27        
        self.interface = self.init_interface()
        self._lcd = LCD(self.interface, num_cols=self.cols, num_rows=4)        
        self._lcd.clear()
        self.print('LCD Initialized!')

    def init_interface(self) :
         return I2CPCF8574Interface(self.comm_port, self.i2c_add, self.pin_map)

    def print(self, str, row=0, col=0):
        self._lcd.set_cursor_pos(row, col)
        self._lcd.print(str)

    def clear(self):
        self._lcd.clear()

    def set_backlight(self):
        self._lcd.set_backlight(self.backlight_on)

    def toggle_backlight(self):
        self.backlight_on = not self.backlight_on
        self.set_backlight()

lcd = I2C_LCD()
import time
time.sleep(2)
lcd.toggle_backlight()
time.sleep(2)
lcd.toggle_backlight()