"""
This facilitator should interact with the main gui, comsolidate all the configurations and send it to
the device and data tools facilitators.
"""
import os
from time import sleep

import numpy as np
# from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
#     NIDAQDevicesConfigsGeneratorMode1
from daxi.control.data.facilitator.processing.process_stacks import get_3d_mips
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1, CameraConfigsGeneratorMode1, StageConfigsGeneratorMode1
from daxi.control.device.facilitator.config_tools.configuration_generator_mode7 import \
    NIDAQDevicesConfigsGeneratorMode7, CameraConfigsGeneratorMode7, StageConfigsGeneratorMode7
from daxi.control.device.facilitator.devicesfacilitator import prepare_all_devices_and_get_ready
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected
from skimage.io import imsave

if devices_connected is False:
    is_simulation = True
else:
    is_simulation = False


class AcquisitionFcltr():
    """
    This is a concrete command in the command pattern.
    """
    def __init__(self, verbose=True):
        """

        :param receiver: [DeviceFcltr]. receiver is a device facilitator: it contains all the physical and
        virtual devices in DaXi.
        :param data: [dict] configurations for the entire process
        """
        self.devices_fcltr = None
        self.configs = None
        self.verbose = verbose
        # make sure the receiver and data is passed into the execute method, so the same command cna perform different
        # command once the configurations are changed in the client. (may not be the case in cli, but will be in gui.)
        # advantage of making the receiver and data as attributes of the command: it will be logged by the invoker, so
        # there is a record of all the specifics.

    def _msg_1(self, verbose=False):
        if verbose:
            print("stepped into AcquisitionFacilitator.acquisition_mode1\n")
        pass

    def _msg_2(self, verbose=False):
        position_list, view_list, color_list, number_of_time_points, slice_number = self._convinience_reasign_params()
        if verbose:
            os.system('echo test system output')
            os.system('echo number of positions: ' + str(len(position_list)))
            os.system('echo views: ' + str(view_list))
            os.system('echo colors: ' + str(color_list))
            os.system('echo number of time points: ' + str(number_of_time_points))
            os.system('echo number of slices: ' + str(slice_number))

    def _msg_3(self, time_point_index=0, verbose=False):
        if verbose:
            os.system('echo ')
            os.system('echo starting time point: ' + str(time_point_index))

    def _msg_4(self, position, verbose=False):
        if verbose:
            os.system('echo moving to this position: ' + str(position))

    def _convinience_reasign_params(self):
        position_list = self.configs['process configs']['acquisition parameters']['positions']
        view_list = self.configs['process configs']['acquisition parameters']['views']
        color_list = self.configs['process configs']['acquisition parameters']['colors']
        number_of_time_points = self.configs['process configs']['acquisition parameters']['number of time points']
        slice_number = self.configs['process configs']['acquisition parameters']['n slices'] + 1
        return position_list, view_list, color_list, number_of_time_points, slice_number

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

    def _acquisition_looping_order_p_v_c_s(self,
                                           daq_configs_gclass=None,
                                           cam_configs_gclass=None,
                                           sta_configs_gclass=None):
        """
        This si the acquisition process with the p-v-c-s looping order:
        [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
        This looping order is currently used in mode1 and mode7 acquisitions. (with LS3 and O1 scan, there should be
        another mode that corresponds to SG scan).

        @param daq_configs_gclass:
        @param cam_configs_gclass:
        @param sta_configs_gclass:
        @return:
        """
        if self.configs['process configs']['process type'] == 'acquisition, mode 7':
            self.move_stage = False
        else:
            self.move_stage = True

        # Here, the configurations for the camera and the ASI stage is maintained the same for all cycles.
        self._msg_1(verbose=self.verbose)

        # 1. receive configurations (done by device facilitator)
        self.devices_fcltr.receive_device_configs_all_cycles(process_configs=self.configs,
                                                             daqdevice_configs_generator_class=daq_configs_gclass,
                                                             camera_configs_generator_class=cam_configs_gclass,
                                                             stage_configs_generator_class=sta_configs_gclass)
        # get the first cycle key
        first_cycle_key = next(iter(self.devices_fcltr.configs_daq_single_cycle_dict))

        # checkout the configurations of a single cycle by key
        self.devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                                         verbose=True)

        # convenience codes
        position_list, view_list, color_list, number_of_time_points, slice_number = self._convinience_reasign_params()

        self._msg_2(verbose=self.verbose)

        prepare_all_devices_and_get_ready(devices_fcltr=self.devices_fcltr, is_simulation=is_simulation)

        # loop over time points
        for time_point_index in np.arange(number_of_time_points):
            self._msg_3(verbose=self.verbose)

            # loop over positions
            for position in position_list:
                self._msg_4(position=position, verbose=self.verbose)

                # move the stage to the position
                if self.move_stage is True:
                    self.devices_fcltr.stage_move_to(position)

                # ASI stage get ready at the position (this line has to be here due to mode1 specifics)
                if self.move_stage is True:
                    self.devices_fcltr.stage_raster_scan_get_ready_at_position(position_name=position)

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
                        cycle_key = 'view' + str(view) + ' color' + str(color)  # get the cycle key for this cycle
                        self.devices_fcltr.checkout_single_cycle_configs(key=cycle_key, verbose=True)

                        # update and write data to daq card for the current cycle index.
                        self.devices_fcltr.daq_update_data()
                        self.devices_fcltr.daq_write_data()

                        # start daq card (waiting for the trigger)
                        self.devices_fcltr.daq_start()

                        # start camera (waiting for the trigger)
                        self.devices_fcltr.camera_start()

                        # start raster scan of asi-stage (will send out the trigger)
                        if self.move_stage is True:
                            self.devices_fcltr.stage_start_raster_scan()

                        # loop over slices for the stack:
                        counter_pre = 0
                        counter = 0
                        os.system('echo single stack acquisition starts ...')
                        while counter <= slice_number - 1:
                            # trap the process in this while-loop until the counter reaches the desired count.
                            counter = self.devices_fcltr.counter.read()
                            if counter is None:
                                counter = 0

                            if counter > counter_pre:
                                print('counter read: ' + str(counter))
                                counter_pre = counter
                            sleep(0.003)

                        os.system('echo counted number of slices: ' + str(counter))
                        # stop(pause) daq card
                        self.devices_fcltr.daq_stop()
                        self.devices_fcltr.camera_stop()

                        # data saving:
                        os.system('echo saving data: ' + str(counter))
                        stack_fname = 'STACK_position--' + position + '--view' + str(view) + '--color-' + str(color)+'.tif'
                        mips_fname = 'MIPS_position--' + position + '--view' + str(view) + '--color-' + str(color)+'.tif'
                        stack_path = os.path.join(self.data_saving_path, stack_fname)
                        mips_path = os.path.join(self.data_saving_path, mips_fname)

                        stack = self.devices_fcltr.camera.get_current_stack(camera_id=0, current_frame_count=14)
                        m = np.transpose(stack, (2, 0, 1))
                        imsave(stack_path, m)

                        mip0, mip1, mip2, stitched_mips = get_3d_mips(stack, stitched_mips_only=False)
                        imsave(mips_path, stitched_mips)

                        os.system('echo single stack acquisition ends.')
                        os.system('echo .')

        self.devices_fcltr.daq_close()
        self.devices_fcltr.camera_close()
        # perhaps we shouldn't close the camera. Should test and see if the camera is re-trigger-able when stopped.
        # self.devices_fcltr.stage_close()  # seems like it is not necessary to call a function to close the stage.
        return 0

    def acquisition_mode1(self):
        """
        # [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
        # with LS3 scan.
        @return:
        """
        self._acquisition_looping_order_p_v_c_s(
                                           daq_configs_gclass=NIDAQDevicesConfigsGeneratorMode1,
                                           cam_configs_gclass=CameraConfigsGeneratorMode1,
                                           sta_configs_gclass=StageConfigsGeneratorMode1)
        # eventually have to refactor all these with dependency injection.
        print("stepped out of AcquisitionFacilitator.acquisition_mode1")

    def acquisition_mode7(self):
        """
        this will be acquisition mode 7 - which is mode1 with O1 scan, (mode1 is using LS3 scan).
        @return:

        [mode 7] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice] - [scan: O1]

        now think about the event triggering strategy - Jan 26, 2023. xiyu.
        1. first, the camera cannot be waiting for a asi stage trigger, it has to be a separate trigger
        2. O1 voltages has to be a step function.
        3. camera output trigger still needs to be used to trigger the DAQ suits (for light sheet sweeping and so on).
        4. the voltage to set the O1 stage position needs to be settled before the frame acquisition begines, and when
           the camera output trigger arrives, the O1 needs to stay static. So O1 move to desired position during the
           readout time of the "last frame". Basically, all the daq devices need to get ready during the "read out time"
           of the last frame.
           after each slice, the daq card should stop-rewrite-start again - yes? think about it for a while. rewrite is
           required if a single cycle covers the period of one slice instead of one stack, and O1 voltage
           needs to be updated - but what if we put the full cycle to be the first camera trigger? (no, there will be
           synchronization issue with the camera since the camera start time is not precise.) - ok, stop-rewrite-start
           is necessary.

           need to test the response time for the stop-rewrite-start cycle for the daq devices.

           this means for O1 scan, we have to tolerate low speed. O1 is heavy anyhow and the stage stabilization takes
           time anyhow, so that's fine.

        5. Perhaps to capture the piezo-stage-is-stable signal and use that as the master trigger. write in a way that
           allows for this upgrade.

        option 1 - 1 cycle = 1 slice, 1 daq chasis
            run the camera at master pulse start trigger mode and set large intervals and leave enough "resting" time
            after each exposure time for each frame.
            and after each frame, stop-rewrite-start the daq card cycle again.
            dangers:
                1. daq stop-rewrite-start may not catch up with the next exposure time.
                In this case - you miss a camera trigger - and you get a dark frame, and the desired slice will come
                in the next frame that has correct signal - which is fine. - mitigation - remove dark frames. OK for
                static sample.
                2. when the daq starts, the exposure trigger comes too early - and the movement haven't settled yet.
                This will give wrong signal - think about it. - mitigation - set really long read out time so this event
                does not happen.

                the daq stop-rewrite-start signal should be triggered by what?
                even assuming it is triggered properly, will O1 move to the desired position in time? It has to be already there.
                is there an initialization state that we can issue?

                daq runs a cycle, then it stops, then it runs again.

                think about when to tell daq card to stop? when counter increase 1, wait for exposure time +
                fraction buffer time, save the frame, then stop-rewrite-restart     All these needs to finish before the
                next camera trigger.

        option 2: 1 cycle = 1 slice, 2 daq chasis
            run a separate c-daq card to control O1.
            this should be the most reliable solution. you can even implment a channel to trigger the next chasis.
            or maybe use a raspbery pi at the low cost range.

        option 3: 1 cycle = full stack 1 daq chassis
            everything is static so it can be implemented with certain buffer for uncertainty.
            imperfection arises with the imperfection of the master pulse time. check the reliabiitliy of that.
            danger: motion of strip-reduction galvo may generate artifacts - either match it with exposure time, or
            have it run much faster than exposure time. or have it operate in a time window wider than the exposure time?
            no, just run it much faster than the exposure time.
            just make the daq card duty cycle slightly wider than the exposure time window, and extend on both ends.
            think about it for a while.

        OK, try option 3 first.
        option 3 - specifics.
            the camera runs in a master pulse start trigger mode (same as mode 1)
            the counter will count the number of frames to decide when a stack ends (same as mode 1)
            the daq will stop-rewrite-start the daq card after each stack. (same as mode 1)
            daq configuration swill be different from mode 1:
                it won't be triggered by the camera output triggers.
                it may or may not be retriger-able and it doesn't matter, because there will only be 1 duty cycle.
                the voltages are generated for the full stack before the stack acquisition begins.
            Now think about:
                What is the start trigger for the camera?
                    use an external trigger start mode. and make a super short asi-stage-scan trigger perhaps to be the
                    camera trigger. The first frame won't be used.
                What is the start trigger for the daq card?
                    may still use the camera frame output trigger, and for the first frame, make it dark.
            need to record the trigger signals on the oscilloscope for confirmation.
            OK, proceed with these specifics.
            the daq will ignore early triggers if the cycle is not finished yet, so that's good.
            the triggering wiring do not need to change.


        """
        self._acquisition_looping_order_p_v_c_s(
                                           daq_configs_gclass=NIDAQDevicesConfigsGeneratorMode7,
                                           cam_configs_gclass=CameraConfigsGeneratorMode7,
                                           sta_configs_gclass=StageConfigsGeneratorMode7)
        print("stepped out of AcquisitionFacilitator.acquisition_mode7")
        return 0
