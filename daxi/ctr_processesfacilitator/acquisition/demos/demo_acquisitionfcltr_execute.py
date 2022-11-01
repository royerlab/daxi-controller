import os

from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
from daxi.ctr_processesfacilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.ctr_processesfacilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates


def demo_acquisition_fcltr_execute():
    # get a device facilitator object
    d = DevicesFcltr()

    # load process configuration template
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)

    a = AcquisitionFcltr()
    a.execute(device_fcltr=d, process_configs=process_configs)
    return 'successful'


if __name__ == 'main':
    demo_acquisition_fcltr_execute()
