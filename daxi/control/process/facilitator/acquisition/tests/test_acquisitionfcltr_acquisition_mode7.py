from daxi.control.process.facilitator.acquisition.demos.demo_acquisitionfcltr_acquisition_mode7 import \
    demo_acquisitionfcltr_acquisition_mode7


def test_acquisitionfcltr_acquisition_mode7():
    msg = demo_acquisitionfcltr_acquisition_mode7(config_fname='pytest_mini_session_mode7.yaml')
    assert msg == 'success'
