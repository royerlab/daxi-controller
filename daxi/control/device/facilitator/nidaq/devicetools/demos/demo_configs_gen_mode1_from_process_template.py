import os
from matplotlib import pyplot as plt

from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
"""
this is a demo to create configurations using the configuration generator for mode 1 acquisition.
But we will start from a process tempalte that was saved in a yaml file.
"""

# first, load yaml file from template
# look into the demo for template loader.
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
configs = load_process_configs(path=path)

# synthesize the configurations - process_parameter
process_parameters = configs['process configs']['acquisition parameters']

# synthesize the configurations - daq_terminal_configs
daq_terminal_configs = configs['device configurations']['nidaq_terminals']

# synthesize the configurations - calibration_records
calibration_records = configs['device configurations']['calibration_records']

# synthesize the configurations - alignment_records
alignment_records = configs['device configurations']['alignment_records']

# yes it does feel intuitive here to have a data type as the interface to standardize these things above.
# todo need a datatype for these configuraitons. wait until more is done so the format becomes clearer.

# now get the configuration generator object
configs_generator = NIDAQDevicesConfigsGeneratorMode1(params=process_parameters,
                                                      nidaq_terminals=daq_terminal_configs,
                                                      calibration_records=calibration_records,
                                                      alignment_records=alignment_records)

# look into the demo for configuration generator mode 1.
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
