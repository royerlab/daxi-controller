"""
This facilitator should interact with the main gui, comsolidate all the configurations and send it to
the device and data tools facilitators.
"""
import copy
import os
from time import sleep

import numpy as np
# from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
#     NIDAQDevicesConfigsGeneratorMode1
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1, CameraConfigsGeneratorMode1, StageConfigsGeneratorMode1
from daxi.control.device.facilitator.config_tools.configuration_generator_mode7 import \
    NIDAQDevicesConfigsGeneratorMode7, CameraConfigsGeneratorMode7, StageConfigsGeneratorMode7
from daxi.control.device.facilitator.devicesfacilitator import prepare_all_devices_and_get_ready
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected
from matplotlib import pyplot as plt

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

    def _crop_data_setment(self, data_list, index_start, index_end):
        """
        thi smethod takes a list of data sequences, and crop the sequences from index_start to index_end
        and generate a new data list with the cropped data sequences.
        :param data_list:
        :param index_start:
        :param index_end:
        :return:
        """
        output = []
        for data_sequence in data_list:
            output.append(data_sequence[index_start:index_end])
        return output

    def _update_data_for_all_ao(self, ind, d):
        self.devices_fcltr.subtask_ao_configs_list[ind]['data'] = d
        self.devices_fcltr.subtask_ao_list[ind] = d
        self.devices_fcltr.taskbundle_ao.data_list[ind] = d

    def _update_data_for_all_do(self, ind, d):
        self.devices_fcltr.subtask_do_configs_list[ind]['data'] = d
        self.devices_fcltr.subtask_do_list[ind] = d
        self.devices_fcltr.taskbundle_do.data_list[ind] = d

    def _prepare_acquisition_for_one_stack(self, view, color):
        """
        This will get the devices started and wait for the trigger to start acquisition.

        :param view:
        :param color:
        :return:
        """
        # move the filter wheel.
        self.devices_fcltr.serial_move_filter_wheel(color)

        # based on the view and color indexes, choose a daq data cycle index. (This is
        # actually implemented in DevicesFcltr)
        cycle_key = 'view' + str(view) + ' color' + str(color)  # get the cycle key for this cycle
        self.devices_fcltr.checkout_single_cycle_configs(key=cycle_key, verbose=True)

        # then map the data to the ao do task bundles
        # update the data fiels in subtask_ao_configs_list, and subtask_ao, and taskbundle_ao
        for ind, a in enumerate(self.devices_fcltr.subtask_ao_configs_list):
            if a['device'] == 'scanning_galvo':
                d = copy.deepcopy(self.devices_fcltr.configs_scanning_galvo['data'])
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'view switching galvo 1':
                d = self.devices_fcltr.configs_view_switching_galvo_1['data']
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'view switching galvo 2':
                d = self.devices_fcltr.configs_view_switching_galvo_2['data']
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'gamma galvo':
                d = self.devices_fcltr.configs_gamma_galvo_strip_reduction['data']
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'beta galvo':
                d = self.devices_fcltr.configs_beta_galvo_light_sheet_incident_angle['data']
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'O1':
                d = self.devices_fcltr.configs_O1['data']
                self._update_data_for_all_ao(ind, d)

            if a['device'] == 'O3':
                d = self.devices_fcltr.configs_O3['data']
                self._update_data_for_all_ao(ind, d)

        # update the data fiels in subtask_do_configs_list, and subtask_do, and taskbundle_do
        for ind, a in enumerate(self.devices_fcltr.subtask_do_configs_list):
            if a['device'] == '405-laser':
                d = self.devices_fcltr.configs_405_laser['data']
                self._update_data_for_all_do(ind, d)

            if a['device'] == '488-laser':
                d = self.devices_fcltr.configs_488_laser['data']
                self._update_data_for_all_do(ind, d)

            if a['device'] == '561-laser':
                d = self.devices_fcltr.configs_561_laser['data']
                self._update_data_for_all_do(ind, d)

            if a['device'] == '639-laser':
                d = self.devices_fcltr.configs_639_laser['data']
                self._update_data_for_all_do(ind, d)

            if a['device'] == 'bright-field':
                d = self.devices_fcltr.configs_bright_field['data']
                self._update_data_for_all_do(ind, d)

        return 0

    def _acquisition_for_one_stack_identical_daqv_across_frames(self):
        """
        This method implements the acquisition routine where the stack voltages for every exposure time is the same,
        DAQ data do not get updated across the entire stack.

        :return:
        """
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
        counter_pre = 0
        counter = 0
        os.system('echo single stack acquisition starts ...')
        while counter <= self.configs['process configs']['acquisition parameters']['n slices']:
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

    def _acquisition_for_one_stack_different_daqv_across_frames_static_sample_stage(self):
        """
        This method implements the acquisition routine where the stack voltages for every exposure time are updated each
        time after the exposure (during the readout time of the frame). the daq card is stopped, updated, re-write, and
        will be triggered by the next camera output trigger.

        :return:
        """
        # first, because calculatign the daq profiles takes time, we only want to calculate it once and we dont want to
        # perform the calculation every frame. So we will start from already clacualted data, and the data is stored in
        # the sequences for the entire stack.
        # now we want to write data to the card with data only for this frame, so we take out the segment and write
        # to daq
        # update and write data to daq card for the current cycle index.
        # change the data of the subtasks for both AO and DO, then update/write

        # find out the index of the data segment.
        index_start = 0
        cycle_sample_number = self.devices_fcltr.configs_all_cycles['configs_daq_general']['on-duty sample number'] + \
                              self.devices_fcltr.configs_all_cycles['configs_daq_general']['off-duty sample number']
        index_end = cycle_sample_number


        self.devices_fcltr.taskbundle_ao.data_list = \
            self._crop_data_setment(self.ao_data_list, index_start, index_end)
        self.devices_fcltr.taskbundle_do.data_list = \
            self._crop_data_setment(self.do_data_list, index_start, index_end)

        # now write data to daq card
        self.devices_fcltr.daq_write_data()

        # start daq card (waiting for the trigger from the camera)
        self.devices_fcltr.daq_start()

        # start camera (In this mode, the camera should be configured for software trigger)
        assert self.devices_fcltr.configs_camera['master pulse trigger'] == 'SOFTWARE'
        self.devices_fcltr.camera_start()

        # loop over slices for the stack:
        frame_number = 0
        counter = 0
        os.system('echo single stack acquisition starts ...')
        while frame_number < self.configs['process configs']['acquisition parameters']['n slices'] - 1:
            # trap the process in this while-loop until the counter reaches the desired count.
            counter = self.devices_fcltr.counter.read()
            # print('c1 - counter read: ' + str(counter) + ', frame_number:' + str(frame_number))
            if counter is None:
                counter = 0

            if counter > 0:
                # that means the camera frame has increased one, now need to prepare everything for the next frame
                frame_number = frame_number + 1  # and frame number incretes by one.
                print('c2 - counter read: ' + str(counter) + ', frame_number :' + str(frame_number))
                # wait for two frame cycles
                sleep(self.devices_fcltr.configs_camera['master pulse interval'])
                # stop daq card, update daq voltages and start again.
                self.devices_fcltr.daq_stop()

                index_start = frame_number*cycle_sample_number
                index_end = index_start + cycle_sample_number
                print('indexes is from ' + str(index_start) + ' to ' +str(index_end))
                self.devices_fcltr.taskbundle_ao.data_list = \
                    self._crop_data_setment(self.ao_data_list, index_start, index_end)
                self.devices_fcltr.taskbundle_do.data_list = \
                    self._crop_data_setment(self.do_data_list, index_start, index_end)
                print('data length is ' + str(len(self.devices_fcltr.taskbundle_do.data_list[0])))
                self.devices_fcltr.daq_write_data()
                self.devices_fcltr.daq_start()
                counter = None
            counter = self.devices_fcltr.counter.read()

        os.system('echo counted number of slices: ' + str(counter))
        # stop(pause) daq card
        # wait for two frame cycles
        sleep(self.devices_fcltr.configs_camera['master pulse interval']*2)
        self.devices_fcltr.daq_stop()
        self.devices_fcltr.camera_stop()

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
        position_list, view_list, color_list, number_of_time_points, slice_number = \
            self._convinience_reasign_params()

        self._msg_2(verbose=self.verbose)

        prepare_all_devices_and_get_ready(devices_fcltr=self.devices_fcltr, is_simulation=is_simulation)

        # loop over time points
        for time_point_index in np.arange(number_of_time_points):
            self._msg_3(verbose=self.verbose)

            # loop over positions
            for position in position_list:
                self._msg_4(position=position, verbose=self.verbose)

                # move the stage to the position
                print('now move to position: '+ position)
                self.devices_fcltr.stage_move_to(position)

                # ASI stage get ready at the position (this line has to be here due to mode1 specifics)
                self.devices_fcltr.stage_raster_scan_get_ready_at_position(position_name=position)

                # loop over views.
                for view in view_list:
                    os.system('echo --- going to this view: view' + str(view))

                    # loop over colors.
                    for color in color_list:
                        os.system('echo --- --- switching to this color: color' + str(color))
                        os.system('echo --- --- --- current: time point: ' + str(time_point_index) +
                                  ', position: ' + str(position) + ', view' + str(view) + ', color' + str(color))

                        self._prepare_acquisition_for_one_stack(view, color)
                        self.ao_data_list = copy.deepcopy(self.devices_fcltr.taskbundle_ao.data_list)
                        self.do_data_list = copy.deepcopy(self.devices_fcltr.taskbundle_do.data_list)

                        if self.configs['process configs']['process type'] == 'acquisition, mode 1':
                            self._acquisition_for_one_stack_identical_daqv_across_frames()

                        if self.configs['process configs']['process type'] == 'acquisition, mode 7':
                            self._acquisition_for_one_stack_different_daqv_across_frames_static_sample_stage()

                        os.system('echo single stack acquisition ends.')
                        os.system('echo .')

        # wait for two frame cycles
        sleep(self.devices_fcltr.configs_camera['master pulse interval'] * 2)
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
