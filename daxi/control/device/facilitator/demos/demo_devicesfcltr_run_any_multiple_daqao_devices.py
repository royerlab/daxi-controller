import os
from time import sleep

from matplotlib import pyplot as plt
import numpy as np


from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.device.facilitator.nidaq.nidaq import SubTaskAO
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
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

# prepare a list of names of the devices configurations attributes.
sg = 'configs_scanning_galvo'
vsg1 = 'configs_view_switching_galvo_1'
vsg2 = 'configs_view_switching_galvo_2'
beta = 'configs_beta_galvo_light_sheet_incident_angle'
gamma = 'configs_gamma_galvo_strip_reduction'
# metronome = 'configs_metronome'
# counter = 'counter'
# l405 = 'configs_405_laser'
# l488 = 'configs_488_laser'
# l561 = 'configs_561_laser'
# l639 = 'configs_639_laser'
# bfled = 'configs_bright_field'
O1 = 'configs_O1'
O3 = 'configs_O3'


# 2. prepare the SG as an ao subtask
config_SG = getattr(devices_fcltr, 'configs_scanning_galvo')
# get the data for SG galvo so it is a scanning curve.
st_sg = SubTaskAO(config_SG)
if st_sg.data is None:
    st_sg.generate_data()


devices_list = [sg, vsg1, vsg2, beta, gamma, O1, O3]
devices_fcltr.subtask_ao_list=[]

for device_name in devices_list:
    config = getattr(devices_fcltr, device_name)
    devices_fcltr.subtask_ao_configs_list = [config]

    # copy the SG data to the vsg1 so we can see it scans.
    st = SubTaskAO(config)
    st.data = st_sg.data

    devices_fcltr.subtask_ao_list.append(st)

# plot voltage profiles together with the metronome ticks.
metronome_frequency = devices_fcltr.configs_metronome['frequency']
data = st.data
time_ticks = np.arange(len(data))/metronome_frequency  # unit: seconds.
plt.plot(time_ticks, data)
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
