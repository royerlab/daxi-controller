from daxi.globals_configs_constants_general_tools.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools.constants import virtual_tools_configs_path, \
    device_fcltr_configs_path, params_test_selected_params
import pprint

print("try to load a configuration dictionary:")
p = NIDAQConfigsParser()
p.set_configs_path(virtual_tools_configs_path)
section = 'Physical Devices Section'
keyword = 'AO_task_bundle'
configs = \
    p.get_configs_by_path_section_keyword(section, keyword)

pprint.pprint(configs)

print("try to load a parameter dictionary:")
p = NIDAQConfigsParser()
p.set_configs_path(params_test_selected_params)
section = 'Selected Parameters Section'
keyword = 'mode1_demo'
params = \
    p.get_configs_by_path_section_keyword(section, keyword)

pprint.pprint(params)

print("try to load a configuration dictionary from device fcltr configs path:")
p = NIDAQConfigsParser()
p.set_configs_path(device_fcltr_configs_path)
section = 'Physical Devices Section'
keyword = 'scanning_galvo'
params = \
    p.get_configs_by_path_section_keyword(section, keyword)

pprint.pprint(params)
