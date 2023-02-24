from daxi.control.process.facilitator.processes_facilitator import save_process_configs
from daxi.control.process.facilitator.system.demos.demo_acquisition_parameter_suggestion_mode7 import \
    demo_acquisition_params_mode7
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates, \
    params_test_selected_params, configs_daq_terminals_calibrations
from daxi.control.process.facilitator.system.tools.acquisition_parameter_suggestion import AcqParamMode8
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
import os

import pprint

# Prints the nicely formatted dictionary
m = AcqParamMode8(dx=0.4,  # um
                  length=500,
                  t_exposure=100,
                  t_readout=500,
                  t_stage_retraction=23,  # retraction time for the stage after a stack acquisition is done.
                  number_of_colors_per_slice=1,
                  colors=['488'],  # a sublist of the list: ['bright_field', '405', '488', '561', '639']
                  slice_color_list=None,
                  views=['1', '2'],
                  positions_views_list=None,
                  positions={'p1': {'x': 1, 'y': 10}, 'p2': {'x': 23, 'y': 12}},
                  number_of_time_points=2,
                  light_sheet_scanning_range=1,  # unit: mm
                  )

m.adapt()

m.find_parameter_combinations_o1scan()

m.display_parameter_options()

m.get_parameter_combination_o1scan(magnification_factor=5)

acquisition_parameters = m.selected_parameters

path = os.path.join(process_templates, 'template_acquisition_mode8-dev-thick_stack_488only.yaml')

# create a configuration dictionary.
configs_dict = {}

# 1. get the acquisition parameter dictionary
process_parameters = m.selected_parameters

# load in all the devices' configuration dictionary
p = NIDAQConfigsParser()
# now get the terminal configurations
p.set_configs_path(configs_daq_terminals_calibrations)
section = 'Connection Section'
keyword = 'nidaq_terminals'
daq_terminal_configs = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

keyword = 'calibration_records'
calibration_records = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

keyword = 'alignment_records'
alignment_records = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

keyword = 'camera_core_configs'
camera_core_configs = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)
camera_core_configs['master pulse interval'] = (process_parameters['exposure time (ms)'] + process_parameters['camera read out time (ms)'])/1000
camera_core_configs['master pulse trigger'] = 'SOFTWARE'
camera_core_configs['master pulse mode'] = 'CONTINUOUS'
camera_core_configs['output trigger polarity'] = 'NEGATIVE'

keyword = 'stage_core_configs'
stage_core_configs = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

# composite the configs_dict dictionary
configs_dict = {
        "process type": "acquisition, mode 8",
        "process configs":
        {
            "process type": "acquisition, mode 8",
            "acquisition parameters": acquisition_parameters,
        },
        "device configurations":
        {
            'nidaq_terminals': daq_terminal_configs,
            'calibration_records': calibration_records,
            'alignment_records': alignment_records,
            'camera_core_configs': camera_core_configs,
            'stage_core_configs': stage_core_configs,
        },
}
# save the configurations dictionary as a yaml file.
save_process_configs(path=path, configs=configs_dict)
pprint.pprint(configs_dict)
