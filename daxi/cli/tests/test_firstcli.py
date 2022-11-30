import pytest

from daxi.cli.demos.demo_firstcli import demo_firstcli_acquire
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_configs_yaml_path
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_acquire():
    msg = demo_firstcli_acquire(process_configs_path=process_configs_yaml_path)
    assert msg == 'successful'

