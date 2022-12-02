# get a device facilitator object.
# here we demonstrate how to use an InspectionFcltr to inspect the scanning galvo (turn on, start, stop, close).

import os

from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.process.facilitator.inspection.inspection_facilitator import InspectionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_templates
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected


def demo_inspectionfcltr_execute_scanning_galvo():
    d = DevicesFcltr(devices_connected=devices_connected)

    # load process configuration template
    path = os.path.join(process_templates, 'template_acquisition_mode1-dev.yaml')
    process_configs = load_process_configs(path=path)

    # set the process to be inspecting scanning galvo
    process_configs['process type'] = 'inspection, inspect_scanning_galvo'
    process_configs['process configs']['process type'] = 'inspection, inspect_scanning_galvo'

    inspection = InspectionFcltr()
    inspection.execute(devices_fcltr=d, process_configs=process_configs)
    assert inspection.status_scanning_galvo == "good"
    return "successful"


if __name__ == '__main__':
    demo_inspectionfcltr_execute_scanning_galvo()
