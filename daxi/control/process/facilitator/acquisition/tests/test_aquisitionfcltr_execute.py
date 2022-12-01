import pytest

from daxi.control.process.facilitator.acquisition.demos.demo_acquisitionfcltr_execute import demo_acquisition_fcltr_execute
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected, long_test


@pytest.mark.skipif(long_test is False, reason="This test requires daq cards to be connected.")
def test_acquisitionfcltr_execute():
    msg = demo_acquisition_fcltr_execute()
    assert msg == 'successful'
