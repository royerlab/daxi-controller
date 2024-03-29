from daxi.control.device.facilitator.serial.daxi_ms2k_stage_simulated import DaxiMS2kStageSimulated


def demo_asi_stage_simulated_configure_raster_scan_and_go():
    a = DaxiMS2kStageSimulated("COM6", 9600)
    a.connect()

    # store the current position of the stage.
    a.store_current_position()

    pos = a.define_explicit_position()
    print('pos:')
    print(pos)
    pos['scan configurations']['encoder divide'] = 24
    pos['scan configurations']['scan speed'] = 5  # 0.528
    a.stored_positions['p1'] = pos
    print('a.stored_positions')
    print(a.stored_positions)
    a.move_to('p1')
    a.raster_scan_ready(position_name='p1')
    a.raster_scan_go()
    print()
    return 'success'


if __name__ == '__main__':
    msg = demo_asi_stage_simulated_configure_raster_scan_and_go()
    assert msg == 'success'
