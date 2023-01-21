import platform
import os
daxi_path = 'C:/Users/PiscesScope/xiyu_workbench/daxi-controller/daxi'

if platform.system() == 'Darwin':
    m = os.getcwd()
    daxi_path = os.path.join(os.path.join(m.split('daxi-controller')[0], 'daxi-controller'), 'daxi')

configs_templates_path = daxi_path + "/globals_configs_constants_general_tools_needbettername/" \
                             "configuration_templates"
process_templates: str = configs_templates_path + '/process_templates'

virtual_tools_configs_path = configs_templates_path+"/devices_configs"

device_fcltr_configs_path = configs_templates_path+"/devices_fcltr_configs_panel"

params_test_selected_params = configs_templates_path+"/params_test_selected_params_for_mode1to6"

configs_daq_terminals = configs_templates_path+"/wiring_alignment_and_calibration"

configs_core_daq_devices = configs_templates_path+"/devices_configs_core"

process_configs_yaml_path = process_templates + '/template_acquisition_mode1-dev.yaml'


