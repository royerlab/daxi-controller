from daxi.control.device.facilitator.config_tools.configuration_generator_mode7 import NIDAQDevicesConfigsGeneratorMode7
from daxi.control.device.facilitator.config_tools.plot_daq_devices_voltage_profiles import plot_daq_voltage_profiles
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_configs_yaml_path_mode7

process_configs = load_process_configs(path=process_configs_yaml_path_mode7)
acquisition_parameters = process_configs['process configs']['acquisition parameters']
daq_terminal_configs = process_configs['device configurations']['nidaq_terminals']
calibration_records = process_configs['device configurations']['calibration_records']
alignment_records = process_configs['device configurations']['alignment_records']
camera_core_configs = process_configs['device configurations']['camera_core_configs']


a = NIDAQDevicesConfigsGeneratorMode7(process_configs=process_configs,
                                      params=acquisition_parameters,
                                      nidaq_terminals=daq_terminal_configs,
                                      calibration_records=calibration_records,
                                      alignment_records=alignment_records)

a.get_configs_for_metronome()
a.get_configs_for_counter()
a.get_configs_do_task_bundle()
a.get_configs_ao_task_bundle()
a.get_configs_scanning_galvo(params=None)
a.get_configs_view_switching_galvo_1()
a.get_configs_view_switching_galvo_2()

plot_daq_voltage_profiles(configs=a)

