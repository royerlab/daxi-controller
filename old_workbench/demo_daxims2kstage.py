from old_workbench.asistage.daxims2kstage import DaxiMs2kStage

# conect to the asi stage used on the DaXi microscope. We are using a MS2000 stage from ASI.
a = DaxiMs2kStage("COM6", 9600)

# store the current position of the stage.
a.store_current_position()

# check the list of current positions:
print('a.stored_positions')
print(a.stored_positions)

# Define an explicit position using a built-in function, the settings would be the default number
pos = a.define_explicit_position(name='p1')

# Add the position to the .stored_position dictionary
a.stored_positions['p1'] = pos

# Define an explicit position using a built-in function, the settings would be the default number
pos = {'unit': 'mm',
     'X': 0.4212,
     'Y': 0.0001,
     'scan configurations': {'scan speed': 0.00528,
                             'scan range': 2.0,
                             'start position': 0.4212,
                             'end position': 2.4212,
                             'encoder divide': 24}}

# add the position to the .stored_position dictionary
a.stored_positions['p2'] = pos

print('a.stored_positions')
print(a.stored_positions)

a.move_to('p1')
# in the mean while move the joy stick so the stage is at a different position.
# then record that position

input('now we are going to get ready at position p1 for raster scan, press any key to continue...')
a.raster_scan_ready(position_name='p1')

input('press any key to start the raster scan...')
a.raster_scan_go()

input('now we are moving to p2')
a.move_to('p2')

input('now we are going to get ready at p2 for raster scan, press any key to continue...')
a.raster_scan_ready(position_name='p2')

input('press any key to start the raster scan at p2...')
a.raster_scan_go()
