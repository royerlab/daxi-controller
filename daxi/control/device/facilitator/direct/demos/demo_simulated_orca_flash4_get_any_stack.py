from time import sleep

from daxi.control.data.facilitator.processing.process_stacks import get_3d_mips
from daxi.control.device.facilitator.direct.orca_flash4_simulated import OrcaFlash4Simulation
from matplotlib import pyplot as plt
import numpy as np

cam = OrcaFlash4Simulation(camera_index=0)
cam.get_ready(camera_ids=[0])
# define camera configurations
camera_configs = {}
camera_configs['exposure time (ms)'] = 100
camera_configs['frame number'] = 100
camera_configs['trigger source'] = 'MASTER PULSE'
camera_configs['trigger mode'] = 'NORMAL'
camera_configs['trigger polarity'] = 'POSITIVE'
camera_configs['trigger times'] = 1
camera_configs['output trigger kind'] = 'TRIGGER READY'
camera_configs['output trigger polarity'] = 'POSITIVE'
camera_configs['master pulse mode'] = 'START'
camera_configs['burst times'] = 1
camera_configs['master pulse interval'] = 0.01
camera_configs['master pulse trigger'] = 'EXTERNAL'
camera_configs['buffer size (frame number)'] = 300
camera_configs['xdim'] = 100
camera_configs['ydim'] = 200


cam.set_configurations(camera_configs=camera_configs)

cam.start(camera_ids=[0])
for i in np.arange(100):
    sleep(1)
    stack = cam.get_any_stack(camera_id=0, stack_index=0)
    mip0, mip1, mip2, stitched_mips = get_3d_mips(stack=stack)
    plt.imshow(stitched_mips)
    plt.show()


cam.stop()
print('done')

