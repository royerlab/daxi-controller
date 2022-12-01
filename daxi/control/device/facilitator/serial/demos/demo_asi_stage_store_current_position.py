# conect to the asi stage used on the DaXi microscope. We are using a MS2000 stage from ASI.
from daxi.control.device.facilitator.serial.daxims2kstage import DaxiMs2kStage

a = DaxiMs2kStage("COM6", 9600)

# store the current position of the stage.
a.store_current_position()
print('\n\nnow display the list of stored positions:')

print(a.stored_positions)

