from daxi.control.process.facilitator.inspection.demos.demo_inspectionfcltr_execute_metronome import \
    demo_inspectionfcltr_execute_metronome


def test_inspectionfcltr_execute_metronome():
    msg = demo_inspectionfcltr_execute_metronome()
    assert msg == 'successful'
