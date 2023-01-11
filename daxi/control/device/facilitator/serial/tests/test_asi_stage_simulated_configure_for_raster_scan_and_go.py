from daxi.control.device.facilitator.serial.demos.demo_asi_stage_simulated_configure_for_raster_scan_and_go import \
    demo_asi_stage_simulated_configure_raster_scan_and_go


def test_asi_stage_simulated_configure_raster_scan_and_go():
    msg = demo_asi_stage_simulated_configure_raster_scan_and_go()
    assert msg == 'success'
