# conect to the asi stage used on the DaXi microscope. We are using a MS2000 stage from ASI.
from daxi.control.device.facilitator.serial.daxi_ms2k_stage import DaxiMs2kStage


def demo_asi_stage_store_current_position():
    a = DaxiMs2kStage("COM6", 9600)
    a.connect()

    # store the current position of the stage.
    a.store_current_position()
    print('\n\nnow display the list of stored positions:')

    print(a.stored_positions)
    return 'success'


if __name__ == '__main__':
    msg = demo_asi_stage_store_current_position()
