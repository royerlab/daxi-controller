# first load and receive all configurations from tempalte
# check demo_devicesfcltr_receive_and_map_configs.py for details

# 0.  checkout a devices facilitator
import os
from pprint import pprint

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.device.facilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates


def demo_devicefcltr_checkout_configs_from_all_cycles_by_key(verbose=True):
    df = DevicesFcltr()
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    configs = load_process_configs(path=path)
    df.receive_device_configs_all_cycles(process_configs=configs,
                                         daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
    # before mapping:
    if verbose:
        print('before mapping')
        pprint(df.configs_405_laser)
    assert df.configs_405_laser is None

    # mapping
    if verbose:
        print('mapping/checking out a configuration for a single cycle')
    df.checkout_single_cycle_configs(key='view1 color488')
    assert df.configs_405_laser is not None

    # after mapping:
    if verbose:
        print('after mapping')
        pprint(df.configs_405_laser)

    return 'success'


if __name__ == "__main__":
    demo_devicefcltr_checkout_configs_from_all_cycles_by_key(verbose=False)
