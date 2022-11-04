from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_mode1 import \
    NIDAQDevicesConfigsGeneratorMode1
from daxi.ctr_devicesfacilitator.nidaq.nidaq import SubTaskAO


class InspectionFcltr:
    """
    AcquisitionFcltr perfroms at the level of a focused process facilitator. it is a command when invoked by the
    client(ProcessesFcltr) through its invoker. and this focused process facilitator shoudl be paried with two receivers
    the DevicesFcltr and the DataFcltr. Currently we are only paying attention to the DevicesFcltr. - Xiyu @ 2022-11-03

    refer to issue #3 (link below) for notes regarding the big picture of implementing this class.
    https://github.com/xiyuyi/daxi-controller/issues/3
    """
    def __init__(self):
        self.process_configs = None
        self.data_fcltr = None
        self.devices_fcltr = None
        self.status_metronome = None
        self.status_counter = None
        self.status_scanning_galvo = None
        self.status_view_switching_galvo1 = None
        self.status_view_switching_galvo2 = None
        self.status_gamma_galvo_strip_reduction = None
        self.status_beta_galvo_lightsheet_incident_angle = None
        self.status_405_laser = None
        self.status_488_laser = None
        self.status_561_laser = None
        self.status_639_laser = None
        self.status_bright_field = None
        self.status_O1 = None
        self.status_O3 = None
        self.status_filter_wheel = None
        self.status_water_dispenser = None
        self.status_serial_placeholder = None
        self.status_camera_placeholder = None

    def execute(self, devices_fcltr=None, data_fcltr=None, process_configs=None):
        self.devices_fcltr = devices_fcltr
        self.data_fcltr = data_fcltr
        self.process_configs = process_configs
        if self.process_configs['process type'] == 'inspection, inspect_metronome':
            self.inspect_metronome()

        if self.process_configs['process type'] == 'inspection, inspect_counter':
            self.inspect_counter()

        if self.process_configs['process type'] == 'inspection, inspect_scanning_galvo':
            self.inspect_scanning_galvo()

        if self.process_configs['process type'] == 'inspection, inspect_view_switching_galvo1':
            self.inspect_view_switching_galvo1()

        if self.process_configs['process type'] == 'inspection, inspect_view_switching_galvo2':
            self.inspect_view_switching_galvo2()

        if self.process_configs['process type'] == 'inspection, inspect_gamma_galvo_strip_reduction':
            self.inspect_gamma_galvo_strip_reduction()

        if self.process_configs['process type'] == 'inspection, inspect_beta_galvo_lightsheet_incident_angle':
            self.inspect_beta_galvo_lightsheet_incident_angle()

        if self.process_configs['process type'] == 'inspection, inspect_405_laser':
            self.inspect_405_laser()

        if self.process_configs['process type'] == 'inspection, inspect_488_laser':
            self.inspect_488_laser()

        if self.process_configs['process type'] == 'inspection, inspect_561_laser':
            self.inspect_561_laser()

        if self.process_configs['process type'] == 'inspection, inspect_639_laser':
            self.inspect_639_laser()

        if self.process_configs['process type'] == 'inspection, inspect_bright_field':
            self.inspect_bright_field()

        if self.process_configs['process type'] == 'inspection, inspect_O1':
            self.inspect_O1()

        if self.process_configs['process type'] == 'inspection, inspect_O3':
            self.inspect_O3()

        if self.process_configs['process type'] == 'inspection, inspect_filter_wheel':
            self.inspect_filter_wheel()

        if self.process_configs['process type'] == 'inspection, inspect_water_dispenser':
            self.inspect_water_dispenser()

        if self.process_configs['process type'] == 'inspection, inspect_serial_placeholder':
            self.inspect_serial_placeholder()

        if self.process_configs['process type'] == 'inspection, inspect_camera_placeholder':
            self.inspect_camera_placeholder()

        return 0

    def inspect_metronome(self):
        """
        make sure it can generate reasonable number of ticks.
        should measure with oscilloscope and physically check.
        it should configure everything on the device configurator where only append 1 ao task and start it.
        should modify the device fcltr to not start ao/do task if no subtasks are attached.
        :return:
        """
        print('AcquisitionFcltr - this will inspect metronome')
        self.devices_fcltr.receive_device_configs_all_cycles(
                                    process_configs=self.process_configs,
                                    device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
        first_cycle_key = next(iter(self.devices_fcltr.configs_single_cycle_dict))
        self.devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                                         verbose=True)

        # 3. prepare metronome
        self.devices_fcltr.daq_prepare_metronome()

        # 4. get ready, start, stop and close the metronome.
        self.devices_fcltr.metronome.get_ready()
        self.devices_fcltr.metronome.start()
        self.devices_fcltr.metronome.stop()
        self.devices_fcltr.metronome.close()

        self.status_metronome = 'good'
        return 0

    def inspect_counter(self):
        print('AcquisitionFcltr - this will inspect counter')
        self.status_counter = 'good'
        return 0

    def inspect_scanning_galvo(self):
        print('AcquisitionFcltr - this will inspect scanning galvo')
        # 0.  checkout a devices facilitator (already passed in by the command)
        # 1. receive configurations and checkout a singel configuration.
        self.devices_fcltr.receive_device_configs_all_cycles(
            process_configs=self.process_configs,
            device_configs_generator_class=NIDAQDevicesConfigsGeneratorMode1)
        first_cycle_key = next(iter(self.devices_fcltr.configs_single_cycle_dict))
        self.devices_fcltr.checkout_single_cycle_configs(key=first_cycle_key,
                                                         verbose=True)

        # 2. prepare the SG as an ao subtask
        config = getattr(self.devices_fcltr, 'configs_scanning_galvo')
        self.devices_fcltr.subtask_ao_configs_list = [config]
        st = SubTaskAO(config)
        if st.data is None:
            st.generate_data()
        self.devices_fcltr.subtask_ao_list = [st]

        # 3. prepare metronome
        self.devices_fcltr.daq_prepare_metronome()

        # 4. prepare AO task bundle
        self.devices_fcltr.daq_prepare_taskbundle_ao()

        # 5. add metronome to the ao task bundle
        self.devices_fcltr.taskbundle_ao.add_metronome(self.devices_fcltr.metronome)

        # 6. add sub-tasks for ao task bundle
        self.devices_fcltr.daq_add_subtasks_ao()

        # 7. get ready, start, stop and close
        self.devices_fcltr.taskbundle_ao.get_ready()
        self.devices_fcltr.metronome.get_ready()

        self.devices_fcltr.taskbundle_ao.stop()
        self.devices_fcltr.metronome.stop()

        self.devices_fcltr.taskbundle_ao.close()
        self.devices_fcltr.metronome.close()


        self.status_scanning_galvo = 'good'
        return 0

    def inspect_view_switching_galvo1(self):
        print('AcquisitionFcltr - this will inspect view switching galvo 1')
        self.status_view_switching_galvo1 = 'good'
        return 0

    def inspect_view_switching_galvo2(self):
        print('AcquisitionFcltr - this will inspect view switching galvo 2')
        self.status_view_switching_galvo2 = 'good'
        return 0

    def inspect_gamma_galvo_strip_reduction(self):
        print('AcquisitionFcltr - this will inspect gamma galvo strip reduction')
        self.status_gamma_galvo_strip_reduction = 'good'
        return 0

    def inspect_beta_galvo_lightsheet_incident_angle(self):
        print('AcquisitionFcltr - this will inspect beta galvo light sheet incident angle')
        self.status_beta_galvo_lightsheet_incident_angle = 'good'
        return 0

    def inspect_405_laser(self):
        print('AcquisitionFcltr - this will inspect 405 laser')
        self.status_405_laser = 'good'
        return 0

    def inspect_488_laser(self):
        print('AcquisitionFcltr - this will inspect 488 laser')
        self.status_488_laser = 'good'
        return 0

    def inspect_561_laser(self):
        print('AcquisitionFcltr - this will inspect 561 laser')
        self.status_561_laser = 'good'
        return 0

    def inspect_639_laser(self):
        print('AcquisitionFcltr - this will inspect 639 laser')
        self.status_639_laser = 'good'
        return 0

    def inspect_bright_field(self):
        print('AcquisitionFcltr - this will inspect bright field')
        self.status_bright_field = 'good'
        return 0

    def inspect_O1(self):
        print('AcquisitionFcltr - this will inspect O1')
        self.status_O1 = 'good'
        return 0

    def inspect_O3(self):
        print('AcquisitionFcltr - this will inspect O3')
        self.status_O3 = 'good'
        return 0

    def inspect_filter_wheel(self):
        print('AcquisitionFcltr - this will inspect filter wheel')
        self.status_filter_wheel = 'good'
        return 0

    def inspect_water_dispenser(self):
        print('AcquisitionFcltr - this will inspect water dispenser')
        self.status_water_dispenser = 'good'
        return 0

    def inspect_serial_placeholder(self):
        print('AcquisitionFcltr - this will inspect serial devices [placeholder]')
        self.status_serial_placeholder = 'good'
        return 0

    def inspect_camera_placeholder(self):
        print('AcquisitionFcltr - this will inspect camera [place holder]')
        self.status_camera_placeholder = 'good'
        return 0

