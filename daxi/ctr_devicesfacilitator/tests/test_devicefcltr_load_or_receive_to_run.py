import pytest

from daxi.ctr_devicesfacilitator.demos.demo_devicesfcltr_load_and_run import demo_devicefcltr_load_and_run
from daxi.ctr_devicesfacilitator.demos.demo_devicesfcltr_receive_map_checkout_and_run import \
    demo_devicefcltr_receive_map_checkout_and_run
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_devicefcltr_load_and_run():
    msg = demo_devicefcltr_load_and_run(verbose=False, interactive=False)
    assert msg == 'success'


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_devicefcltr_receive_map_checkout_and_run():
    msg = demo_devicefcltr_receive_map_checkout_and_run(verbose=False, interactive=False)
    assert msg == 'success'
