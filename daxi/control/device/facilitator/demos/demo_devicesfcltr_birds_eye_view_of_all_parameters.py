# this file demonstrates how to use the device facilitator to create a bird's-eye view of all parameters
# 0.  checkout a devices facilitator
import os
import numpy as np
from matplotlib import pyplot as plt


from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

df = DevicesFcltr(devices_connected=devices_connected)

path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
configs = load_process_configs(path=path)

# 1. receive configurations
df.receive_device_configs_all_cycles(process_configs=configs,
                                     daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)

# should have an extra step to choose a view/color, and map it to the
# single cycle configs, then move on.

df.checkout_single_cycle_configs(key='view1 color488')

plt.figure(figsize=(10, 10))
h = plt.subplot(4, 4, 1)
h.set_title('metronome')

h = plt.subplot(4, 4, 2)
# plot voltage profiles together with the metronome ticks.
metronome_frequency = df.configs_metronome['frequency']
scanning_galvo_data = df.configs_scanning_galvo['data']
time_ticks = np.arange(len(scanning_galvo_data))/metronome_frequency  # unit: seconds.
plt.plot(time_ticks, scanning_galvo_data)
h.set_title('SG info')
h.set_xlabel('time (s)')
h.set_ylabel('voltage (volt)')
plt.show()



