from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path


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
    df.load_device_configs(device_fcltr_configs_path)
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
    assert hasattr(df, 'configs_metronome')
    assert hasattr(df, 'configs_counter')
    assert hasattr(df, 'configs_AO_task_bundle')
    assert hasattr(df, 'configs_scanning_galvo')
    assert hasattr(df, 'configs_view_switching_galvo_1')
    assert hasattr(df, 'configs_view_switching_galvo_2')
    assert hasattr(df, 'configs_gamma_galvo_strip_reduction')
    assert hasattr(df, 'configs_beta_galvo_light_sheet_incident_angle')
    assert hasattr(df, 'configs_O1')
    assert hasattr(df, 'configs_O3')
