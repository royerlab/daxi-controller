from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_filter_wheel import \
    demo_inspectionfcltr_execute_fileter_wheel


def test_inspectionfcltr_execute_fileter_wheel():
    msg = demo_inspectionfcltr_execute_fileter_wheel()
    assert msg == 'successful'

