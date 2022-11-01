# demo_devicesfcltr_load_and_run.py
import os

from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.ctr_processesfacilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import device_fcltr_configs_path, \
    process_templates
from time import sleep


def demo_devicefcltr_receive_map_checkout_and_run(verbose=False, interactive=True):

    # 0.  checkout a devices facilitator
    df = DevicesFcltr()

    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    configs = load_process_configs(path=path)


    # 1. get configurations
    df.receive_device_configs_all_cycles(process_configs=configs,
                                         device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)

    # should have an extra step to choose a view/color, and map it to the
    # single cycle configs, then move on.

    df.checkout_single_cycle_configs(key='view1 color488')

    # 2. prepare subtasks and calculate the data for all subtasks
    df.daq_prepare_subtasks_ao()
    df.daq_prepare_subtasks_do()

    # 3. prepare metronome
    df.daq_prepare_metronome()

    # 4. prepare AO task bundle
    df.daq_prepare_taskbundle_ao()
    df.daq_prepare_taskbundle_do()

    # 5. add metronome to ao task bundle
    df.daq_add_metronome()

    # 6. add sub-tasks for ao task bundle
    df.daq_add_subtasks_ao()
    df.daq_add_subtasks_do()

    # 7. get ready
    df.daq_get_ready()

    # 8. start
    df.daq_start()

    # 9. wait for user to quit the process
    if interactive:
        print('enter q to quit...')
        while input() != 'q':
            sleep(0.05)

    sleep(0.05)

    # 10. close the task
    df.daq_close()
    if verbose:
        print('demo load device configurations and run ...')
    return 'success'


if __name__ == "__main__":
    demo_devicefcltr_receive_map_checkout_and_run(verbose=False, interactive=True)

