from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_VSG2 import \
    demo_inspectionfcltr_execute_VSG2


def test_inspectionfcltr_execute_VSG2():
    msg = demo_inspectionfcltr_execute_VSG2()
    assert msg == 'successful'

