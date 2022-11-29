from daxi.control.process.facilitator.inspection.demos.demo_inspectionfcltr_execute_counter import \
    demo_inspectionfcltr_execute_counter


def test_inspectionfcltr_execute_counter():
    msg = demo_inspectionfcltr_execute_counter()
    assert msg == 'successful'
