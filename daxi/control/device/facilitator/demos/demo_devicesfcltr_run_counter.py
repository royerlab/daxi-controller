import datetime
import os
from time import sleep

from matplotlib import pyplot as plt
import numpy as np

# from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
# from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
#     NIDAQDevicesConfigsGeneratorMode1
# from daxi.ctr_devicesfacilitator.nidaq.nidaq import SubTaskAO
# from daxi.ctr_processesfacilitator.processes_facilitator import load_process_configs
from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

# this demo uses device facilitator to control a counter.

# checkout a device facilitator:
devices_fcltr = DevicesFcltr(devices_connected=devices_connected)

# load process configuration template
path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
process_configs = load_process_configs(path=path)

# 1. receive configurations and checkout a singel configuration.
devices_fcltr.receive_device_configs_all_cycles(process_configs=process_configs,
                                                daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
first_cycle_key = next(iter(devices_fcltr.configs_single_cycle_dict))
devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                            verbose=True)

# 2. prepare the counter
devices_fcltr.daq_prepare_counter()

# 3. counter get ready:
devices_fcltr.counter.get_ready()


# 4. start counter
devices_fcltr.counter.start()

# 5. test counting
frame_number_pre = 0
frame_number = 0

print('test counting, this will count up to 100 frames and stop.')
counting = True
while counting:
    while frame_number == frame_number_pre:
        frame_number = devices_fcltr.counter.read()
        sleep(0.001)
    current_time = datetime.datetime.now()
    print('frame number is ' + str(frame_number) + ', curren time is ' + str(current_time))
    frame_number_pre = frame_number
    if frame_number_pre >= 100:
        counting = False

# stop counter
devices_fcltr.counter.stop()

# close counter
devices_fcltr.counter.close()

