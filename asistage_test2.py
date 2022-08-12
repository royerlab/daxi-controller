# import tools
from asistage.ms2k import MS2000
from time import sleep
import pymmcore
import numpy as np


# test how to generate the trigger signal by moving from one position to another.


# scan system for com ports
print(f"COM Ports: {MS2000.scan_ports()}")


# connect to the MS2000 with a given baud rate
print("connecting to MS2000")
ms2k = MS2000("COM6", 9600)
ms2k.connect_to_serial()


if not ms2k.is_open():
    print("ms2k is not open.")


sleep(2)
# ms2k.scan(x=10000, y=10000)


# sleep(1)
# ms2k.moverel(-10000, 10000)
# sleep(1)
# ms2k.moverel(0, 10000)
# sleep(1)
# ms2k.moverel(0, -10000)

# scan from absolute position 10 to 1
ms2k.send_command("SPEED X=0.528\r")
print(ms2k.read_response())
busy = True
while busy:
    busy = ms2k.is_device_busy()



ms2k.send_command("SCANR X=0.0 Y=10.0 Z=24\r")
print(ms2k.read_response())

ms2k.send_command("SCAN\r")
print(ms2k.read_response())

# ms2k.get_position_um(axis="X")
# print(x)
# print(ms2k.read_response())

# # get X, Y axis position in unit of mm.
# def get_positions():
# pos = {}  # dictionary to store the axis positions
# for axis_tag in ['X', 'Y']:
#     ms2k.send_command(f"WHERE "+axis_tag+"\r")  # send a serial command to get the X axis position
#     resp = ms2k.read_response()  # receive the responses with position information expressed in a string
#     pos_str = resp.split(" ")[1]  # parse the string to obtain the position substring in ASI unit (10 um).
#     pos[axis_tag] = float(pos_str)/10.0  # convert the positiong (as a string) to float number, in unit of mm.
#     # wait for the device
#     busy = True
#     while busy:
#         busy = ms2k.is_device_busy()

# P = get_positions()

# self.send_command(f"WHERE {axis}\r")
# response = self.read_response()
# return float(response.split(" ")[1]) / 10.0

# set scanning speed.
# set scanning axis
# start scanning start and end point
# disconnect from the serial port

ms2k.disconnect_from_serial()

