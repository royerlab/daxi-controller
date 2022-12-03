from time import sleep

from daxi.control.device.facilitator.direct.orca_flash4_simulated import OrcaFlash4Simulation


cam = OrcaFlash4Simulation(camera_index=0)
cam.live_capturing_return_images_get_ready()
data = cam.live_capturing_return_images_capture_image()
cam.live_capturing_return_images_capture_end()
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
camera_configs['buffer size (frame number)'] = 200
cam.set_configurations(camera_configs=camera_configs)

cam.start(camera_ids=[0])
p = ''
while p != 'q':
    p=input('type q to exit ... type n/y to turn off/on the capturing messages...')
    if p == 'n':
        cam.capturing_data_message(option='off', camera_ids=[0])
    if p == 'y':
        cam.capturing_data_message(option='on', camera_ids=[0])
    sleep(0.1)

cam.stop()
print('done')




