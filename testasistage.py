# main.py
from asistage.ms2k import MS2000
import numpy as np


def main():
    # scan system for com ports
    print(f"COM Ports: {MS2000.scan_ports()}")

    # connect to the MS2000
    ms2k = MS2000("COM6", 9600)
    ms2k.connect_to_serial()
    if not ms2k.is_open():
        print("Exiting the program...")
        return

    # move the stage
    for n in np.arange(10):
        ms2k.moverel(2000, 0)
        ms2k.wait_for_device()

    ms2k.moverel(10000, 0)
    ms2k.wait_for_device()
    ms2k.moverel(1000, 0)
    ms2k.wait_for_device()
    ms2k.moverel(0, 0)
    ms2k.wait_for_device()

    # close the serial port
    ms2k.disconnect_from_serial()


if __name__ == "__main__":
    main()