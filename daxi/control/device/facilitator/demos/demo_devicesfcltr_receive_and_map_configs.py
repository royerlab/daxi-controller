"""
this demo should recieve a process configuration file (from the yaml file),
generate the configurations for all cycles ()
map it into single_cycle configs dict

then the devices facilitator is going to have a method called 'map single cylce'
or something that can be called by a focused group process fcltr, and it will
map the configurations to the single clc configurations attributes ready to execute.

after this, should go ahead and implement the focused process fcltr to do that for mode 1.

also need a "refresh-data" type of method in the device facilitator
"""
import os

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates

# 0.  checkout a devices facilitator
df = DevicesFcltr()

# define the template acquisition file and load it in. it is a process configuration.
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
configs = load_process_configs(path=path)

# 1. receive the configurations
df.receive_device_configs_all_cycles(process_configs=configs,
                                     daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)

# 2. map the configurations
print('printing dictionary keys for df.configs_single_cycle_dict')
for k in df.configs_single_cycle_dict.keys():
    print(k)
print('length = '+str(len(df.configs_single_cycle_dict.keys())))

# check one dict:
print('')
print('check one configuration:')
for k in df.configs_single_cycle_dict['view1 color488']:
    print(k)
print('length = '+str(len(df.configs_single_cycle_dict['view1 color488'].keys())))

