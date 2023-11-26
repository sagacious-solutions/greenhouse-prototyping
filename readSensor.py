import sdc40
import time

sensor = sdc40.SDC40()

while (True):
    data = sensor.get_readings()
    print(str(data))
    time.sleep(5)
