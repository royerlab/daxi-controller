import os

from daxi.control.device.facilitator.devicefacilitator import DevicesFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path, \
    process_templates
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1

def test_check_AObundle():
    """
    test the wiring checking of AObundle and make sure it is working as expected.
    it should report error when the AObundle wiring is wrong
    it should suggest re-wiring options when wrong wiring is detected
    it should report that the AObundle wiring is correct when everything is correct
    it should generate the inspectable elements that can be used to generate wiring diagram.
    :return:
    """
    # todo - test check AO bundle funciton in devicefacilitator
    pass


def test_load_device_configs():
    df = DevicesFcltr()
    df.load_device_configs_one_cycle(device_fcltr_configs_path)
    assert isinstance(df.devices_and_tools_collection, dict)
    assert 'Virtual Tools Section' in df.devices_and_tools_collection
    assert 'Physical Devices Section' in df.devices_and_tools_collection
    assert 'metronome' in df.devices_and_tools_collection['Virtual Tools Section']
    assert 'counter' in df.devices_and_tools_collection['Virtual Tools Section']
    assert 'AO_task_bundle' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'scanning_galvo' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'view_switching_galvo_1' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'view_switching_galvo_2' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'gamma_galvo_strip_reduction' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'beta_galvo_light_sheet_incident_angle' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'O1' in df.devices_and_tools_collection['Physical Devices Section']
    assert 'O3' in df.devices_and_tools_collection['Physical Devices Section']
    assert hasattr(df, 'description')
    assert hasattr(df, 'subtask_ao_list')
    assert hasattr(df, 'subtask_ao_configs_list')
    assert hasattr(df, 'subtask_do_list')
    assert hasattr(df, 'subtask_do_configs_list')
    assert hasattr(df, 'metronome')
    assert hasattr(df, 'devices_and_tools_collection')
    assert hasattr(df, 'taskbundle_ao')
    assert hasattr(df, 'configs_metronome')
    assert hasattr(df, 'configs_counter')
    assert hasattr(df, 'configs_AO_task_bundle')
    assert hasattr(df, 'configs_DO_task_bundle')
    assert hasattr(df, 'configs_scanning_galvo')
    assert hasattr(df, 'configs_view_switching_galvo_1')
    assert hasattr(df, 'configs_view_switching_galvo_2')
    assert hasattr(df, 'configs_gamma_galvo_strip_reduction')
    assert hasattr(df, 'configs_beta_galvo_light_sheet_incident_angle')
    assert hasattr(df, 'configs_405_laser')
    assert hasattr(df, 'configs_488_laser')
    assert hasattr(df, 'configs_561_laser')
    assert hasattr(df, 'configs_639_laser')
    assert hasattr(df, 'configs_bright_field')
    assert hasattr(df, 'configs_O1')
    assert hasattr(df, 'configs_O3')


def assert_configs_metronome(configs_metronome: dict):
    assert set(configs_metronome.keys()) == \
           set(['name', 'task type', 'counter terminal', 'counting output terminal', 'idle state', 'frequency',
            'sample mode', 'number of samples', 'trigger terminal', 'trigger edge', 'retriggerable', 'purpose'])


def assert_configs_counter(configs_counter: dict):
    assert set(configs_counter.keys()) == \
           set(['name', 'task type', 'counter terminal', 'counting input terminal', 'counting edge', 'initial count',
            'purpose', 'current count', 'verbose'])


def assert_configs_AO_task_bundle(configs_AO_task_bundle: dict):
    assert set(configs_AO_task_bundle.keys()) == \
           set(['name', 'task type', 'trigger terminal', 'trigger edge', 'sample mode'])


def assert_configs_DO_task_bundle(configs_DO_task_bundle: dict):
    assert set(configs_DO_task_bundle.keys()) == \
           set(['name', 'task type', 'trigger terminal', 'trigger edge', 'sample mode'])


def assert_configs_scanning_galvo(configs_scanning_galvo: dict):
    assert set(configs_scanning_galvo.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal',
            'distance (um) to voltage (v) conversion factor (v/um)', 'data', 'data generator', 'data configs'])


def assert_configs_view_switching_galvo_1(configs_view_switching_galvo_1: dict):
    assert set(configs_view_switching_galvo_1.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'data', 'data generator',
            'data configs'])


def assert_configs_view_switching_galvo_2(configs_view_switching_galvo_2: dict):
    assert set(configs_view_switching_galvo_2.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'data', 'data generator',
            'data configs'])


