from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_405laser import \
    demo_inspectionfcltr_execute_405_laser


def test_inspectionfcltr_execute_405_laser():
    msg = demo_inspectionfcltr_execute_405_laser()
    assert msg == 'successful'
