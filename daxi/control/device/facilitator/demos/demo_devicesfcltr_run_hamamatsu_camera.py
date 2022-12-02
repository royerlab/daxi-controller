from time import sleep

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr

# 0.  checkout a devices facilitator
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path

df = DevicesFcltr()

# 1. get configurations
df.load_device_configs_one_cycle(device_configs_file=device_fcltr_configs_path)

# 2. prepare the camera
df.camera_prepare()

# 3. get ready the camera
df.camera_get_ready()

# 4. start the camera
df.camera_start()

# 5. user termination
p =''
while p !='q':
    p=input('press q to exit...\n')
    sleep(0.05)

# 6. stop the camera
df.camera_stop()

# 7. close the camera
df.camera_close()
