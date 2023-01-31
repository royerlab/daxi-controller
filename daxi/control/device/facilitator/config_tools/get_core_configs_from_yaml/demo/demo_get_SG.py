from daxi.control.device.facilitator.config_tools.get_core_configs_from_yaml.get_core_configs_SG import \
    _get_core_sg_configs
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
import os


def assert_sg_configs(sg_configs):
    assert 'device' in sg_configs.keys()
    assert 'name' in sg_configs.keys()
    assert 'task type' in sg_configs.keys()
    assert 'idle state' in sg_configs.keys()
    assert 'voltage output terminal' in sg_configs.keys()
    assert 'home voltage offset for view 1' in sg_configs.keys()
    assert 'home voltage offset for view 2' in sg_configs.keys()
    assert 'distance (um) to voltage (v) conversion factor (v/um)' in sg_configs.keys()
    assert 'data for view 1' in sg_configs.keys()
    assert 'data for view 2' in sg_configs.keys()
    assert 'data generator' in sg_configs.keys()
    assert 'data configs' in sg_configs.keys()
    assert sg_configs['device'] == 'scanning_galvo'


def demo_get_sg_configs():
    # load a yaml file
    path = os.path.join(process_templates, 'template_acquisition_mode7-dev.yaml')
    process_configs = load_process_configs(path=path)

    # get the SG_configs based on the process_configs
    sg_configs = _get_core_sg_configs(process_configs=process_configs)
    assert_sg_configs(sg_configs)
    assert sg_configs['data generator'] == 'constant'

    # do another test with mode1
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    sg_configs = _get_core_sg_configs(process_configs=process_configs)
    assert_sg_configs(sg_configs)
    assert sg_configs['data generator'] == 'linear_ramp_soft_retraction'
    return 'success'


if __name__ == '__main__':
    demo_get_sg_configs()
