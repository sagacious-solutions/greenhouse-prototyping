import RPi.GPIO as GPIO
import time

class CycleTimer:
    def __init__ (self, offTimeS, onTimeS, pinNum, useBCM=True, onIsHigh=True) :
        self.offTimeS = offTimeS
        self.onTimeS = onTimeS
        self.pinNum = pinNum
        self.on = GPIO.HIGH if onIsHigh else GPIO.LOW
        self.off = GPIO.LOW if onIsHigh else GPIO.HIGH

        if (useBCM) :
            GPIO.setmode(GPIO.BCM)
        else :
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(pinNum, GPIO.OUT, initial=self.off)


    def cycleLoop(self):
        while True :
            print(f'Cycle timer on.')
            GPIO.output(self.pinNum, self.on)
            time.sleep(self.onTimeS)
            print(f'Cycle timer off.')
            GPIO.output(self.pinNum, self.off)
            time.sleep(self.offTimeS)