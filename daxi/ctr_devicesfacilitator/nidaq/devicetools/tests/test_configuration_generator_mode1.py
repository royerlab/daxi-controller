from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.globals_configs_constants_general_tools_needbettername.constants import params_test_selected_params, configs_daq_terminals
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
import pytest


# now use the configuration generator to get the configurations for all 16 devices.
@pytest.fixture
def daq_terminal_configs():
    # now get the terminal configurations
    p2 = NIDAQConfigsParser()
    p2.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'nidaq_terminals'
    output = \
        p2.get_configs_by_path_section_keyword(section, keyword, verbose=False)
    return output


@pytest.fixture
def process_parameters():
    p1 = NIDAQConfigsParser()
    p1.set_configs_path(params_test_selected_params)
    section = 'Selected Parameters Section'
    keyword = 'mode1_demo'
    output = \
        p1.get_configs_by_path_section_keyword(section, keyword, verbose=False)
    return output


@pytest.fixture
def calibration_records():
    # now get the terminal configurations
    p2 = NIDAQConfigsParser()
    p2.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'calibration_records'
    output = \
        p2.get_configs_by_path_section_keyword(section, keyword, verbose=False)
    return output


@pytest.fixture
def alignment_records():
    # now get the terminal configurations
    p2 = NIDAQConfigsParser()
    p2.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'alignment_records'
    output = \
        p2.get_configs_by_path_section_keyword(section, keyword, verbose=False)
    return output


@pytest.fixture
def configs_generator():
    p = NIDAQConfigsParser()
    p.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'nidaq_terminals'
    d = \
        p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

    p.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'calibration_records'
    c = \
        p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

    p.set_configs_path(configs_daq_terminals)
    section = 'Connection Section'
    keyword = 'alignment_records'
    a = \
        p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

    p.set_configs_path(params_test_selected_params)
    section = 'Selected Parameters Section'
    keyword = 'mode1_demo'
    pr = \
        p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

    output = NIDAQDevicesConfigsGeneratorMode1(params=pr,
                                               nidaq_terminals=d,
                                               calibration_records=c,
                                               alignment_records=a,
                                               verbose=False)

    return output


def test_configs_generator_mode1_initiation(daq_terminal_configs, process_parameters, calibration_records,
                                            alignment_records):
    c = NIDAQDevicesConfigsGeneratorMode1(params=process_parameters,
                                          nidaq_terminals=daq_terminal_configs,
                                          calibration_records=calibration_records,
                                          alignment_records=alignment_records,
                                          verbose=False)
    assert isinstance(c, NIDAQDevicesConfigsGeneratorMode1)


def test_configs_generator_mode1_fixture_initiation(configs_generator):
    assert isinstance(configs_generator, NIDAQDevicesConfigsGeneratorMode1)


def test_configs_metronome(configs_generator):
    configs_metronome = \
        configs_generator.get_configs_for_metronome()
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_metronome.values()]) is False


def test_configs_counter(configs_generator):
    configs_counter = \
        configs_generator.get_configs_for_counter()
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_counter.values()]) is False


def test_configs_do_task_bundle(configs_generator):
    configs_do_task = \
        configs_generator.get_configs_do_task_bundle()
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_do_task.values()]) is False


def test_configs_ao_task_bundle(configs_generator):
    configs_ao_task_bundle = \
        configs_generator.get_configs_ao_task_bundle()
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_ao_task_bundle.values()]) is False


def test_configs_scanning_galvo(configs_generator, process_parameters):
    configs_scanning_galvo = \
        configs_generator.get_configs_scanning_galvo(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_scanning_galvo.values()]) is False


def test_configs_view_switching_galvo_1(configs_generator, process_parameters):
    configs_view_switching_galvo_1 = \
        configs_generator.get_configs_view_switching_galvo_1(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_view_switching_galvo_1.values()]) is False


def test_configs_view_switching_galvo_2(configs_generator, process_parameters):
    configs_view_switching_galvo_2 = \
        configs_generator.get_configs_view_switching_galvo_2(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_view_switching_galvo_2.values()]) is False


def test_configs_gamma_galvo_strip_reduction(configs_generator, process_parameters):
    configs_gamma_galvo_strip_reduction = \
        configs_generator.get_configs_gamma_galvo_strip_reduction(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_gamma_galvo_strip_reduction.values()]) is False


def test_configs_beta_galvo_light_sheet_incident_angle(configs_generator, process_parameters):
    configs_beta_galvo_light_sheet_incident_angle = \
        configs_generator.get_configs_beta_galvo_light_sheet_incident_angle(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_beta_galvo_light_sheet_incident_angle.values()]) is False


def test_configs_o1(configs_generator, process_parameters):
    configs_o1 = configs_generator.get_configs_o1(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_o1.values()]) is False


def test_configs_o3(configs_generator, process_parameters):
    configs_o3 = configs_generator.get_configs_o3(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_o3.values()]) is False


def test_configs_405_laser(configs_generator, process_parameters):
    configs_405_laser = configs_generator.get_configs_405_laser(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_405_laser.values()]) is False


def test_configs_488_laser(configs_generator, process_parameters):
    configs_488_laser = configs_generator.get_configs_488_laser(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_488_laser.values()]) is False


def test_configs_561_laser(configs_generator, process_parameters):
    configs_561_laser = configs_generator.get_configs_561_laser(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_561_laser.values()]) is False


def test_configs_639_laser(configs_generator, process_parameters):
    configs_639_laser = configs_generator.get_configs_639_laser(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_639_laser.values()]) is False


def test_configs_bright_field(configs_generator, process_parameters):
    configs_bright_field = configs_generator.get_configs_bright_field(params=process_parameters)
    # make sure all the fields are populated up. (no None)
    assert any([v is None for v in configs_bright_field.values()]) is False
