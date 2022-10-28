import os

from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.ctr_processesfacilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path, \
    process_templates

# 0.  checkout a devices facilitator
df = DevicesFcltr()

# when devices facilitator is a receiver, it receives the data configurations
# from it's command and it will populate up the configuraiton

# we load the configs first that is passed over by the client through the command (think about the cli client or a
# focused process fcltr as the client).
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
configs = load_process_configs(path=path)

# then this configs is passed to the receiver to populate its configurations for all the devices.
df.receive_device_configs(device_configs=configs)
