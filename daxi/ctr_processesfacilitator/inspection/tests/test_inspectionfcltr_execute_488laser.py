from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_488laser import \
    demo_inspectionfcltr_execute_488_laser


def test_inspectionfcltr_execute_488_laser():
    msg = demo_inspectionfcltr_execute_488_laser()
    assert msg == 'successful'
