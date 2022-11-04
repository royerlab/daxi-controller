from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_bright_field import \
    demo_inspectionfcltr_execute_bright_field


def test_inspectionfcltr_execute_bright_field():
    msg = demo_inspectionfcltr_execute_bright_field()
    assert msg == 'successful'

