'''
This module will collect can data
'''

import can 
can_bus = can.interface.Bus(bustype='socketcan', channel='can0',bitrate=250000)

def collect_can_data():
    with open('can_data.txt', 'a') as can_file:
        count=0
        for msg in can_bus:
            count+=1
            can_file.write(str(msg)+str('\n'))

