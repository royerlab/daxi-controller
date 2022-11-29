from daxi.control.process.facilitator.inspection.demos.demo_inspectionfcltr_execute_O1 import \
    demo_inspectionfcltr_execute_O1


def test_inspectionfcltr_execute_O1():
    msg = demo_inspectionfcltr_execute_O1()
    assert msg == 'successful'

