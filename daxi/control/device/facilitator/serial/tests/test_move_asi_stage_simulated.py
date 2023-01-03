from daxi.control.device.facilitator.serial.demos.demo_move_asi_stage_simulated import move_asi_stage_simulated


def test_move_asi_stage_simulated():
    msg = move_asi_stage_simulated()
    assert msg == 'success'
