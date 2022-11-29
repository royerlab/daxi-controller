from daxi.control.process.facilitator.inspection.demos.demo_inspectionfcltr_execute_gammaG import \
    demo_inspectionfcltr_execute_gammaG


def test_inspectionfcltr_execute_gammaG():
    msg = demo_inspectionfcltr_execute_gammaG()
    assert msg == 'successful'

