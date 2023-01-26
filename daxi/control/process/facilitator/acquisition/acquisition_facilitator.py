"""
This facilitator should interact with the main gui, comsolidate all the configurations and send it to
the device and data tools facilitators.
"""
import os
from time import sleep

import numpy as np
# from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
#     NIDAQDevicesConfigsGeneratorMode1
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1, CameraConfigsGeneratorMode1, StageConfigsGeneratorMode1
from daxi.control.device.facilitator.devicesfacilitator import prepare_all_devices_and_get_ready
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

if devices_connected is False:
    is_simulation = True


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

    def execute(self, devices_fcltr=None, data_fcltr=None, process_configs=None):
        """
        look at the configurations and perform the acquisition for all devices.
        this object serves as a command.

        based on the receiver and the data, perform the process.
        should do checkout and mapping of devices configs for all cycle types somwhere.
        think about it s hould be execute levle, or acquisition_mode1 level.
        :return:
        """
        self.devices_fcltr = devices_fcltr
        self.configs = process_configs
        self.data_fcltr = data_fcltr
        if self.configs['process configs']['process type'] == 'acquisition, mode 1':
            self.acquisition_mode1()

        if self.configs['process configs']['process type'] == 'acquisition, mode 7':
            self.acquisition_mode7()


        return 0

    def acquisition_mode1(self):
        # [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
        # Here, the configurations for the camera and the ASI stage is maintained the same for all cycles.
        print("stepped into AcquisitionFacilitator.acquisition_mode1\n")

        # 1. receive configurations (done by device facilitator)
        self.devices_fcltr.receive_device_configs_all_cycles(process_configs=self.configs,
                                                             daqdevice_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1,
                                                             camera_configs_generator_class=CameraConfigsGeneratorMode1,
                                                             stage_configs_generator_class=StageConfigsGeneratorMode1)
        # get the first cycle key
        first_cycle_key = next(iter(self.devices_fcltr.configs_daq_single_cycle_dict))

        # checkout the configurations of a single cycle by key
        self.devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                                         verbose=True)

        # convenience codes
        position_list = self.configs['process configs']['acquisition parameters']['positions']
        view_list = self.configs['process configs']['acquisition parameters']['views']
        color_list = self.configs['process configs']['acquisition parameters']['colors']
        number_of_time_points = self.configs['process configs']['acquisition parameters']['number of time points']
        slice_number = self.configs['process configs']['acquisition parameters']['n slices'] + 1

        os.system('echo test system output')
        os.system('echo number of positions: ' + str(len(position_list)))
        os.system('echo views: ' + str(view_list))
        os.system('echo colors: ' + str(color_list))
        os.system('echo number of time points: ' + str(number_of_time_points))
        os.system('echo number of slices: ' + str(slice_number))

        prepare_all_devices_and_get_ready(devices_fcltr=self.devices_fcltr, is_simulation=is_simulation)

        # loop over time points
        for time_point_index in np.arange(number_of_time_points):
            os.system('echo ')
            os.system('echo starting time point: ' + str(time_point_index))
            # loop over positions
            for position in position_list:
                os.system('echo moving to this position: ' + str(position))
                # move the stage to the position
                self.devices_fcltr.stage_move_to(position)
                # ASI stage get ready at the position (this line has to be here due to mode1 specifics)
                # looping order:
                # [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
                self.devices_fcltr.stage_raster_scan_get_ready_at_position(
                    position_name=position,
                    )

                # loop over views.
                for view in view_list:
                    os.system('echo --- going to this view: view' + str(view))
                    # loop over colors.
                    for color in color_list:
                        os.system('echo --- --- switching to this color: color' + str(color))
                        os.system('echo --- --- --- current: time point: ' + str(time_point_index) +
                                  ', position: ' + str(position) + ', view' + str(view) + ', color' + str(color))
                        # move the filter wheel.
                        self.devices_fcltr.serial_move_filter_wheel(color)

                        # based on the view and color indexes, choose a daq data cycle index. (This is
                        # actually implemented in DevicesFcltr)
                        cycle_key = 'view'+str(view) + ' color' + str(color) # get the cycle key for this cycle
                        self.devices_fcltr.checkout_single_cycle_configs(key=cycle_key,
                                                                         verbose=True)

                        # update and write data to daq card for the current cycle index.
                        self.devices_fcltr.daq_update_data()
                        self.devices_fcltr.daq_write_data()
                        # start daq card (waiting for the trigger)
                        self.devices_fcltr.daq_start()
                        # start camera (waiting for the trigger)
                        self.devices_fcltr.camera_start()
                        # start raster scan of asi-stage (will send out the trigger)
                        self.devices_fcltr.stage_start_raster_scan()
                        # loop over slices for the stack:
                        counter = 0
                        os.system('echo single stack acquisition starts ...')
                        while counter <= slice_number - 1:
                            # trap the process in this while-loop until the counter reaches the desired count.
                            counter = self.devices_fcltr.counter.read()
                            sleep(0.003)
                        os.system('echo counted number of slices: '+str(counter))
                        # stop(pause) daq card
                        self.devices_fcltr.daq_stop()
                        self.devices_fcltr.camera_stop()
                        os.system('echo single stack acquisition ends.')
                        os.system('echo .')

        self.devices_fcltr.daq_close()
        self.devices_fcltr.camera_close()
        # perhaps we shouldn't close the camera. Should test and see if the camera is re-trigger-able when stopped.
        # self.devices_fcltr.stage_close()  # seems like it is not necessary to call a function to close the stage.

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

    def acquisition_mode7(self):
        """
        this will be acquisition mode 7 - which is mode1 with O1 scan, instead of LS3 scan.
        @return:
        """
        print('\n[implement acquisition mode 7 here]\n')
        return 0
