from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_561laser import \
    demo_inspectionfcltr_execute_561_laser


def test_inspectionfcltr_execute_561_laser():
    msg = demo_inspectionfcltr_execute_561_laser()
    assert msg == 'successful'
