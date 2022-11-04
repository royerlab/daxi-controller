from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_VSG1 import \
    demo_inspectionfcltr_execute_VSG1


def test_inspectionfcltr_execute_VSG1():
    msg = demo_inspectionfcltr_execute_VSG1()
    assert msg == 'successful'

