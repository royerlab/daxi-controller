import os

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.process.facilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


def demo_acquisition_fcltr_execute():
    # get a device facilitator object
    d = DevicesFcltr(devices_connected=devices_connected)

    # load process configuration template
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)

    a = AcquisitionFcltr()
    a.execute(devices_fcltr=d, process_configs=process_configs)
    return 'successful'


if __name__ == 'main':
    demo_acquisition_fcltr_execute()