def assert_configs_gamma_galvo_strip_reduction(configs_gamma_galvo_strip_reduction: dict):
    assert set(configs_gamma_galvo_strip_reduction.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal',
            'data', 'data generator', 'data configs'])


def assert_configs_beta_galvo_light_sheet_incident_angle(configs_beta_galvo_light_sheet_incident_angle: dict):
    assert set(configs_beta_galvo_light_sheet_incident_angle.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'data', 'data generator',
            'data configs'])


def assert_configs_405_laser(configs_405_laser: dict):
    assert set(configs_405_laser.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_488_laser(configs_488_laser: dict):
    assert set(configs_488_laser.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_561_laser(configs_561_laser: dict):
    assert set(configs_561_laser.keys()) == \
            set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_639_laser(configs_639_laser: dict):
    assert set(configs_639_laser.keys()) == \
            set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_bright_field(configs_bright_field: dict):
    assert set(configs_bright_field.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_O1(configs_O1: dict):
    assert set(configs_O1.keys()) == \
            set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'data', 'data generator',
             'data configs'])


def assert_configs_O3(configs_O3: dict):
    assert set(configs_O3.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'data', 'data generator',
            'data configs'])


def assert_configs_metronome_all_cycles(configs):
    assert set(configs.keys()) == \
        set(['name', 'task type', 'counter terminal', 'counting output terminal', 'idle state', 'frequency', 'sample mode',
         'number of samples', 'trigger terminal', 'trigger edge', 'retriggerable', 'purpose'])


def assert_configs_counter_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['name', 'task type', 'counter terminal', 'counting input terminal', 'counting edge', 'initial count',
            'purpose', 'current count', 'verbose'])


def assert_configs_AO_task_bundle_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['name', 'task type', 'trigger terminal', 'trigger edge', 'sample mode'])


def assert_configs_DO_task_bundle_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['name', 'task type', 'trigger terminal', 'trigger edge', 'sample mode'])


def assert_configs_scanning_galvo_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal',
                'home voltage offset for view 1',
            'home voltage offset for view 2', 'distance (um) to voltage (v) conversion factor (v/um)',
            'data for view 1', 'data for view 2', 'data generator', 'data configs'])


def assert_configs_view_switching_galvo_1_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal',
                'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 2', 'data for view 1', 'data generator', 'data configs'])


def assert_configs_view_switching_galvo_2_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 2', 'data for view 1', 'data generator', 'data configs'])


def assert_configs_gamma_galvo_strip_reduction_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 1', 'data for view 2', 'data generator', 'data configs'])


def assert_configs_beta_galvo_light_sheet_incident_angle_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 1', 'data for view 2', 'data generator', 'data configs'])


def assert_configs_405_laser_all_cycles(configs):
    assert set(configs.keys()) == \
          set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_488_laser_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_561_laser_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_639_laser_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_bright_field_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'voltage output terminal', 'data', 'data generator', 'data configs'])


def assert_configs_O1_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 1', 'data for view 2', 'data generator', 'data configs'])


def assert_configs_O3_all_cycles(configs):
    assert set(configs.keys()) == \
           set(['device', 'name', 'task type', 'idle state', 'voltage output terminal', 'home voltage offset for view 1',
            'home voltage offset for view 2', 'data for view 1', 'data for view 2', 'data generator', 'data configs'])


def test_load_device_configs_contents():
    df = DevicesFcltr()
    df.load_device_configs_one_cycle(device_fcltr_configs_path)
    assert_configs_metronome(df.configs_metronome)
    assert_configs_counter(df.configs_counter)
    assert_configs_AO_task_bundle(df.configs_AO_task_bundle)
    assert_configs_DO_task_bundle(df.configs_DO_task_bundle)
    assert_configs_scanning_galvo(df.configs_scanning_galvo)
    assert_configs_view_switching_galvo_1(df.configs_view_switching_galvo_1)
    assert_configs_view_switching_galvo_2(df.configs_view_switching_galvo_2)
    assert_configs_gamma_galvo_strip_reduction(\
        df.configs_gamma_galvo_strip_reduction)
    assert_configs_beta_galvo_light_sheet_incident_angle(\
        df.configs_beta_galvo_light_sheet_incident_angle)
    assert_configs_405_laser(df.configs_405_laser)
    assert_configs_488_laser(df.configs_488_laser)
    assert_configs_561_laser(df.configs_561_laser)
    assert_configs_639_laser(df.configs_639_laser)
    assert_configs_bright_field(df.configs_bright_field)
    assert_configs_O1(df.configs_O1)
    assert_configs_O3(df.configs_O3)


