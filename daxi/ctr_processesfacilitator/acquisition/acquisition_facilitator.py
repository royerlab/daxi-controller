"""
This facilitator should interact with the main gui, comsolidate all the configurations and send it to
the device and data tools facilitators.
"""
from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1


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
        self.devices_fcltr = None
        self.configs = None
        # make sure the receiver and data is passed into the execute method, so the same command cna perform different
        # command once the configurations are changed in the client. (may not be the case in cli, but will be in gui.)
        # advantage of making the receiver and data as attributes of the command: it will be logged by the invoker, so
        # there is a record of all the specifics.

    def execute(self, device_fcltr, process_configs):
        """
        look at the configurations and perform the acquisition for all devices.
        this object serves as a command.

        based on the receiver and the data, perform the process.
        should do checkout and mapping of devices configs for all cycle types somwhere.
        think about it s hould be execute levle, or acquisition_mode1 level.
        :return:
        """
        self.devices_fcltr = device_fcltr
        self.configs = process_configs
        if self.configs['process configs']['process type'] == 'acquisition, mode 1':
            self.acquisition_mode1()

        return 0

    def acquisition_mode1(self):
        # [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
        print("stepped into AcquisitionFacilitator.acquisition_mode1\n")
        # 1. receive configurations
        self.devices_fcltr.receive_device_configs_all_cycles(
                                    process_configs=self.configs,
                                    device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
        first_cycle_key = next(iter(self.devices_fcltr.configs_single_cycle_dict))
        self.devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                                         verbose=True)
        position_list = self.configs['process configs']['acquisition parameters']['positions']
        view_list = self.configs['process configs']['acquisition parameters']['views']
        color_list = self.configs['process configs']['acquisition parameters']['colors']

        # 2. prepare subtasks and calculate the data for all subtasks
        self.devices_fcltr.daq_prepare_subtasks_ao()
        self.devices_fcltr.daq_prepare_subtasks_do()

        # 3. prepare metronome
        self.devices_fcltr.daq_prepare_metronome()

        # 4. prepare AO task bundle
        self.devices_fcltr.daq_prepare_taskbundle_ao()
        self.devices_fcltr.daq_prepare_taskbundle_do()

        # 5. add metronome to ao task bundle
        self.devices_fcltr.daq_add_metronome()

        # 6. add sub-tasks for ao task bundle
        self.devices_fcltr.daq_add_subtasks_ao()
        self.devices_fcltr.daq_add_subtasks_do()

        # 7. get ready
        self.devices_fcltr.daq_get_ready()

        # ASI stage get ready (handle the receivers) (design for now and leave implementation after framework with a
        # working daq is done)
        # copy/organize from the previous ad-hoc in the old_workbench
        # demo - indevelopment -set raster scanning speed.py
        # think:
        # this should be in device facilitator

        # camera get ready (for now, display an image to prompt the user to run the HCI)
        # daq card configure and everybody get ready (do it through the DevicesFcilitator, map, chekcout 1
        # configuration and start everything)
        # loop over positions
        for position in position_list:
            print('\n moving to this position: ' + str(position))
            # move the stage to the position

            # need to get devices ready before looping

            # loop over views
            for view in view_list:
                print(' --- now going to this view: view' + str(view))
                # loop over colors
                for color in color_list:
                    print(' --- --- now switching to this color: color' + str(color))
                    # move the filter wheel
                    # think about it:
                    # this should be done under devices facilitator and should be calling the serial devices.
                    self.devices_fcltr.serial_move_filter_wheel(color)  # manual for now XD.. sigh. - well, tolerable.

                    # based on the view and color indexes, choose a daq data cycle index. (This is actually implemented
                    # in DevicesFcltr)
                    self.devices_fcltr.checkout_single_cycle_configs(key='view'+str(view)+' color'+str(color),
                                                                     verbose=True)
                    # write data to daq card again for the changed cycle index.
                    self.devices_fcltr.daq_update_data()
                    # start daq card (waiting for the trigger)
                    self.devices_fcltr.daq_start()
                    # start camera (waiting for the trigger)
                    self.devices_fcltr.camera_start()
                    # start raster scan of asi-stage (will send out the trigger)
                    self.devices_fcltr.stage_start()
                    # loop over slice›
                    # stop(pause) daq card

        # todo need to check how to re-trigger camera acquisition with the same acquisition protocol.
        # think about the structure of the data here # todo 2022-10-25 item 1.
        print("will first get all the devices ready for the device facilitator, that is \n"
              "appended in this class. we'll do something like self.devcie_fcltr.receive_\n"
              "device_configs() to make sure the configs is received we'll then do \n "
              "self.device_facilitators.\"prepare_everything_and_play_the_devices\" to make \n"
              "sure all the devices are initiated and ready at the minimum level")
        print("we will then go through the loop order shown above in the comments, to actually \n"
              "perform this acquisition task\n")
        print("stepped out of AcquisitionFacilitator.acquisition_mode1")
        return 0
