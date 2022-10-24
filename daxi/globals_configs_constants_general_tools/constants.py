import platform
daxi_path = 'C:/Users/PiscesScope/xiyu_workbench/daxi-controller/daxi'

if platform.system() == 'Darwin':
    daxi_path='/Users/xiyuyi/Desktop/Research/P-daxi-codes/daxi-controller/daxi'

virtual_tools_configs_path = daxi_path + "/globals_configs_constants_general_tools/" \
                             "configuration_templates/devices_configs"

device_fcltr_configs_path = daxi_path + "/globals_configs_constants_general_tools/" \
                             "configuration_templates/devices_fcltr_configs_panel"

params_test_selected_params = daxi_path + "/globals_configs_constants_general_tools/" \
                             "configuration_templates/params_test_selected_params_for_mode1to6"

configs_daq_terminals = daxi_path + "/globals_configs_constants_general_tools/" \
                             "configuration_templates/wiring_alignment_and_calibration"

configs_core_daq_devices = daxi_path + "/globals_configs_constants_general_tools/" \
                             "configuration_templates/devices_configs_core"