def test_receive_device_configs_contents_all_cycles():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    assert_configs_metronome_all_cycles(df.configs_all_cycles['configs_metronome'])
    assert_configs_counter_all_cycles(df.configs_all_cycles['configs_counter'])
    assert_configs_AO_task_bundle_all_cycles(df.configs_all_cycles['configs_AO_task_bundle'])
    assert_configs_DO_task_bundle_all_cycles(df.configs_all_cycles['configs_DO_task_bundle'])
    assert_configs_scanning_galvo_all_cycles(df.configs_all_cycles['configs_scanning_galvo'])
    assert_configs_view_switching_galvo_1_all_cycles(df.configs_all_cycles['configs_view_switching_galvo_1'])
    assert_configs_view_switching_galvo_2_all_cycles(df.configs_all_cycles['configs_view_switching_galvo_2'])
    assert_configs_gamma_galvo_strip_reduction_all_cycles(\
        df.configs_all_cycles['configs_gamma_galvo_strip_reduction'])
    assert_configs_beta_galvo_light_sheet_incident_angle_all_cycles(\
        df.configs_all_cycles['configs_beta_galvo_light_sheet_incident_angle'])
    assert_configs_405_laser_all_cycles(df.configs_all_cycles['configs_405_laser'])
    assert_configs_488_laser_all_cycles(df.configs_all_cycles['configs_488_laser'])
    assert_configs_561_laser_all_cycles(df.configs_all_cycles['configs_561_laser'])
    assert_configs_639_laser_all_cycles(df.configs_all_cycles['configs_639_laser'])
    assert_configs_bright_field_all_cycles(df.configs_all_cycles['configs_bright_field'])
    assert_configs_O1_all_cycles(df.configs_all_cycles['configs_O1'])
    assert_configs_O3_all_cycles(df.configs_all_cycles['configs_O3'])


def test_receive_device_single_cycle_configs_metronome():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_metronome(df.configs_single_cycle_dict[c]['configs_metronome'])


def test_receive_device_single_cycle_configs_counter():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_counter(df.configs_single_cycle_dict[c]['configs_counter'])


def test_receive_device_single_cycle_configs_AO_task_bundle():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_AO_task_bundle(df.configs_single_cycle_dict[c]['configs_AO_task_bundle'])


def test_receive_device_single_cycle_configs_DO_task_bundle():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_DO_task_bundle(df.configs_single_cycle_dict[c]['configs_DO_task_bundle'])


def test_receive_device_single_cycle_configs_scanning_galvo():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_scanning_galvo(df.configs_single_cycle_dict[c]['configs_scanning_galvo'])


def test_receive_device_single_cycle_configs_view_switching_galvo_1():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_view_switching_galvo_1(df.configs_single_cycle_dict[c]['configs_view_switching_galvo_1'])


def test_receive_device_single_cycle_configs_view_switching_galvo_2():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_view_switching_galvo_2(df.configs_single_cycle_dict[c]['configs_view_switching_galvo_2'])


def test_receive_device_single_cycle_configs_gamma_galvo_strip_reduction():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_gamma_galvo_strip_reduction(df.configs_single_cycle_dict[c]['configs_gamma_galvo_strip_reduction'])


def test_receive_device_single_cycle_configs_beta_galvo_light_sheet_incident_angle():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_beta_galvo_light_sheet_incident_angle(df.configs_single_cycle_dict[c]['configs_beta_galvo_light_sheet_incident_angle'])


def test_receive_device_single_cycle_configs_O1():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_O1(df.configs_single_cycle_dict[c]['configs_O1'])


def test_receive_device_single_cycle_configs_O3():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_O3(df.configs_single_cycle_dict[c]['configs_O3'])


def test_receive_device_single_cycle_configs_405_laser():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_405_laser(df.configs_single_cycle_dict[c]['configs_405_laser'])


def test_receive_device_single_cycle_configs_488_laser():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_488_laser(df.configs_single_cycle_dict[c]['configs_488_laser'])


def test_receive_device_single_cycle_configs_561_laser():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_561_laser(df.configs_single_cycle_dict[c]['configs_561_laser'])


def test_receive_device_single_cycle_configs_639_laser():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_639_laser(df.configs_single_cycle_dict[c]['configs_639_laser'])


def test_receive_device_single_cycle_configs_bright_field():
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)
    df = DevicesFcltr()
    df.receive_device_configs_all_cycles(process_configs=process_configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    for c in df.configs_single_cycle_dict.keys():
        assert_configs_bright_field(df.configs_single_cycle_dict[c]['configs_bright_field'])
