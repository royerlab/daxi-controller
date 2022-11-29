# test_laser.py

from daxi.control.device.facilitator.devicefacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.laser import LaserBase
from daxi.control.device.facilitator.nidaq.tests.assert_laser import assert_laser


def test_laser_base_class(lines=['405', '488', '561', '637'],
                          terminals=['placeholder', 'placeholder', 'placeholder', 'placeholder']):
    # get a device manager
    device_mgr = DevicesFcltr()
    laser_base = LaserBase(laser_line_names=lines,
                           daq_terminal_names=terminals,
                           on_voltage=5.0,
                           off_voltage=0.0)
    assert_laser(verbose=True, laser=laser_base)
