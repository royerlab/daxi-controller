from daxi.control.device.facilitator.serial.daxims2kstage import DaxiMs2kStage

a = DaxiMs2kStage("COM6", 9600)
a.connect()

# store the current position of the stage.
a.store_current_position()


# get the current position:
p1 = a.get_current_position()

# define a position explicitly
p2 = a.define_explicit_position(x=1.0, y=1.0)

# append the positions to the stored position list:
a.stored_positions['p1'] = p1
a.stored_positions['p2'] = p2
a.add_current_position_to_list(name='p3')

# change speed
a.stored_positions['p1']['scan configurations']['encoder divide'] = 24
a.stored_positions['p1']['scan configurations']['scan speed'] = 5  # 0.528

print('\n\nnow display the list of stored positions:')
print(a.stored_positions)

print(a.stored_positions.keys())

