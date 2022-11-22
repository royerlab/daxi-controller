from copylot.hardware.orca_camera.camera import OrcaCamera

cam = OrcaCamera()
camera_configs={
    'exposure time (ms)': 100,
    'frame number': 100,
    'trigger source fvalue': 2, # this sets the TRIGGER SOURCE to external trigger.
    ''
    'output trigger': 'exposure',
}
cam.set_configurations(camera_configs)
