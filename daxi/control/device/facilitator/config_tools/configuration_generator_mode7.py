from daxi.control.device.facilitator.config_tools.configuration_generator_base import NIDAQDevicesConfigsGeneratorBase, \
    CameraConfigsGeneratorBase, StageConfigsGeneratorBase
from daxi.control.device.facilitator.config_tools.configuration_generator_mode1 import CameraConfigsGeneratorMode1, \
    StageConfigsGeneratorMode1
from daxi.control.device.facilitator.config_tools.generate_functions import DAQDataGenerator
import numpy as np


class NIDAQDevicesConfigsGeneratorMode7(NIDAQDevicesConfigsGeneratorBase):
    """
    This class takes the acquisition parameters, and generate the configuration dictionaries for all the devices.
    This class is designed for mode1 acquisition

    the looping order for this acquisition mode is:
    [mode 7] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
    with O1 scan.

    a cycle should have the sequence of the full stack.
    all the configuration templates should be loaded in the base class.
    And the methods here is to calculate and populate up the "None" fields.
    """

    def __init__(self,
                 params=None,
                 nidaq_terminals=None,
                 calibration_records=None,
                 alignment_records=None,
                 process_configs=None,
                 verbose=False):
        super().__init__(nidaq_terminals,
                         calibration_records=calibration_records,
                         alignment_records=alignment_records,
                         process_configs=process_configs)
        self.verbose = verbose
        self._get_core_configs_for_all()

        # total number of samples
        self.sample_number_total_per_frame = np.int32(np.floor(
            params['metronome frequency'] *
            (params['exposure time (ms)'] + params['camera read out time (ms)']) / 1000
        ))

        # calculate the number of samples during camera exposure (can chase a bit longer by using np.ceil)
        self.sample_number_on_duty = np.int32(np.ceil(
            params['metronome frequency'] * (params['exposure time (ms)']) / 1000
        ))

        # calculate the number of samples during camera readout
        self.sample_number_off_duty = self.sample_number_total_per_frame - self.sample_number_on_duty

        self.slices_per_stack = params['n slices']
        self.sample_number_total = self.sample_number_total_per_frame * self.slices_per_stack

    def get_configs_for_metronome(self):
        """
        this should generate the data profile for this device, for the full cycle.
        for mode7, the full cycle is the entire stack (n frames)
        notes:
        self.slices_per_stack is the total number of slices per stack.
        self.sample_number_total_per_frame is the sampel number per image.
        self.sample_number_total is the sample number per stack.

        :param params: dictionary, the configuration parameters of all the specific device
        :param nidaq_terminals: dict. the configurations of all the wiring of daq cards for all devices.
        :return:
        """

        self.configs_metronome['number of samples'] = self.sample_number_total
        return self.configs_metronome  # write the tests to make sure there is no more None fields

    def get_configs_for_counter(self):
        self.configs_counter['initial count'] = 0
        self.configs_counter['current count'] = 0
        return self.configs_counter

    def get_configs_do_task_bundle(self):
        """
        no None fields to propagate for this device.
        :param params:
        :param nidaq_terminals:
        :return:
        """
        return self.configs_do_task_bundle

    def get_configs_ao_task_bundle(self):
        """
        no None fields to propagate for this device.
        :param params:
        :param nidaq_terminals:
        :return:
        """
        return self.configs_ao_task_bundle

    def get_configs_scanning_galvo(self, params=None):
        """
        Note that the 'distance (um) to voltage (v) conversion factor (v/um)' should be done during the calibration
        stage.

        this should generate the data profile for this device, for the full cycle.
        for mode7, the full cycle is the entire stack (n frames)
        notes:
        self.slices_per_stack is the total number of slices per stack.
        self.sample_number_total_per_frame is the sample number per image.
        self.sample_number_total is the sample number per stack.

        :param params:
        :param nidaq_terminals:
        :return:
        """
        self.configs_scanning_galvo['data configs']['sample number'] = self.sample_number_total

        # home voltage for view 1 and view 2:
        vhome_view1 = self.configs_scanning_galvo['home voltage offset for view 1']
        vhome_view2 = self.configs_scanning_galvo['home voltage offset for view 2']

        dg = DAQDataGenerator()
        if self.configs_scanning_galvo['data generator'] == 'linear_ramp_soft_retraction':
            # scanning range in delta distance.
            # sr = params['scanning galvo scan range limit (um)']  # in O1 scan, scan the SG in it's full range.
            sr = 100 # scan 100 um.

            # voltage conversion factor
            d2v = self.configs_scanning_galvo['distance (um) to voltage (v) conversion factor (v/um)']
            # the +/- sign of this factor defines the scanning direciton with respect to the sign of the voltage applied to
            # the galvo.

            # scanning range in delta V
            sr_v = sr * d2v

            # linear ramp start/end voltage for view 1 a/2:
            v_start_view1 = vhome_view1 - sr_v / 2
            v_start_view2 = vhome_view2 - sr_v / 2
            v_stop_view1 = vhome_view1 + sr_v / 2
            v_stop_view2 = vhome_view2 + sr_v / 2

            self.configs_scanning_galvo['data configs']['linear ramp start for view 1'] = v_start_view1
            self.configs_scanning_galvo['data configs']['linear ramp stop for view 1'] = v_stop_view1
            self.configs_scanning_galvo['data configs']['linear ramp start for view 2'] = v_start_view2
            self.configs_scanning_galvo['data configs']['linear ramp stop for view 2'] = v_stop_view2
            self.configs_scanning_galvo['data configs']['linear ramp sample number'] = self.sample_number_on_duty
            self.configs_scanning_galvo['data configs']['soft retraction sample number'] = self.sample_number_off_duty

            data_view1 = \
                dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view1,
                                                      v1=v_stop_view1,
                                                      n_sample_ramp=self.sample_number_on_duty,
                                                      n_sample_retraction=self.sample_number_off_duty)

            data_view2 = \
                dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view2,
                                                      v1=v_stop_view2,
                                                      n_sample_ramp=self.sample_number_on_duty,
                                                      n_sample_retraction=self.sample_number_off_duty)

            n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
            self.configs_scanning_galvo['data for view 1'] = \
                list([data_view1[0]]*len(data_view1)+data_view1*(n_slices-1))
            self.configs_scanning_galvo['data for view 2'] = \
                list([data_view2[0]]*len(data_view2)+data_view2*(n_slices-1))

        elif self.configs_scanning_galvo['data generator'] == 'constant':
            data_view1 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=vhome_view1
                )
            data_view2 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=vhome_view2
                )

            self.configs_scanning_galvo['data for view 1'] = list(data_view1)
            self.configs_scanning_galvo['data for view 2'] = list(data_view2)

        return self.configs_scanning_galvo

    def get_configs_view_switching_galvo_1(self, params=None):
        self.configs_view_switching_galvo_1['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_view_switching_galvo_1['data generator'] == 'constant':
            data_view1 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_1['home voltage offset for view 1'],
                )
            data_view2 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_1['home voltage offset for view 2'],
                )
            self.configs_view_switching_galvo_1['data for view 1'] = list(data_view1)
            self.configs_view_switching_galvo_1['data for view 2'] = list(data_view2)

        return self.configs_view_switching_galvo_1

    def get_configs_view_switching_galvo_2(self, params=None):
        self.configs_view_switching_galvo_2['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_view_switching_galvo_2['data generator'] == 'constant':
            data_view1 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_2['home voltage offset for view 1'],
                )
            data_view2 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_2['home voltage offset for view 2'],
                )
            self.configs_view_switching_galvo_2['data for view 1'] = list(data_view1)
            self.configs_view_switching_galvo_2['data for view 2'] = list(data_view2)

        return self.configs_view_switching_galvo_2

    def get_configs_gamma_galvo_strip_reduction(self, params):
        # copy over the start and stop voltage for view 1.
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp start for view 1'] = \
            self.calibration_records['gamma galvo strip reduction']['linear ramp start for view 1']
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp stop for view 1'] = \
            self.calibration_records['gamma galvo strip reduction']['linear ramp stop for view 1']
        v_start_view1 = self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp start for view 1']
        v_stop_view1 = self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp stop for view 1']

        # copy over the start and stop voltage for view 2.
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp start for view 2'] = \
            self.calibration_records['gamma galvo strip reduction']['linear ramp start for view 2']
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp stop for view 2'] = \
            self.calibration_records['gamma galvo strip reduction']['linear ramp stop for view 2']
        v_start_view2 = self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp start for view 2']
        v_stop_view2 = self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp stop for view 2']

        # checkout a data generator
        dg = DAQDataGenerator()
        if self.configs_gamma_galvo_strip_reduction['data generator'] == 'linear_ramp_soft_retraction':
            n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
            data_view1 = dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view1,
                                                               v1=v_stop_view1,
                                                               n_sample_ramp=self.sample_number_on_duty,
                                                               n_sample_retraction=self.sample_number_off_duty)

            data_view2 = dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view2,
                                                               v1=v_stop_view2,
                                                               n_sample_ramp=self.sample_number_on_duty,
                                                               n_sample_retraction=self.sample_number_off_duty)

            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_gamma_galvo_strip_reduction['data for view 1'] = \
                list([data_view1[0]]*len(data_view1)+data_view1*(n_slices-1))
            self.configs_gamma_galvo_strip_reduction['data for view 2'] = \
                list([data_view2[0]]*len(data_view2)+data_view2*(n_slices-1))

        # self.configs_gamma_galvo_strip_reduction['data'] = None
        return self.configs_gamma_galvo_strip_reduction

    def get_configs_beta_galvo_light_sheet_incident_angle(self, params):
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_beta_galvo_light_sheet_incident_angle['data generator'] == 'constant':
            data_view1 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_beta_galvo_light_sheet_incident_angle['home voltage offset for view 1'],
                )
            data_view2 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_beta_galvo_light_sheet_incident_angle['home voltage offset for view 2'],
                )
            self.configs_beta_galvo_light_sheet_incident_angle['data for view 1'] = list(data_view1)
            self.configs_beta_galvo_light_sheet_incident_angle['data for view 2'] = list(data_view2)
        return self.configs_beta_galvo_light_sheet_incident_angle

    def get_configs_o1(self, params):
        self.configs_o1['data configs']['sample number'] = self.sample_number_total
        dg = DAQDataGenerator()
        d2v = self.calibration_records['O1']['distance (um) to voltage (v) conversion factor (v/um)']
        slice_distance = self.process_configs['process configs']['acquisition parameters']['slice distance (um)']
        voltage_increment_per_slice = d2v*slice_distance
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        # now assign the voltage profiles per slice:
        n_samples_per_frame = self.sample_number_on_duty+self.sample_number_off_duty
        self.configs_o1['data for view 1'] = []
        self.configs_o1['data for view 2'] = []
        # now generate the data sequences.
        # note that in mode 7, we want the O1 movement to happen and settle before exposure begins.
        # so here we choose to sacrifice the first cycle (turn off the laser, discard the first camera frame), and
        # move O1 starting from the beginning of the readout time (while everything else start operating at the
        # beginning of the exposure time)
        # prepare empty data sequences:

        # so, calculate data for O1 for the first cycle
        prof_view1 = \
            dg.constant(
                n_samples=self.sample_number_on_duty,
                constant=self.configs_o1['home voltage offset for view 1'],
            )
        prof_view2 = \
            dg.constant(
                n_samples=self.sample_number_on_duty,
                constant=self.configs_o1['home voltage offset for view 2'],
            )

        prof_view1 += self.configs_o1['home voltage offset for view 1']
        prof_view2 += self.configs_o1['home voltage offset for view 2']

        self.configs_o1['data for view 1'] = self.configs_o1['data for view 1'] + list(prof_view1)
        self.configs_o1['data for view 2'] = self.configs_o1['data for view 2'] + list(prof_view2)

        # then, calculate data for all the rest of the cycles.
        for slice_index in np.arange(1, n_slices):
            print('generating sequence for O1, slice #' + str(slice_index))
            v_incre = voltage_increment_per_slice*(slice_index-1) # -1 is to make sure the first data-frame will be the actual starting position.
            if self.configs_o1['data generator'] == 'constant':
                prof_view1 = \
                    dg.constant(
                        n_samples=n_samples_per_frame,
                        constant=self.configs_o1['home voltage offset for view 1'] + v_incre,
                    )
                prof_view2 = \
                    dg.constant(
                        n_samples=n_samples_per_frame,
                        constant=self.configs_o1['home voltage offset for view 2'] + v_incre,
                    )

                prof_view1 += self.configs_o1['home voltage offset for view 1']
                prof_view2 += self.configs_o1['home voltage offset for view 2']

                self.configs_o1['data for view 1'] = self.configs_o1['data for view 1'] + list(prof_view1)
                self.configs_o1['data for view 2'] = self.configs_o1['data for view 2'] + list(prof_view2)

        # now add the tail voltage to O1, to move the objective to the starting point, during the
        # last off-duty time (readout time window).
        prof_view1_tail = \
            dg.constant(
                n_samples=self.sample_number_off_duty,
                constant=self.configs_o1['home voltage offset for view 1'],
            )

        prof_view2_tail = \
            dg.constant(
                n_samples=self.sample_number_off_duty,
                constant=self.configs_o1['home voltage offset for view 2'],
            )

        prof_view1_tail += self.configs_o1['home voltage offset for view 1']
        prof_view2_tail += self.configs_o1['home voltage offset for view 2']

        self.configs_o1['data for view 1'] = self.configs_o1['data for view 1'] + list(prof_view1_tail)
        self.configs_o1['data for view 2'] = self.configs_o1['data for view 2'] + list(prof_view2_tail)

        self.configs_o1['data for view 1'], self.configs_o1['data for view 2'] =\
            _center_shift_2_lists(self.configs_o1['data for view 1'], self.configs_o1['data for view 2'])

        return self.configs_o1

    def get_configs_o3(self, params=None):
        self.configs_o3['data configs']['sample number'] = self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_o3['data generator'] == 'constant':
            data_view1 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_o3['home voltage offset for view 1'],
                )
            data_view2 = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_o3['home voltage offset for view 2'],
                )
            self.configs_o3['data for view 1'] = list(data_view1)
            self.configs_o3['data for view 2'] = list(data_view2)
        return self.configs_o3

    def get_configs_405_laser(self, params):
        """
        This creates the voltage sequence for the 405 laser for the full stack when the laser is on.
        """
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        self.configs_405_laser['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_405_laser['data generator'] == 'on-off sequence':
            one_frame_data = \
                dg.on_off_sequence(n_samples_on=self.sample_number_on_duty,
                                   n_samples_off=self.sample_number_off_duty,
                                   on_value=True,
                                   off_value=False)
            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_405_laser['data'] = [False]*len(one_frame_data)+one_frame_data*(n_slices-1)

        return self.configs_405_laser

    def get_configs_488_laser(self, params):
        """
        This creates the voltage sequence for the 488 laser for the full stack when the laser is on.
        """
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        self.configs_488_laser['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_488_laser['data generator'] == 'on-off sequence':
            one_frame_data = \
                dg.on_off_sequence(n_samples_on=self.sample_number_on_duty,
                                   n_samples_off=self.sample_number_off_duty,
                                   on_value=True,
                                   off_value=False)
            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_488_laser['data'] = [False]*len(one_frame_data)+one_frame_data*(n_slices-1)
        return self.configs_488_laser

    def get_configs_561_laser(self, params):
        """
        This creates the voltage sequence for the 561 laser for the full stack when the laser is on.
        """
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        self.configs_561_laser['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_561_laser['data generator'] == 'on-off sequence':
            one_frame_data = \
                dg.on_off_sequence(n_samples_on=self.sample_number_on_duty,
                                   n_samples_off=self.sample_number_off_duty,
                                   on_value=True,
                                   off_value=False)
            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_561_laser['data'] = [False]*len(one_frame_data)+one_frame_data*(n_slices-1)
        return self.configs_561_laser

    def get_configs_639_laser(self, params):
        """
        This creates the voltage sequence for the 639 laser for the full stack when the laser is on.
        """
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        self.configs_639_laser['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_639_laser['data generator'] == 'on-off sequence':
            one_frame_data = \
                dg.on_off_sequence(n_samples_on=self.sample_number_on_duty,
                                   n_samples_off=self.sample_number_off_duty,
                                   on_value=True,
                                   off_value=False)
            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_639_laser['data'] = [False]*len(one_frame_data)+one_frame_data*(n_slices-1)
        return self.configs_639_laser

    def get_configs_bright_field(self, params):
        """
        This creates the voltage sequence for the bright field LED for the full stack when the laser is on.
        """
        n_slices = self.process_configs['process configs']['acquisition parameters']['n slices']
        self.configs_bright_field['data configs']['sample number'] = \
            self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_bright_field['data generator'] == 'on-off sequence':
            one_frame_data = \
                dg.on_off_sequence(n_samples_on=self.sample_number_on_duty,
                                   n_samples_off=self.sample_number_off_duty,
                                   on_value=True,
                                   off_value=False)
            # keep in mind that the daq devices are not in duty for the first frame.
            # this is specific for mode7 acquisition.
            self.configs_bright_field['data'] = [False]*len(one_frame_data)+one_frame_data*(n_slices-1)
        return self.configs_bright_field

    def get_configs_single_cycle_dict(self, params):
        configs_list = {}
        for view in params['views']:
            for color in params['colors']:
                configs_list['view' + view + ' color' + color] = \
                    self.get_configs_single_cycle(view=view, color=color)
        return configs_list

    def get_configs_single_cycle(self, view=None, color=None):
        # now mask and pikc from the all cycle dicts, to return a singel cycle configs.
        configs = {}
        # go through every devices, and map the devices configs for a single cycle.
        configs['configs_metronome'] = self.map_sc_configs_metronome()
        configs['configs_counter'] = self.map_sc_configs_counter()
        configs['configs_DO_task_bundle'] = self.map_sc_configs_DO_task_bundle()
        configs['configs_AO_task_bundle'] = self.map_sc_configs_AO_task_bundle()
        configs['configs_scanning_galvo'] = self.map_sc_configs_scanning_galvo(view=view)
        configs['configs_view_switching_galvo_1'] = self.map_sc_configs_view_switching_galvo_1(view=view, color=color)
        configs['configs_view_switching_galvo_2'] = self.map_sc_configs_view_switching_galvo_2(view=view, color=color)
        configs['configs_gamma_galvo_strip_reduction'] = \
            self.map_sc_configs_gamma_galvo_strip_reduction(view=view, color=color)
        configs['configs_beta_galvo_light_sheet_incident_angle'] = \
            self.map_sc_configs_beta_galvo_light_sheet_incident_angle(view=view, color=color)
        configs['configs_O1'] = self.map_sc_configs_O1(view=view, color=color)
        configs['configs_O3'] = self.map_sc_configs_O3(view=view, color=color)
        configs['configs_405_laser'] = self.map_sc_configs_405_laser(view=view, color=color)
        configs['configs_488_laser'] = self.map_sc_configs_488_laser(view=view, color=color)
        configs['configs_561_laser'] = self.map_sc_configs_561_laser(view=view, color=color)
        configs['configs_639_laser'] = self.map_sc_configs_639_laser(view=view, color=color)
        configs['configs_bright_field'] = self.map_sc_configs_bright_field(view=view, color=color)
        return configs

    def map_sc_configs_metronome(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        configs = self.configs_metronome
        return configs

    def map_sc_configs_counter(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        configs = self.configs_counter
        return configs

    def map_sc_configs_DO_task_bundle(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        configs = self.configs_do_task_bundle
        return configs

    def map_sc_configs_AO_task_bundle(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        configs = self.configs_ao_task_bundle
        return configs

    def map_sc_configs_scanning_galvo(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        origin = self.configs_scanning_galvo
        # configs['device'] = origin['devices']
        configs = \
            {'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'idle state': origin['idle state'],
             'voltage output terminal': origin['voltage output terminal'],
             'distance (um) to voltage (v) conversion factor (v/um)':
                 origin['distance (um) to voltage (v) conversion factor (v/um)'],
             'data': origin['data for view ' + str(view)],
             'data generator': origin['data generator'],
             'data configs': None,
             }
        if origin['data generator'] == 'constant':
            configs['data configs'] = \
                {'type': origin['data configs']['type'],
                 'sample number': origin['data configs']['sample number']
                 }
        return configs

    def map_sc_configs_view_switching_galvo_1(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        origin = self.configs_view_switching_galvo_1
        configs = {
            'name': origin['name'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal'],
            'data': origin['data for view ' + str(view)],
            'data generator': origin['data generator'],
            'data configs': origin['data configs'],
        }
        return configs

    def map_sc_configs_view_switching_galvo_2(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        origin = self.configs_view_switching_galvo_2
        configs = {
            'name': origin['name'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal'],
            'data': origin['data for view ' + str(view)],
            'data generator': origin['data generator'],
            'data configs': origin['data configs'],
        }
        return configs

    def map_sc_configs_gamma_galvo_strip_reduction(self, view=None, color=None):
        """
        sc = single cycle
        :param view:
        :param color:
        :return:
        """
        origin = \
            self.configs_gamma_galvo_strip_reduction
        configs = {
            'data': origin['data for view ' + str(view)],
            'data configs': {'linear ramp sample number': origin['data configs']['linear ramp sample number'],
                             'linear ramp start': origin['data configs']['linear ramp start for view ' + str(view)],
                             'linear ramp stop': origin['data configs']['linear ramp stop for view ' + str(view)],
                             'soft retraction sample number': origin['data configs']['soft retraction sample number'],
                             'type': origin['data configs']['type']},
            'data generator': origin['data generator'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'name': origin['name'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal']}

        return configs

    def map_sc_configs_beta_galvo_light_sheet_incident_angle(self, view=None, color=None):
        """

        :param view:
        :param color:
        :return:
        """
        origin = \
            self.configs_beta_galvo_light_sheet_incident_angle
        configs = {
            'data': origin['data for view '+str(view)],
            'data configs': origin['data configs'],
            'data generator': origin['data generator'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'name': origin['name'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal']}
        return configs

    def map_sc_configs_O1(self, view=None, color=None):
        origin = \
            self.configs_o1
        configs = {
            'data': origin['data for view '+str(view)],
            'data configs': origin['data configs'],
            'data generator': origin['data generator'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'name': origin['name'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal']}
        return configs

    def map_sc_configs_O3(self, view=None, color=None):
        origin = \
            self.configs_o3
        configs = {
            'data': origin['data for view '+str(view)],
            'data configs': origin['data configs'],
            'data generator': origin['data generator'],
            'device': origin['device'],
            'idle state': origin['idle state'],
            'name': origin['name'],
            'task type': origin['task type'],
            'voltage output terminal': origin['voltage output terminal']}
        return configs

    def map_sc_configs_405_laser(self, view=None, color=None):
        origin=self.configs_405_laser
        if color == '405':
            data405=origin['data']
        else:
            data405=[False]*len(origin['data'])

        configs = \
            {
             'data': data405,
             'data configs': origin['data configs'],
             'data generator': origin['data generator'],
             'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'voltage output terminal': origin['voltage output terminal']
            }
        return configs

    def map_sc_configs_488_laser(self, view=None, color=None):
        origin = self.configs_488_laser
        if color == '488':
            data488 = origin['data']
        else:
            data488 = [False]*len(origin['data'])

        configs = \
            {
             'data': data488,
             'data configs': origin['data configs'],
             'data generator': origin['data generator'],
             'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'voltage output terminal': origin['voltage output terminal']
            }
        return configs

    def map_sc_configs_561_laser(self, view=None, color=None):
        origin = self.configs_561_laser
        if color == '561':
            data561 = origin['data']
        else:
            data561 = [False]*len(origin['data'])

        configs = \
            {
             'data': data561,
             'data configs': origin['data configs'],
             'data generator': origin['data generator'],
             'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'voltage output terminal': origin['voltage output terminal']
            }
        return configs

    def map_sc_configs_639_laser(self, view=None, color=None):
        origin = self.configs_639_laser
        if color == '639':
            data639 = origin['data']
        else:
            data639 = [False]*len(origin['data'])

        configs = \
            {
             'data': data639,
             'data configs': origin['data configs'],
             'data generator': origin['data generator'],
             'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'voltage output terminal': origin['voltage output terminal']
            }
        return configs

    def map_sc_configs_bright_field(self, view=None, color=None):
        origin = self.configs_bright_field
        if color == 'bright_field':
            data_bright_field = origin['data']
        else:
            data_bright_field = [False]*len(origin['data'])

        configs = \
            {
             'data': data_bright_field,
             'data configs': origin['data configs'],
             'data generator': origin['data generator'],
             'device': origin['device'],
             'name': origin['name'],
             'task type': origin['task type'],
             'voltage output terminal': origin['voltage output terminal']
            }
        return configs


class CameraConfigsGeneratorMode7(CameraConfigsGeneratorMode1):
    """
    keeping it the same with Mode1 acquisition
    """
    def __init__(self,
                 camera_core_configs=None):
        super().__init__(camera_core_configs=camera_core_configs)


    # def get_configs_camera(self, params):
    #     """
    #     generate the configuration file for the camera for this mode 1 acquisition
    #     """
    #     self.configs_camera['exposure time (ms)'] = params['exposure time (ms)']
    #     self.configs_camera['frame number'] = params['n slices']
    #     self.configs_camera['buffer size (frame number)'] = \
    #         self.configs_camera['frame number'] * self.configs_camera['buffer size (stack number)']
    #     return self.configs_camera
    #
    # def map_sc_configs_camera(self):
    #     """
    #     sc = single cycle
    #     :param view:
    #     :param color:
    #     :return:
    #     """
    #     configs = self.configs_camera
    #     return configs
    #
    # def get_configs_single_cycle_dict(self, params):
    #     configs_list = {}
    #     for view in params['views']:
    #         for color in params['colors']:
    #             configs_list['view' + view + ' color' + color] = \
    #                 self.map_sc_configs_camera()
    #     return configs_list


class StageConfigsGeneratorMode7(StageConfigsGeneratorMode1):
    def __init__(self,
                 stage_core_configs=None):
        super().__init__(stage_core_configs=stage_core_configs)
        # do some extra initiation operations.
        self._get_core_configs_asi_stage()

    # def get_configs_asi_stage(self, acquisition_params):
    #     """
    #     generate the configuration file for the camera for this mode 1 acquisition
    #     """
    #     # get exposure time (te):
    #     te = acquisition_params['exposure time (ms)']
    #
    #     # get readout time (tr) - or the time for everything to fly back in LS3 mode:
    #     tr = acquisition_params['camera read out time (ms)']
    #
    #     # total range (tr)
    #     total_range = acquisition_params['scanning range (um)']
    #
    #     # number of slices
    #     ns = acquisition_params['n slices']
    #
    #     # get travel range of sample per slice (um)
    #     slice_range = total_range/ns
    #
    #     # get travel time of sample per slice (ms)
    #     travel_time = te + tr
    #
    #     # get travel speed (the scanning speed of the stage) in um/ms
    #     scan_speed_umms = slice_range/travel_time
    #
    #     self.configs_asi_stage['scan speed (um/ms)'] = scan_speed_umms
    #     self.configs_asi_stage['scan range (um)'] = slice_range
    #     self.configs_asi_stage['start position'] = None
    #     self.configs_asi_stage['end position'] = None
    #     self.configs_asi_stage['position list'] = acquisition_params['positions']
    #
    #     return self.configs_asi_stage
    #
    # def map_sc_configs_asi_stage(self):
    #     """
    #     sc = single cycle
    #     :param view:
    #     :param color:
    #     :return:
    #     """
    #     configs = self.configs_asi_stage
    #     return configs
    #
    # def get_configs_single_cycle_dict(self, params):
    #     configs_list = {}
    #     for view in params['views']:
    #         for color in params['colors']:
    #             configs_list['view' + view + ' color' + color] = \
    #                 self.map_sc_configs_asi_stage()
    #     return configs_list


def _center_shift_2_lists(a: list, b: list):
    mida = a[int(np.ceil(len(a) / 2))]
    midb = b[int(np.ceil(len(b) / 2))]
    mid = (mida + midb)/2
    a = list(np.asarray(a) - mid)
    b = list(np.asarray(b) - mid)
    return a, b
