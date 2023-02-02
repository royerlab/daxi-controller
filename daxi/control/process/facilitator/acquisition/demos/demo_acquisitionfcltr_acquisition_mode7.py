import os
from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.process.facilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


def demo_acquisitionfcltr_acquisition_mode7(config_fname):
    # Define path to the configuration file
    path = os.path.join(process_templates, config_fname)
    process_configs = load_process_configs(path=path)

    # checkout a device facilitator
    df = DevicesFcltr(devices_connected=devices_connected)
    df.display_message = False

    # checkout an acquisition facilitator
    af = AcquisitionFcltr()

    # configure the acquisition facilitator
    af.devices_fcltr = df
    af.configs = process_configs
    af.configs['process configs']['acquisition parameters']['number of time points'] = 100
    # start mode7 acquisition
    af.acquisition_mode7()
    return 'success'


if __name__ == '__main__':
    demo_acquisitionfcltr_acquisition_mode7(config_fname='template_acquisition_mode7-dev-small_stack.yaml')
