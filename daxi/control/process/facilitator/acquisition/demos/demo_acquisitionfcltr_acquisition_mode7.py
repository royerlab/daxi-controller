import os
from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.process.facilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

# Define path to the configuration file
path = os.path.join(process_templates, 'template_acquisition_mode7-dev-small_stack.yaml')
process_configs = load_process_configs(path=path)

# checkout a device facilitator
df = DevicesFcltr(devices_connected=devices_connected)

# checkout an acquisition facilitator
af = AcquisitionFcltr()

# configure the acquisition facilitator
af.devices_fcltr = df
af.configs = process_configs

# start mode7 acquisition
af.acquisition_mode7()
