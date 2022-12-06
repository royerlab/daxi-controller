from daxi.control.device.facilitator.serial.daxi_ms2k_stage import DaxiMs2kStage

# conect to the asi stage used on the DaXi microscope. We are using a MS2000 stage from ASI.
a = DaxiMs2kStage("COM6", 9600)
a.connect()

# store the current position of the stage.
a.store_current_position()

pos = a.define_explicit_position(name='p1')
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
