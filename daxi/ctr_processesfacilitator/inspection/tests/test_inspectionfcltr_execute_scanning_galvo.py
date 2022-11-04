from daxi.ctr_processesfacilitator.inspection.demos.demo_inspectionfcltr_execute_scanning_galvo import \
    demo_inspectionfcltr_execute_scanning_galvo


def test_inspectionfcltr_execute_scanning_galvo():
    msg = demo_inspectionfcltr_execute_scanning_galvo()
    assert msg == 'successful'
