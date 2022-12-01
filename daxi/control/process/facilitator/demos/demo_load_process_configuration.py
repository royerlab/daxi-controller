from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
import os
import pprint

path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')

configs = load_process_configs(path=path)

pprint.pprint(configs)
