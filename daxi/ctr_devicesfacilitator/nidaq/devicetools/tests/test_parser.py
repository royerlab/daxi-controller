from daxi.globals_configs_constants_general_tools.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools.constants import virtual_tools_configs_path, device_fcltr_configs_path


def create_nidaq_parser():
    # make sure all attributes and method exist.
    nidaq_p = NIDAQConfigsParser()
    return nidaq_p


def test_get_counter_configs():
    configs_path = virtual_tools_configs_path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    p.get_counter_configs()
    assert hasattr(p, 'counter_configs')
    assert isinstance(p.counter_configs, dict)


def test_get_oscilloscope1_configs():
    configs_path = virtual_tools_configs_path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    p.get_oscilloscope1_configs()
    assert hasattr(p, 'oscilloscope1_configs')
    assert isinstance(p.oscilloscope1_configs, dict)


def test_get_oscilloscope2_configs():
    configs_path = virtual_tools_configs_path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    p.get_oscilloscope2_configs()
    assert hasattr(p, 'oscilloscope2_configs')
    assert isinstance(p.oscilloscope2_configs, dict)


def test_get_oscilloscope3_configs():
    configs_path = virtual_tools_configs_path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    p.get_oscilloscope3_configs()
    assert hasattr(p, 'oscilloscope3_configs')
    assert isinstance(p.oscilloscope3_configs, dict)


def test_get_configs_by_path_section_keyword():
    configs_path = virtual_tools_configs_path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    section = 'Physical Devices Section'
    keyword = 'oscilloscope_channel1'
    p.get_configs_by_path_section_keyword(section, keyword)
    assert hasattr(p, 'oscilloscope1_configs')
    assert isinstance(p.oscilloscope1_configs, dict)


def template_test_get_scanning_galvo(path, section, keyword):
    configs_path = path
    p = create_nidaq_parser()
    p.set_configs_path(configs_path)
    p.get_configs_by_path_section_keyword(section, keyword)
    assert hasattr(p, 'scanning_galvo_configs')
    assert isinstance(p.scanning_galvo_configs, dict)
    assert 'device' in p.scanning_galvo_configs.keys()
    assert 'name' in p.scanning_galvo_configs.keys()
    assert 'idle state' in p.scanning_galvo_configs.keys()
    assert 'voltage output terminal' in p.scanning_galvo_configs.keys()
    assert 'distance (um) to voltage (v) conversion factor (v/um)' in p.scanning_galvo_configs.keys()
    assert 'data' in p.scanning_galvo_configs.keys()
    assert 'data generator' in p.scanning_galvo_configs.keys()
    assert 'data configs' in p.scanning_galvo_configs.keys()
    assert 'type' in p.scanning_galvo_configs['data configs'].keys()
    assert 'linear ramp start' in p.scanning_galvo_configs['data configs'].keys()
    assert 'linear ramp stop' in p.scanning_galvo_configs['data configs'].keys()
    assert 'linear ramp sample number' in p.scanning_galvo_configs['data configs'].keys()


def test_get_scanning_galvo_virtual_tools_configs_path():
    template_test_get_scanning_galvo(path=virtual_tools_configs_path,
                                     section='Physical Devices Section',
                                     keyword='scanning_galvo_soft_retraction')


def test_get_scanning_galvo_device_fcltr_configs_path():
    template_test_get_scanning_galvo(path=device_fcltr_configs_path,
                                     section='Physical Devices Section',
                                     keyword='scanning_galvo')
