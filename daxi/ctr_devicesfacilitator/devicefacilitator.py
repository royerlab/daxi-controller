from daxi.globals_configs_constants_general_tools.parser import NIDAQConfigsParser
from daxi.ctr_devicesfacilitator.nidaq.nidaq import Metronome, TaskBundleAO, TaskBundleDO, SubTaskAO, SubTaskDO


class DevicesFcltr:
    """

    Think about the role of a device facilitator
    it will take the configuration from an overal panel, or a template.
    it will then perform the 8 step tasks for all the devices.
    Now for daq, there are 10 steps, and should be included in all child classes of the Device Facilitators.

    """
    def __init__(self):
        self.description = "This is the devices facilitator for DaXi microscope"
        self.subtask_ao_list = []
        self.subtask_ao_configs_list = []
        self.subtask_do_list = []
        self.subtask_do_configs_list = []
        self.metronome = None
        self.devices_and_tools_collection = None
        self.taskbundle_ao = None
        self.configs_metronome = None
        self.configs_counter = None
        self.configs_AO_task_bundle = None
        self.configs_DO_task_bundle = None
        self.configs_scanning_galvo = None
        self.configs_view_switching_galvo_1 = None
        self.configs_view_switching_galvo_2 = None
        self.configs_gamma_galvo_strip_reduction = None
        self.configs_beta_galvo_light_sheet_incident_angle = None
        self.configs_O1 = None
        self.configs_O3 = None

    def load_device_configs(self, device_configs_file, verbose=True):
        """
        It will take the configs_path as an input parameter, and load in all the configurations.
        Parameters
        load from the device_configs path
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
                setattr(self, 'configs_'+device_tool, configs)

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
        self.metronome = Metronome()
        self.metronome.set_configurations(self.configs_metronome)

    def daq_prepare_counter(self):
        """
        prepare the metronome for the device.
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
        self.taskbundle_ao = TaskBundleAO()
        self.taskbundle_ao.set_configurations(self.configs_AO_task_bundle)

    def daq_prepare_subtasks_ao(self):
        """
        prepare all the subtasks for ao channels, store in a subtasks list
        Returns
        -------

        """
        # 1. make a list of AO subtasks
        self.subtask_ao_configs_list = []
        for key in self.__dict__.keys():
            if key.startswith('configs_'):
                config = getattr(self, key)
                if config['task type'] == 'AO subtask':
                    self.subtask_ao_configs_list.append(config)

        # 2. make the subtasks objects, and generate data for each one of them.
        for st_configs in self.subtask_ao_configs_list:
            st = SubTaskAO(st_configs)
            st.generate_data()         # todo - write data generators for all ao task types
            self.subtask_ao_list.append(st)

    def daq_prepare_taskbundle_do(self):
        """
        prepare the TaskBundleDO object
        Returns
        -------

        """
        self.taskbundle_do = TaskBundleDO()
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
                if config['task type'] == 'DO subtask':
                    self.subtask_do_configs_list.append(config)

        # 2. make the subtasks objects, and generate data for each one of them.
        for st_configs in self.subtask_do_configs_list:
            st = SubTaskDO(st_configs)
            st.generate_data()         # todo - write data generators for all ao task types
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

    def serial_placeholder(self):
        """
        there should be a series of actions corresponds to serial ports.
        Returns
        -------

        """

    def direct_device_placeholder(self):
        """
        There should be a series of actions corresponds to serial ports.
        Returns
        -------

        """
