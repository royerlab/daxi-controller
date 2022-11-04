import pytest

from daxi.ctr_processesfacilitator.acquisition.demos.demo_acquisitionfcltr_execute import demo_acquisition_fcltr_execute
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_acquisitionfcltr_execute():
    msg = demo_acquisition_fcltr_execute()
    assert msg == 'successful'
