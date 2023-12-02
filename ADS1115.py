#!/usr/bin/env python
import time
import os
import time
import math
from ads1015 import ADS1015

CHANNELS = ["in0/ref", "in1/ref", "in2/ref", "in1/gnd"]

TIME_LENGTH_FOR_DIFS_SECS = 15

print(
    """read-all.py - read all three inputs of the ADC

Press Ctrl+C to exit!
"""
)

ads1015 = ADS1015()
chip_type = ads1015.detect_chip_type()

print("Found: {}".format(chip_type))

ads1015.set_mode("single")
ads1015.set_programmable_gain(4)

# if chip_type == "ADS1015":
ads1015.set_sample_rate(1600)
# else:
# ads1015.set_sample_rate(860)

start_time = time.time()
diffMinutes = []
minutesIn = 0

try:
    chMin = [100,100,100,100]
    chMax = [0,0,0,0]
    chMaxDiff = [0,0,0,0]

    while True:
        now = time.time()
        secsPassed = math.floor(now - start_time)        

        if (math.floor(secsPassed / TIME_LENGTH_FOR_DIFS_SECS) > minutesIn) :
            minutesIn = math.floor(secsPassed / TIME_LENGTH_FOR_DIFS_SECS)
            diffMinutes.append(chMaxDiff)
            chMin = [100,100,100,100]
            chMax = [0,0,0,0]
            chMaxDiff = [0,0,0,0]         

        os.system('clear')
        print(f'Time in { secsPassed }')
        reference = ads1015.get_reference_voltage()
        print("Reference voltage: {:6.3f}v \n".format(reference))

        for index, channel in enumerate(CHANNELS):
            value = ads1015.get_compensated_voltage(
                channel=channel, reference_voltage=reference
            )
            chMin[index] = value if value < chMin[index] else chMin[index]
            chMax[index] = value if value > chMax[index] else chMax[index]

            dif = chMax[index] - chMin[index]
            chMaxDiff[index] = dif if dif > chMaxDiff[index] else chMaxDiff[index]

            print("{}: {:6.3f}v".format(channel, value))
            print("{} Max: {:6.3f}v".format(channel, chMax[index]))
            print("{} Min: {:6.3f}v".format(channel, chMin[index]))
            print("{} Diff: {:6.3f}v".format(channel, dif))
            print("{} Max Diff: {:6.3f}v".format(channel, chMaxDiff[index]))
            print("")

        for i, difMin in enumerate(diffMinutes) : 
            for j, dif in enumerate(difMin) : 
                print(f'ch {j} : {round(dif, 2)}')
            print('')

        print("")
        time.sleep(3)

except KeyboardInterrupt:
    pass