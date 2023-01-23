from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.globals_configs_constants_general_tools_needbettername.constants import params_test_selected_params, \
    configs_daq_terminals
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from matplotlib import pyplot as plt

# first, load in the parameters from a template file for mode 1 demonstration.
p1 = NIDAQConfigsParser()
p1.set_configs_path(params_test_selected_params)
section = 'Selected Parameters Section'
keyword = 'mode1_demo'
process_parameters = \
    p1.get_configs_by_path_section_keyword(section, keyword, verbose=False)

# now get the terminal configurations
p2 = NIDAQConfigsParser()
p2.set_configs_path(configs_daq_terminals)
section = 'Connection Section'
keyword = 'nidaq_terminals'
daq_terminal_configs = \
    p2.get_configs_by_path_section_keyword(section, keyword, verbose=False)

p = NIDAQConfigsParser()
p.set_configs_path(configs_daq_terminals)
section = 'Connection Section'
keyword = 'calibration_records'
calibration_records = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

p.set_configs_path(configs_daq_terminals)
section = 'Connection Section'
keyword = 'alignment_records'
alignment_records = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

# now get the configuration generator
configs_generator = NIDAQDevicesConfigsGeneratorMode1(params=process_parameters,
                                                      nidaq_terminals=daq_terminal_configs,
                                                      calibration_records=calibration_records,
                                                      alignment_records=alignment_records)

# now use the configuration generator to get the configurations for all 16 devices.
configs_metronome = \
    configs_generator.get_configs_for_metronome()

configs_counter = \
    configs_generator.get_configs_for_counter()

configs_do_task = \
    configs_generator.get_configs_do_task_bundle()

configs_ao_task_bundle = \
    configs_generator.get_configs_ao_task_bundle()

configs_scanning_galvo = \
    configs_generator.get_configs_scanning_galvo(params=process_parameters)
plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.plot(configs_scanning_galvo['data for view 1'], 'r-o')
plt.title('voltage profile for scanning galvo for view 1')
plt.subplot(132)
plt.plot(configs_scanning_galvo['data for view 2'], 'b-o')
plt.title('voltage profile for scanning galvo for view 2')
plt.subplot(133)
plt.plot(configs_scanning_galvo['data for view 1'], 'r-o')
plt.plot(configs_scanning_galvo['data for view 2'], 'b-o')
plt.title('voltage profile for scanning galvo for view 1 and 2')
plt.show()

configs_view_switching_galvo_1 = \
    configs_generator.get_configs_view_switching_galvo_1(params=process_parameters)
# plot switching galvo voltage profile
plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.plot(configs_view_switching_galvo_1['data for view 1'], 'r-o')
plt.title('voltage profile for view switching galvo 1 for view 1')
plt.subplot(132)
plt.plot(configs_view_switching_galvo_1['data for view 2'], 'b-o')
plt.title('voltage profile for view switching galvo 1 for view 2')
plt.subplot(133)
plt.plot(configs_view_switching_galvo_1['data for view 1'], 'r-o')
plt.plot(configs_view_switching_galvo_1['data for view 2'], 'b-o')
plt.title('voltage profile for view switching galvo 1 for view 1 and 2')
plt.show()

configs_view_switching_galvo_2 = \
    configs_generator.get_configs_view_switching_galvo_2(params=process_parameters)
plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.plot(configs_view_switching_galvo_2['data for view 1'], 'r-o')
plt.title('voltage profile for view switching galvo 2 for view 1')
plt.subplot(132)
plt.plot(configs_view_switching_galvo_2['data for view 2'], 'b-o')
plt.title('voltage profile for view switching galvo 2 for view 2')
plt.subplot(133)
plt.plot(configs_view_switching_galvo_2['data for view 1'], 'r-o')
plt.plot(configs_view_switching_galvo_2['data for view 2'], 'b-o')
plt.title('voltage profile for view switching galvo 2 for view 1 and 2')

plt.show()

configs_gamma_galvo_strip_reduction = \
    configs_generator.get_configs_gamma_galvo_strip_reduction(params=process_parameters)
plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.plot(configs_gamma_galvo_strip_reduction['data for view 1'], 'r-o')
plt.title('voltage profile for configs_gamma_galvo_strip_reduction for view 1')
plt.subplot(132)
plt.plot(configs_gamma_galvo_strip_reduction['data for view 2'], 'b-o')
plt.title('voltage profile for configs_gamma_galvo_strip_reduction for view 2')
plt.subplot(133)
plt.plot(configs_gamma_galvo_strip_reduction['data for view 1'], 'r-o')
plt.plot(configs_gamma_galvo_strip_reduction['data for view 2'], 'b-o')
plt.title('voltage profile for configs_gamma_galvo_strip_reduction for view 1 and 2')

plt.show()

configs_beta_galvo_light_sheet_incident_angle = \
    configs_generator.get_configs_beta_galvo_light_sheet_incident_angle(process_parameters)

configs_o1 = configs_generator.get_configs_o1(process_parameters)

configs_o3 = configs_generator.get_configs_o3(process_parameters)

configs_405_laser = configs_generator.get_configs_405_laser(process_parameters)

configs_488_laser = configs_generator.get_configs_488_laser(process_parameters)

configs_561_laser = configs_generator.get_configs_561_laser(process_parameters)

configs_639_laser = configs_generator.get_configs_639_laser(process_parameters)

configs_bright_field = configs_generator.get_configs_bright_field(process_parameters)


def print_configs(name: str):
    print('')
    print('')
    print('------------------------------------ Devices Configs Section: ' + name + '')
    print(name + ':')
    eval('pprint.pprint(configs_generator.' + name + ')')


print_configs('configs_metronome')
print_configs('configs_counter')
print_configs('configs_do_task_bundle')
print_configs('configs_ao_task_bundle')
print_configs('configs_scanning_galvo')
print_configs('configs_view_switching_galvo_1')
print_configs('configs_view_switching_galvo_2')
print_configs('configs_gamma_galvo_strip_reduction')
print_configs('configs_beta_galvo_light_sheet_incident_angle')
print_configs('configs_o1')
print_configs('configs_o3')
print_configs('configs_405_laser')
print_configs('configs_488_laser')
print_configs('configs_561_laser')
print_configs('configs_639_laser')
print_configs('configs_bright_field')
