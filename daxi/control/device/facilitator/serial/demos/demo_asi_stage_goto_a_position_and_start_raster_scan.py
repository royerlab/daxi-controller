from time import sleep

from daxi.control.device.facilitator.serial.daxims2kstage import DaxiMs2kStage

# prepare the asi stage object

a = DaxiMs2kStage("COM6", 9600)
a.connect()
# store a series of positions
p1 = a.get_current_position()
p2 = a.define_explicit_position(x=1.0, y=1.0)
p3 = a.define_explicit_position(x=1.0, y=2.0)
p4 = a.define_explicit_position(x=1.0, y=3.0)

# append the positions to the stored position list:
a.stored_positions['p1'] = p1
a.stored_positions['p2'] = p2
a.stored_positions['p3'] = p3
a.stored_positions['p4'] = p4

p = ''
while p != 'p':
    p = input('press p to go to p1 and scan...')
    sleep(0.05)
a.move_to('p1')
a.raster_scan_ready(position_name='p1')
a.raster_scan_go()

p = ''
while p != 'p':
    p = input('press p to go to p2 and scan...')
    sleep(0.05)
a.move_to('p2')
a.raster_scan_ready(position_name='p2')
a.raster_scan_go()

p = ''
while p != 'p':
    p = input('press p to go to p3 and scan...')
    sleep(0.05)
a.move_to('p3')
a.raster_scan_ready(position_name='p3')
a.raster_scan_go()

p = ''
while p != 'p':
    p = input('press p to go to p4 and scan...')
    sleep(0.05)
a.move_to('p4')
a.raster_scan_ready(position_name='p4')
a.raster_scan_go()
