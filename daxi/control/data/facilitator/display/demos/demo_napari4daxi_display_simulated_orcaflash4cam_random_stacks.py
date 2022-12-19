from daxi.control.data.facilitator.display.demos.demo_napari4daxi import demo_daxiviewer
from time import sleep

from daxi.control.data.facilitator.display.napari4daxi import DaXiViewer
from daxi.control.data.facilitator.processing.process_stacks import get_3d_mips, StackProcessing
from daxi.control.device.facilitator.direct.orca_flash4_simulated import OrcaFlash4Simulation
from matplotlib import pyplot as plt
import numpy as np


def simulated_orca_camera_image_feeder(camera : OrcaFlash4Simulation):
    processor = StackProcessing()
    processor.camera = camera
    stitched_mips = processor.get_current_stitched_mips()
    return stitched_mips


def demo_daxiviewer_on_simulated_orca_flash4():
    a = DaXiViewer()
    camera = OrcaFlash4Simulation(camera_index=0)
    camera.get_ready(camera_ids=[0])
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
    camera.set_configurations(camera_configs=camera_configs)
    camera.start(camera_ids=[0])
    a.prepare(
              image_feeder=simulated_orca_camera_image_feeder,
              camera=camera,
              )
    a.go()
    return 'success'


if __name__ == '__main__':
    demo_daxiviewer_on_simulated_orca_flash4()
