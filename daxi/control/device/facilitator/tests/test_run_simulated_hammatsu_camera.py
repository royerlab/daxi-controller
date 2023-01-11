from daxi.control.device.facilitator.demos.demo_devicesfcltr_run_simulated_hamamatsu_camera import \
    demo_run_simulated_hamamatsu_camera


def test_run_simulated_hamamatsu_camera():
    msg = demo_run_simulated_hamamatsu_camera(interactive=False)
    assert msg == 'success'
