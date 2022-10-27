# demo_devicefacilitator.py
from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path
from time import sleep

"""
using a device facilitator to:
load deviced configurations
prepare the divices
get_ready()
start()

so to some extend the DevicesFcltr is working like a workflow.

"""
# 0.  checkout a devices facilitator
df = DevicesFcltr()

# 1. get configurations
df.load_device_configs(device_configs_file=device_fcltr_configs_path)

# 2. prepare subtasks and calculate the data for all subtasks
df.daq_prepare_subtasks_ao()
df.daq_prepare_subtasks_do()

# 3. prepare metronome
df.daq_prepare_metronome()

# 4. prepare AO task bundle
df.daq_prepare_taskbundle_ao()
df.daq_prepare_taskbundle_do()

# 5. add metronome to ao task bundle
df.daq_add_metronome()

# 6. add sub-tasks for ao task bundle
df.daq_add_subtasks_ao()
df.daq_add_subtasks_do()

# 7. get ready
df.daq_get_ready()

# 8. start
df.daq_start()

# 9. wait for user to quit the process
print('enter q to quit...')
while input() != 'q':
    sleep(0.05)

# 10. close the task
df.daq_close()
