from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

if devices_connected is True:
    from daxi.control.device.pool.orca_flash4 import OrcaFlash4

import pytest


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_load_orca_flash4_camera():
    a = OrcaFlash4()
