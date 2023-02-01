from daxi.control.device.pool.orca_flash4 import OrcaFlash4
# codes below is copied over from the master_pulse_start_trigger demo, modify from there.
if __name__ == '__main__':
    # first define a camera configuration dictionary
    camera_configs={}
    camera_configs['exposure time (ms)'] = 150
    camera_configs['frame number'] = 100
    camera_configs['trigger source'] = 'MASTER PULSE'
    camera_configs['trigger mode'] = 'NORMAL'
    camera_configs['trigger polarity'] = 'POSITIVE'
    camera_configs['trigger times'] = 1  # seems irrelevant with the master pulse mode.
    camera_configs['output trigger kind'] = 'TRIGGER READY'
    camera_configs['output trigger polarity'] = 'POSITIVE'  # here the trigger will be sent out as a falling edge.
    # camera_configs['output trigger polarity'] = 'NEGATIVE'
    camera_configs['master pulse mode'] = 'BURST'
    camera_configs['burst times'] = 8  # this is the total number of frames/output triggers during one "burst".
    camera_configs['master pulse interval'] = 0.2  # note that if this interval time is shorter than the exposure time, then there will be problems. Exposure time is always ensured at higher priority.
    camera_configs['master pulse trigger'] = 'EXTERNAL'
    camera_configs['buffer size (frame number)'] = 200

    # now prepare the camera
    camera = OrcaFlash4()

    camera.get_ready(camera_ids=[0])

    camera.set_configurations(camera_configs=camera_configs, camera_ids=[0])

    camera.start(camera_ids=[0])

    p = ''
    while p != 'q':
        p = input('press q to exit ...')

    camera.stop(camera_ids=[0])

    camera.release_buffer(camera_ids=[0])

    camera.close(camera_ids=[0])
