from daxi.control.process.facilitator.processes_facilitator import save_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates, \
    params_test_selected_params, configs_daq_terminals
from daxi.control.process.facilitator.system.tools.acquisition_parameter_suggestion import AcqParamMode1
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
import os
import pprint

m = AcqParamMode1(dx=0.4,
                  length=100,
                  t_exposure=490,
                  t_readout=10,
                  t_stage_retraction=23,
                  scanning_galvo_range_limit=0.8,
                  number_of_colors_per_slice=1,
                  colors=['488', '561'],
                  number_of_scans_per_timepoint=1,
                  slice_color_list=None,
                  positions={'position name 1': {'x': 1, 'y': 10}, 'position name 2': {'x': 23, 'y': 12}},
                  views=['1', '2'],
                  positions_views_list=None,
                  number_of_time_points=2,
                  )
m.adapt()
m.get_parameter_combination(magnification_factor=5)
acquisition_parameters = m.selected_parameters

path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')

# create a configuration dictionary.
configs_dict = {}

# 1. get the acquisition parameter dictionary

# 2. load in all the devices' configuration dictionary
# first, load in the parameters from a template file for mode 1 demonstration.
p = NIDAQConfigsParser()
p.set_configs_path(params_test_selected_params)
section = 'Selected Parameters Section'
keyword = 'mode1_demo'
process_parameters = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

# now get the terminal configurations
p.set_configs_path(configs_daq_terminals)
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

keyword = 'stage_core_configs'
stage_core_configs = \
    p.get_configs_by_path_section_keyword(section, keyword, verbose=False)

# composite the configs_dict dictionary
configs_dict={
        "process type": "acquisition, mode 1",
        "process configs":
        {
            "process type": "acquisition, mode 1",
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
