from time import sleep

from daxi.control.device.pool.orca_flash4 import OrcaFlash4
from daxi.control.device.facilitator.serial.daxi_ms2k_stage import DaxiMs2kStage
import numpy as np
# codes below is copied over from the master_pulse_start_trigger demo, modify from there.
if __name__ == '__main__':
    # first define a camera configuration dictionary
    camera_configs={}
    camera_configs['exposure time (ms)'] = 40
    camera_configs['frame number'] = 100
    camera_configs['trigger source'] = 'MASTER PULSE'
    camera_configs['trigger mode'] = 'NORMAL'
    camera_configs['trigger polarity'] = 'POSITIVE'
    camera_configs['trigger times'] = 1  # seems irrelevant with the master pulse mode.
    camera_configs['output trigger kind'] = 'TRIGGER READY'
    camera_configs['output trigger polarity'] = 'POSITIVE'  # here the trigger will be sent out as a falling edge.
    camera_configs['master pulse mode'] = 'BURST'
    camera_configs['burst times'] = 30  # this is the total number of frames/output triggers during one "burst".
    camera_configs['master pulse interval'] =camera_configs['exposure time (ms)']/1000 + 0.010  # note that if this interval time is shorter than the exposure time, then there will be problems. Exposure time is always ensured at higher priority.
    camera_configs['master pulse trigger'] = 'EXTERNAL'
    camera_configs['buffer size (frame number)'] = 200

    # now prepare the camera
    camera = OrcaFlash4()
    camera.get_ready(camera_ids=[0])
    camera.set_configurations(camera_configs=camera_configs, camera_ids=[0])
    camera.start(camera_ids=[0])

    # now configure the stage
    # conect to the asi stage used on the DaXi microscope. We are using a MS2000 stage from ASI.
    a = DaxiMs2kStage("COM6", 9600)
    a.connect()

    # store the current position of the stage.
    pos = a.define_explicit_position()
    print('pos:')
    print(pos)
    pos['scan configurations']['encoder divide'] = 24
    pos['scan configurations']['scan speed'] = 0.5  # 0.528
    pos['scan configurations']['scan range'] = 0.1  # 0.528

    a.stored_positions['p1'] = pos

    a.move_to('p1')
    a.raster_scan_ready(position_name='p1')

    pause_time=2
    sleep(pause_time)

    for _ in np.arange(50):
        a.raster_scan_ready(position_name='p1')
        a.raster_scan_go()
        sleep(pause_time)
        print('there should be many bursts of acquisition, each burst has 3 frames')

    camera.stop(camera_ids=[0])
    camera.release_buffer(camera_ids=[0])
    camera.close(camera_ids=[0])



