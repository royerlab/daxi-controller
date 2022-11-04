from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_O3 import \
    demo_inspectionfcltr_execute_O3


def test_inspectionfcltr_execute_O3():
    msg = demo_inspectionfcltr_execute_O3()
    assert msg == 'successful'

