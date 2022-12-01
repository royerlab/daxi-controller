import os

from daxi.control.device.facilitator.devicefacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates

af = AcquisitionFcltr()  # checkout an acquisition facilitator.

# this demo shows how to use the AcquisitionFcltr standalone.
# checkout a AcquisitionFcltr\

# the acquisition facilitator is a type of "focused process facilitator", that is intended to serve as a command invoked
# by a client that is either a cli, or the general purpose process facilitator ProcessesFcltr class.
# it's receiver is a device facilitator, and the data it passes are the configurations (of type process_configs ->
# todo should standardize and document the configuration types at some point).

# checkout a device facilitator
# 0.  checkout a devices facilitator
df = DevicesFcltr()

path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
process_configs = load_process_configs(path=path)

# 1. get configurations
df.receive_device_configs_all_cycles(process_configs=process_configs,
                                     device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)

# checkout a single config from the loop
df.checkout_single_cycle_configs(key='view1 color488')

af.devices_fcltr = df
af.configs = process_configs
af.acquisition_mode1()
