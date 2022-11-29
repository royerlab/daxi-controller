from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from daxi.control.device.facilitator.nidaq.nidaq import Metronome, TaskBundleAO, TaskBundleDO, SubTaskAO, SubTaskDO


class DevicesFcltr:
    """

    this is a receiver -- in the pattern for cli/gui, process facilitators and configurations.

    Think about the role of a device facilitator (it's the receiver, receives command from a focused process fcltr.)

    it will take the configuration from an overal panel, or a template. (that's the client)

    it will then perform the 8 step tasks for all the devices. (the receiver executes the process)

    Now for daq, there are 10 steps, and should be included in all child classes of the Device Facilitators.
    the command will use the methods in the receiver, through the receiver, to orchestrates the tasks. so the execute
    steps composition happens in the focused process facilitators.

    the receiver contains all the methods (things they can do and they know how to do), and the command (focused
    process facilitator) uses them through the receiver for the specific process.

    """

    def __init__(self, devices_connected=True):
        self.devices_connected = devices_connected
        self.description = "This is the devices facilitator for DaXi microscope"
        self.subtask_ao_list = []
        self.subtask_ao_configs_list = []
        self.subtask_do_list = []
        self.subtask_do_configs_list = []
        self.metronome = None
        self.devices_and_tools_collection = None
        self.taskbundle_ao = None
        self.taskbundle_do = None
        self.configs_all_cycles = {}
        self.configs_metronome = None
        self.configs_counter = None
        self.configs_AO_task_bundle = None
        self.configs_DO_task_bundle = None
        self.configs_scanning_galvo = None
        self.configs_view_switching_galvo_1 = None
        self.configs_view_switching_galvo_2 = None
        self.configs_gamma_galvo_strip_reduction = None
        self.configs_beta_galvo_light_sheet_incident_angle = None
        self.configs_405_laser = None
        self.configs_488_laser = None
        self.configs_561_laser = None
        self.configs_639_laser = None
        self.configs_bright_field = None
        self.configs_O1 = None
        self.configs_O3 = None
        self.configs_single_cycle_dict = None

    def load_device_configs_one_cycle(self, device_configs_file, verbose=True):
        """
        It will take the configs_path as an input parameter, and load in all the configurations.
        Parameters
        load from the device_configs path
        it will populate the following attributes for itself:
        self.devices_and_tools_collection
        self.configs_*specific_devices_and_tools
        ----------
        configs_path

        Returns
        -------

        """
        # parse the configurations
        # set up the parser
        p = NIDAQConfigsParser()
        p.set_configs_path(device_configs_file)
        # retrieve the complete list of devices and tools
        self.devices_and_tools_collection = \
            p.get_configs_by_path_section_keyword(section='Content Section',
                                                  keyword="all_tools_and_devices",
                                                  verbose=verbose)
        # parse the configurations of all the devices and tools from all sessions based on the colleciton
        for session in self.devices_and_tools_collection.keys():
            for device_tool in self.devices_and_tools_collection[session]:
                # retrieve the configurations
                configs = p.get_configs_by_path_section_keyword(
                    section=session,
                    keyword=device_tool,
                    verbose=verbose
                )
                # assign the attributes
                setattr(self, 'configs_' + device_tool, configs)

    def receive_device_configs_all_cycles(self, process_configs, device_configs_generator_class):
        """

        :param device_configs_generator_class: the class for device generator
        :param process_configs: dict. It should be passed in by a command - a FocusedProcessFcltr type.
        (leave abstraction for future for now.)
        this should do things equivalent to load_device_configs, but instead of doing it from loading things from file,
        it receive from outside the dictionary - device_configs.
        # pay attention to the difference between process_configs and devices configs.
        #todo implement the specifics.
        doubl echeck and makes ure the device configuration generators generates the correct devices configs as done
        in the load* function shown above.

        there is process_configs, devices_configs, single_view_devices_configs
        in this method, we receive a process_configs, a device_configs_generator.
        we have to break it down into devices_configs, then break it down
        into single_view_devices_configs, then generate the specific configs.
        maybe the device configs generator class should break it down into single view configs generator.

        the focused acquisiton fcltr should tell the device fcltr to map different sets of configurations, and tell the
        devicesfcltr to update data without closing all devices. One cycle should be one pair of indexs that specifies
        [light source index, view index].

        think about what to receive in devicesfcltr, and how to do the update. all cycle will have all devices, and
        mapping will be (blocking unused light source to be all off through out the sequence, and map the corresponding
        view index, or synthesis based on the basic sequence through extension of metronome sequences, data, etc.)
        For mode 1, we do picking and blocking. (so this requires awareness of acquisition mode specifics).
        so perhaps this should be done by the process manager).

        Should cycle mapping be done in devicesfcltr, or focused acquisition process fcltr? think about it.
        if it is done in devicesfcltr: advantage is all deviced configurations are at the device level... disadvantage
        is that hte device facilitator need to understand different focused acquisition processes.
        if it is done in the focused acquisition process fcltr, then this fcltr has to understand a bit on the data
        configuraitons.
        OK it makes more sense to have it in the focused processes fcltr.

        :return: nothing
        """
        # synthesize the configurations - process_parameter
        process_parameters = process_configs['process configs']['acquisition parameters']

        # synthesize the configurations - daq_terminal_configs
        daq_terminal_configs = process_configs['device configurations']['nidaq_terminals']

        # synthesize the configurations - calibration_records
        calibration_records = process_configs['device configurations']['calibration_records']

        # synthesize the configurations - alignment_records
        alignment_records = process_configs['device configurations']['alignment_records']

        # now get the configuration generator
        configs_generator = \
            device_configs_generator_class(params=process_parameters,
                                           nidaq_terminals=daq_terminal_configs,
                                           calibration_records=calibration_records,
                                           alignment_records=alignment_records)

        # now generate all device configurations
        self.configs_all_cycles['configs_metronome'] = \
            configs_generator.get_configs_for_metronome()
        self.configs_all_cycles['configs_counter'] = \
            configs_generator.get_configs_for_counter()
        self.configs_all_cycles['configs_DO_task_bundle'] = \
            configs_generator.get_configs_do_task_bundle()
        self.configs_all_cycles['configs_AO_task_bundle'] = \
            configs_generator.get_configs_ao_task_bundle()
        self.configs_all_cycles['configs_scanning_galvo'] = \
            configs_generator.get_configs_scanning_galvo(params=process_parameters)
        self.configs_all_cycles['configs_view_switching_galvo_1'] = \
            configs_generator.get_configs_view_switching_galvo_1(params=process_parameters)
        self.configs_all_cycles['configs_view_switching_galvo_2'] = \
            configs_generator.get_configs_view_switching_galvo_2(params=process_parameters)
        self.configs_all_cycles['configs_gamma_galvo_strip_reduction'] = \
            configs_generator.get_configs_gamma_galvo_strip_reduction(params=process_parameters)
        self.configs_all_cycles['configs_beta_galvo_light_sheet_incident_angle'] = \
            configs_generator.get_configs_beta_galvo_light_sheet_incident_angle(process_parameters)
        self.configs_all_cycles['configs_O1'] = \
            configs_generator.get_configs_o1(process_parameters)
        self.configs_all_cycles['configs_O3'] = \
            configs_generator.get_configs_o3(process_parameters)
        self.configs_all_cycles['configs_405_laser'] = \
            configs_generator.get_configs_405_laser(process_parameters)
        self.configs_all_cycles['configs_488_laser'] = \
            configs_generator.get_configs_488_laser(process_parameters)
        self.configs_all_cycles['configs_561_laser'] = \
            configs_generator.get_configs_561_laser(process_parameters)
        self.configs_all_cycles['configs_639_laser'] = \
            configs_generator.get_configs_639_laser(process_parameters)
        self.configs_all_cycles['configs_bright_field'] = \
            configs_generator.get_configs_bright_field(process_parameters)
        # all the configurations are mapped to a dictionary that stores different cycle types,
        # specified by its own dictionary keys with acquisition-mode specific name patterns.
        self.configs_single_cycle_dict = \
            configs_generator.get_configs_single_cycle_dict(process_parameters)

    def checkout_single_cycle_configs(self, key=None, verbose=False):
        if verbose:
            print('          checking out a single  cycle configuration for '+str(key))
        configs = self.configs_single_cycle_dict[key]
        # now map all the attributes in configs into this object
        for k in configs.keys():
            setattr(self, k, configs[k])

    def show_devices_configs(self):
        """
        print out the names of the devices for convenience
        :return:
        """
        for m in self.__dict__.keys():
            if m.startswith('configs_'):
                n = getattr(self, m)
                if 'data generator' in n:
                    print(m + ": " + n['task type'] + ',  data generator:' + n['data generator'])
                else:
                    print(m + ": " + n['task type'])

    def daq_prepare_metronome(self):
        """
        prepare the metronome for the device.
        Returns
        -------

        """
        self.metronome = Metronome(devices_connected=self.devices_connected)
        self.metronome.set_configurations(self.configs_metronome)

    def daq_prepare_counter(self):
        """
        prepare a counter for the device.
        Returns
        -------

        """
        pass

    def daq_prepare_taskbundle_ao(self):
        """
        prepare the TaskBundleAO object
        Returns
        -------

        """
        self.taskbundle_ao = TaskBundleAO(devices_connected=self.devices_connected)
        self.taskbundle_ao.set_configurations(self.configs_AO_task_bundle)

    def daq_prepare_subtasks_ao(self):
        """
        prepare all the subtasks for ao channels, store in a subtasks list
        Returns
        -------

        """
        # 1. make a list of AO subtasks configurations.
        self.subtask_ao_configs_list = []
        for key in self.__dict__.keys():
            if key.startswith('configs_'):
                config = getattr(self, key)
                if config is not None and 'task type' in config.keys():
                    if config['task type'] == 'AO subtask':
                        self.subtask_ao_configs_list.append(config)

        # 2. make the subtasks objects, and generate data for each one of them.
        for st_configs in self.subtask_ao_configs_list:
            st = SubTaskAO(st_configs)
            if st.data is None:
                st.generate_data()  # todo - now this data generator is used in the receiving method. organize it.
            self.subtask_ao_list.append(st)

    def daq_prepare_taskbundle_do(self):
        """
        prepare the TaskBundleDO object
        Returns
        -------

        """
        self.taskbundle_do = TaskBundleDO(devices_connected=self.devices_connected)
        self.taskbundle_do.set_configurations(self.configs_DO_task_bundle)
        pass

    def daq_prepare_subtasks_do(self):
        """
        prepare all the subtasks for do channels, store in a subtasks list
        Returns
        -------

        """
        # 1. make a list of AO subtasks
        self.subtask_do_configs_list = []
        for key in self.__dict__.keys():
            if key.startswith('configs_'):
                config = getattr(self, key)
                if config is not None and 'task type' in config.keys():
                    if config['task type'] == 'DO subtask':
                        self.subtask_do_configs_list.append(config)

        # 2. make the subtasks objects, and generate data for each one of them.
        for st_configs in self.subtask_do_configs_list:
            st = SubTaskDO(st_configs)
            if st.data is None:
                st.generate_data()  # todo - now this data generator is used in the receiving method. organize it.
            self.subtask_do_list.append(st)

    def daq_check_compatibility(self):
        """
        test the wiring checking of AObundle and make sure it is working as expected.
        it should report error when the AObundle wiring is wrong
        it should suggest re-wiring options when wrong wiring is detected
        it should report that the AObundle wiring is correct when everything is correct
        it should generate the inspectable elements that can be used to generate wiring diagram.
        :return:
        """
        # todo

    def daq_add_metronome(self):
        """
        add metronome to ao taskbundle
        :return:
        """
        self.taskbundle_ao.add_metronome(self.metronome)
        self.taskbundle_do.add_metronome(self.metronome)

    def daq_add_subtasks_ao(self):
        """
        add subtasks_ao to ao taskbundle
        :return:
        """
        for st in self.subtask_ao_list:
            self.taskbundle_ao.add_subtask(st)

    def daq_add_subtasks_do(self):
        """
        add subtasks_do to do taskbundle
        :return:-
        """
        for st in self.subtask_do_list:
            self.taskbundle_do.add_subtask(st)

    def daq_get_ready(self):
        """
        all the devices get ready.
        Returns
        -------

        """
        self.taskbundle_ao.get_ready()
        self.taskbundle_do.get_ready()
        self.metronome.get_ready()
        # todo add counter channels.

    def daq_start(self):
        """
        start the operations
        Returns
        -------

        """
        self.metronome.start()
        self.taskbundle_ao.start()
        self.taskbundle_do.start()
        # todo add counter channels.

    def daq_stop(self):
        """
        stop the operations
        Returns
        -------

        """
        self.taskbundle_ao.stop()
        self.taskbundle_do.stop()
        self.metronome.stop()
        # todo add counter channels.

    def daq_close(self):
        """
        close all devices
        Returns
        -------

        """
        self.taskbundle_ao.close()
        self.taskbundle_do.close()
        self.metronome.close()
        # todo add counter channels.

    def daq_update_data(self):
        """
        close all devices
        Returns
        -------

        """
        self.taskbundle_ao.update_data()
        self.taskbundle_do.update_data()
        # todo add counter channels.

    def daq_write_data(self):
        """
        close all devices
        Returns
        -------

        """
        self.taskbundle_ao.write_data()
        self.taskbundle_do.write_data()
        # self.metronome.write_data()
        # todo add counter channels.

    def serial_placeholder(self):
        """
        there should be a series of actions corresponds to serial ports.
        Returns
        -------

        """

    def serial_move_filter_wheel(self, color):
        """
        should implement this in the future....
        start by looking in old_workbench asistage serialpot.py or something...

        # todo - should implement move filter wheel...
        OK now start to see the logic of the "empty skeleton" like style in coPylot :P

        :param color:
        :return:
        """
        print("          Move Filter Wheel: we will move the filter wheel to the following color: "+str(color))
        # need to have a configuration file of filters in the configs.
        pass

    def direct_device_placeholder(self):
        """
        There should be a series of actions corresponds to serial ports.
        Returns
        -------

        """

    def camera_start(self):
        print("          this will start the camera, leave it out for now. will implement in the future.")
        pass

    def stage_start(self):
        print("          this will start the stage, leave it out for now. will implement in the future.")
        pass

    def camera_stop(self):
        print("          this will stop the camera, leave it out for now. will implement in the future.")
        pass

    def stage_stop(self):
        print("          this will stop the stage, leave it out for now. will implement in the future.")
        pass

    def camera_close(self):
        print("          this will close the camera, leave it out for now. will implement in the future.")
        pass

    def stage_close(self):
        print("          this will close the stage, leave it out for now. will implement in the future.")
        pass
