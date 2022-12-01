from time import sleep

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr

# 0.  checkout a devices facilitator
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path

df = DevicesFcltr()

# 1. get configurations
df.load_device_configs_one_cycle(device_configs_file=device_fcltr_configs_path)

df.camera_prepare_camera()

df.camera_get_ready()

df.camera_start()

p =''
while p !='q':
    p=input('press q to exit...\n')
    sleep(0.05)

df.camera_stop()

df.camera_close()
