
from modules.ProcessControl import ProcessControl
from modules.CycleTimer import CycleTimer
import time
PUMP_RELAY_PIN1 = 17
PUMP_RELAY_PIN2 = 27

if __name__ == '__main__' :
    print('Starting simplePumpController')
    procControl = ProcessControl()
    ct1 = CycleTimer(1, 1, PUMP_RELAY_PIN1)
    time.sleep(0.05)
    ct2 = CycleTimer(1, 1, PUMP_RELAY_PIN2)

    procControl.startProcess('pump', ct1.cycleLoop)
    procControl.startProcess('pump', ct2.cycleLoop)


