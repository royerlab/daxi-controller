import os
from time import sleep

from matplotlib import pyplot as plt
import numpy as np

from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.ctr_devicesfacilitator.nidaq.nidaq import SubTaskAO
from daxi.ctr_processesfacilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

# this demo uses device facilitator to control a scanning galvo.

# checkout a device facilitator:
devices_fcltr = DevicesFcltr(devices_connected=devices_connected)

# load process configuration template
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
process_configs = load_process_configs(path=path)

# 1. receive configurations and checkout a singel configuration.
devices_fcltr.receive_device_configs_all_cycles(
    process_configs=process_configs,
    device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
first_cycle_key = next(iter(devices_fcltr.configs_single_cycle_dict))
devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                            verbose=True)

# 2. prepare the SG as an ao subtask
config = getattr(devices_fcltr, 'configs_scanning_galvo')
devices_fcltr.subtask_ao_configs_list = [config]
st = SubTaskAO(config)
if st.data is None:
    st.generate_data()
devices_fcltr.subtask_ao_list = [st]

# plot voltage profiles together with the metronome ticks.
metronome_frequency = devices_fcltr.configs_metronome['frequency']
scanning_galvo_data = devices_fcltr.configs_scanning_galvo['data']
time_ticks = np.arange(len(scanning_galvo_data))/metronome_frequency  # unit: seconds.
plt.plot(time_ticks, scanning_galvo_data)
plt.show()

# 3. prepare metronome
devices_fcltr.daq_prepare_metronome()

# 4. prepare AO task bundle
devices_fcltr.daq_prepare_taskbundle_ao()

# 5. add metronome to the ao task bundle
devices_fcltr.taskbundle_ao.add_metronome(devices_fcltr.metronome)

# 6. add sub-tasks for ao task bundle
devices_fcltr.daq_add_subtasks_ao()

# 7. get ready, start, stop and close
devices_fcltr.taskbundle_ao.get_ready()
devices_fcltr.metronome.get_ready()

devices_fcltr.taskbundle_ao.start()
devices_fcltr.metronome.start()

print('enter q to quit...')
while input() != 'q':
    sleep(0.05)

sleep(0.05)

devices_fcltr.taskbundle_ao.stop()
devices_fcltr.metronome.stop()

devices_fcltr.taskbundle_ao.close()
devices_fcltr.metronome.close()
