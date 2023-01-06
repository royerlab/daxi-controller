from daxi.control.data.facilitator.display.demos.demo_napari4daxi import demo_daxiviewer
from time import sleep

from daxi.control.data.facilitator.display.napari4daxi import DaXiViewer
from daxi.control.data.facilitator.processing.process_stacks import StackProcessing
from daxi.control.device.facilitator.direct.orca_flash4_simulated import OrcaFlash4Simulation
from matplotlib import pyplot as plt
import numpy as np

from daxi.control.device.facilitator.nidaq.counter import Counter
from daxi.control.device.facilitator.nidaq.simulated_counter import SimulatedCounter
from daxi.control.device.pool.orca_flash4 import OrcaFlash4
from daxi.globals_configs_constants_general_tools_needbettername.constants import virtual_tools_configs_path
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser


def real_orca_camera_image_feeder(camera: OrcaFlash4, processor=None, counter=None):
    counter_output = counter.read()
    processor.camera = camera
    print('counter output is:' + str(counter_output))
    stitched_mips = processor.get_current_stitched_mips(camera_id=0, current_frame_count=counter_output)
    return stitched_mips


def demo_daxiviewer_on_real_orca_flash4():
    # this demo itself may function as the combination of a process/data/device fcltr.
    camera = OrcaFlash4()  # this is a device
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
    # get counter configs:
    p = NIDAQConfigsParser()
    p.set_configs_path(virtual_tools_configs_path)
    section = 'Virtual Tools Section'
    keyword = 'counter'
    configs = \
        p.get_configs_by_path_section_keyword(section, keyword)

    # prepare a counter (look at the counter demo)
    counter = Counter()  # this is a device
    counter.set_configurations(counter_configs=configs)
    counter.get_ready()
    counter.start()
    p = StackProcessing()  # this is a data tool
    daxi_viewer = DaXiViewer()  # this is a data tool
    daxi_viewer.prepare(
              image_feeder=real_orca_camera_image_feeder,
              camera=camera,
              processor=p,
              counter=counter,
              )
    daxi_viewer.go()
    counter.stop()
    counter.close()
    camera.stop()
    camera.release_buffer(camera_ids=[0])
    camera.close(camera_ids=[0])
    print('daxi_viewer session ended')
    return 'success'


if __name__ == '__main__':
    demo_daxiviewer_on_real_orca_flash4()
