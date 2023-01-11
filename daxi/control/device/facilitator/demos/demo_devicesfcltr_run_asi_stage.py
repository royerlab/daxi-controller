from time import sleep

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr

# checkout a device facilitator
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path

df = DevicesFcltr()

# 1. get configurations
df.load_device_configs_one_cycle(device_configs_file=device_fcltr_configs_path)

# 2. prepare the asi stage
df.stage_prepare()


# 3. get ready of the stage
df.stage_get_ready()  # separating this step from the 'prepare' step is useful from the process facilitator level.

# 4. define a series of positions
p1 = df.stage_get_current_position()
p2 = df.stage_define_explicit_position(unit='mm',
                                       x=1.0,
                                       y=1.0)
p3 = df.stage_define_explicit_position(unit='mm',
                                       x=2.0,
                                       y=2.0)

# loop over all positions
for name in ['p1', 'p2', 'p3']:
    # add the positions to the position list
    df.stage_add_position(name=name, pos=p1)

    # configure the raster scan configurations for these positions
    df.stage_raster_scan_set_configs(position_name=name,
                                     scan_range=df.configs_asi_stage['scan range'],
                                     encoder_divide=df.configs_asi_stage['encoder divide'],
                                     scan_speed=df.configs_asi_stage['scan speed'])

for name in ['p1', 'p2', 'p3']:
    p = ''
    while p != 'p':
        p = input('press p to go to '+name+' and scan...')
        sleep(0.05)
    df.stage_raster_scan_get_ready_at_position(name)
    df.stage_start_raster_scan()
