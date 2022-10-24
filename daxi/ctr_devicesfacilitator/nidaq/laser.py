# laser.py
from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr


class LaserBase:
    """ # todo this is unfinished work
    This is the base class for all lasers.
    """
    def __init__(self,
                 laser_line_names: list,
                 daq_terminal_names: list,
                 on_voltage: float,
                 off_voltage: float,
                 ):

        self.laser_line_names = laser_line_names
        self.daq_terminal_names = daq_terminal_names
        self.on_voltage = on_voltage
        self.off_voltage = off_voltage

    def switch_on(self, lines: list):
        """
        This method switches the lasers on during an inspection session

        Parameters
        ----------
        lines: the list of the names of the lasers to inspect here.

        Returns
        -------

        """
        pass

    def switch_off(self, lines: list):
        """
        This method switches the lasers off during an inspection session

        Parameters
        ----------
        lines

        Returns
        -------

        """
        pass
