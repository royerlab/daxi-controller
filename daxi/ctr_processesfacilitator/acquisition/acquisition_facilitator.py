"""
This facilitator should interact with the main gui, comsolidate all the configurations and send it to
the device and data tools facilitators.
"""
from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr


class AcquisitionFcltr():
    """
    This is a concrete command in the command pattern.
    """
    def __init__(self):
        """

        :param receiver: [DeviceFcltr]. receiver is a device facilitator: it contains all the physical and
        virtual devices in DaXi.
        :param data: [dict] configurations for the entire process
        """
        self.device_fcltr = None
        self.configs = None
        # make sure the receiver and data is passed into the execute method, so the same command cna perform different
        # command once the configurations are changed in the client. (may not be the case in cli, but will be in gui.)
        # advantage of making the receiver and data as attributes of the command: it will be logged by the invoker, so
        # there is a record of all the specifics.

    def execute(self, device_fcltr, configs):
        """
        look at the configurations and perform the acquisition for all devices.
        this object serves as a command.

        based on the receiver and the data, perform the process.
        :return:
        """
        self.device_fcltr = device_fcltr
        self.configs = configs
        if self.configs['process configs']['process type'] == 'acquisition, mode 1':
            self.acquisition_mode1()

        return 0

    def acquisition_mode1(self):
        # [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]

        # ASI stage get ready (handle the receivers)
        # camera get ready
        # daq card configure and everybody get ready
        # loop over positions
            # move the stage to the position
            # loop over view
                # loop over color
                    # move the filter wheel
                    # based on the view and color indexes, choose a daq data cycle index.
                    # write data to daq card again for the changed cycle index.
                    # start daq card
                    # loop over slice
                    # stop(pause) daq card
        # todo need to check how to re-trigger camera acquisition with the same acquisition protocol.
        # think about the structure of the data here # todo 2022-10-25 item 1.
        print("stepped into AcquisitionFacilitator.acquisition_mode1\n")
        print("will first get all the devices ready for the device facilitator, that is \n"
              "appended in this class. we'll do something like self.devcie_fcltr.receive_\n"
              "device_configs() to make sure the configs is received we'll then do \n "
              "self.device_facilitators.\"prepare_everything_and_play_the_devices\" to make \n"
              "sure all the devices are initiated and ready at the minimum level")
        print("we will then go through the loop order shown above in the comments, to actually \n"
              "perform this acquisition task\n")
        print("stepped out of AcquisitionFacilitator.acquisition_mode1")
        return 0
