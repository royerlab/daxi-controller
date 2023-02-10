from daxi.control.device.facilitator.config_tools.configuration_generator_mode7 import NIDAQDevicesConfigsGeneratorMode7
from daxi.control.device.facilitator.config_tools.plot_daq_devices_voltage_profiles import plot_daq_voltage_profiles, \
    plot_daq_voltage_profiles_single_cycle_dict
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_configs_yaml_path_mode7_short

process_configs = load_process_configs(path=process_configs_yaml_path_mode7_short)
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
a.get_configs_gamma_galvo_strip_reduction(params=None)
a.get_configs_beta_galvo_light_sheet_incident_angle(params=None)
a.get_configs_o3(params=None)
a.get_configs_405_laser(params=None)
a.get_configs_488_laser(params=None)
a.get_configs_561_laser(params=None)
a.get_configs_639_laser(params=None)
a.get_configs_bright_field(params=None)
a.get_configs_o1(params=None)

plot_daq_voltage_profiles(configs=a,
                          data_points_to_show=10000)

# now get single cycle dictionary
configs_daq_single_cycle_dict = \
    a.get_configs_single_cycle_dict(params=acquisition_parameters)

# and perhaps plot all the sequences for each cycle type
plot_daq_voltage_profiles_single_cycle_dict(configs_dict=configs_daq_single_cycle_dict['view1 colorbright_field'],
                                            data_points_to_show=30000,
                                            dict_key='view1 colorbright_field',
                                            process_configs=a.process_configs)


