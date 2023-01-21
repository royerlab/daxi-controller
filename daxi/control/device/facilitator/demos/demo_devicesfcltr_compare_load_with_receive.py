import os
import pprint

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path, \
    process_templates

# 0.  checkout a devices facilitator
df = DevicesFcltr()

# 1. get configurations
df.load_device_configs_one_cycle(device_configs_file=device_fcltr_configs_path)


# 0.  checkout a devices facilitator
df2 = DevicesFcltr()

# when devices facilitator is a receiver, it receives the data configurations
# from it's command and it will populate up the configuraiton

# we load the configs first that is passed over by the client through the command (think about the cli client or a
# focused process fcltr as the client).
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
configs = load_process_configs(path=path)

# then this configs is passed to the receiver to populate its configurations for all the devices.
df2.receive_device_configs_all_cycles(process_configs=configs,
                                      daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)

print(df2.configs_all_cycles['configs_405_laser'].keys())

pprint.pprint(df.configs_405_laser)
# pprint.pprint(df2.configs_all_cycles['configs_beta_galvo_light_sheet_incident_angle'])
