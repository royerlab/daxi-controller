import copy
from time import sleep

from daxi.control.device.facilitator.serial.daxi_ms2k_stage import DaxiMs2kStage, pos_str2num, pos_2asi
import numpy as np


class DaxiMS2kStageSimulated(DaxiMs2kStage):

    def _is_device_busy(self) -> bool:
        return "B"

    def _wait_for_device(self, report: bool = False) -> None:
        pass

    def config_speed(self, scan_configs=None, speed:float=0.00528):
        """
            Parameters
            ----------
            scan_configs: dict, dictionary of scanning configurations.
            speed: float, unit: um/ms (equivalent to mm/s)

            Returns
            -------

        """
        if scan_configs is None:
            msg_speed = f"SPEED X={speed}\r"
            print('setting the raster scanning speed to be ' + str(speed) + ' from default')
        else:
            msg_speed = f"SPEED X={scan_configs['scan speed']}\r"
        print('setting the raster scanning speed to be ' + str(scan_configs['scan speed']) + ' from scan_configs')

    def config_raster_scan(self,
                           scan_configs: dict,
                           start: float = None,
                           end: float = None,
                           encoder_divide: int = None):
        if scan_configs is None:
            msg_raster_scan = f"SCANR X={start} Y={end} Z={encoder_divide}\r"
        else:
            start = scan_configs['start position']
            end = scan_configs['end position']
            encoder_divide = scan_configs['encoder divide']
            msg_raster_scan = f"SCANR X={start} Y={end} Z={encoder_divide}\r"
        print('message for the stage would be:' + msg_raster_scan)

    def get_current_position(self, unit: str = 'mm'):
        """
        read the current position of the stage, return a dictionary in units of mm.
        unit, str, options: "asi", "mm"
        """

        pos = {'unit': unit}  # store the axis positions
        for axis_tag in ['X', 'Y']:
            pos_str = str(int(np.random.randn(1)*10000)+1)
            pos[axis_tag] = pos_str2num(pos_str, unit)
            sleep(0.01)
            self._wait_for_device()

        pos = self._store_position_info(pos=pos)
        return pos

    def connect(self):
        pass

    def move_to(self, destination_name:str):
        """

        Parameters
        ----------
        destination_name: str
            name of the stored destination position.

        Returns
        -------

        """

        # retrieve the position under the destination_name
        pos = self.stored_positions[destination_name]
        # convert the position to asi unit
        pos_asi = pos_2asi(pos)
        print('move to position at' + str(pos_asi))

    def raster_scan_go(self):
        print('raster scan go')
