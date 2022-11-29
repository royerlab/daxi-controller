# get a device facilitator object
# here we demonstrate how to use an InspectionFcltr to inspect 405 galvo (turn on, start, stop, close).

import os

from daxi.control.device.facilitator.devicefacilitator import DevicesFcltr
from daxi.control.process.facilitator.inspection.inspection_facilitator import InspectionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


def demo_inspectionfcltr_execute_405_laser():
    d = DevicesFcltr(devices_connected=devices_connected)

    # load process configuration template
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)

    # set the process to be inspecting metronome
    process_configs['process type'] = 'inspection, inspect_405_laser'
    process_configs['process configs']['process type'] = 'inspection, inspect_405_laser'

    inspection = InspectionFcltr()
    inspection.execute(devices_fcltr=d, process_configs=process_configs)
    return "successful"


if __name__ == '__main__':
    demo_inspectionfcltr_execute_405_laser()
