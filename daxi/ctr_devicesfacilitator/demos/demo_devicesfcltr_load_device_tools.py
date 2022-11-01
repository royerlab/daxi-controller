from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path

# 0.  checkout a devices facilitator
df = DevicesFcltr()

# 1. get configurations
df.load_device_configs_one_cycle(device_configs_file=device_fcltr_configs_path)
