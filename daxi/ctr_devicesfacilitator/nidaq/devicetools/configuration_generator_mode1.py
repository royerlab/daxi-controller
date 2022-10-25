from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_base import NIDAQDevicesConfigsGeneratorBase
from daxi.ctr_devicesfacilitator.nidaq.devicetools.generate_functions import DAQDataGenerator
import numpy as np


class NIDAQDevicesConfigsGeneratorMode1(NIDAQDevicesConfigsGeneratorBase):
    """
    This class takes the acquisition parameters, and generate the configuration dictionaries for all the devices.
    This class is designed for mode1 acquisition

    the looping order for this acquisition mode is:
    [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]

    all the configuration templates should be loaded in the base class.
    And the methods here is to calculate and populate up the "None" fields.
    """

    def __init__(self,
                 params=None,
                 nidaq_terminals=None,
                 calibration_records=None,
                 alignment_records=None,
                 verbose=False):
        super().__init__(nidaq_terminals,
                         calibration_records=calibration_records,
                         alignment_records=alignment_records)
        self.verbose = verbose
        self._get_core_configs_for_all()

        # total number of samples
        self.sample_number_total = np.int32(np.floor(
            params['metronome frequency'] *
            (params['exposure time (ms)'] + params['camera read out time (ms)']) / 1000
        ))

        # calculate the number of samples during camera exposure (can chase a bit longer by using np.ceil)
        self.sample_number_on_duty = np.int32(np.ceil(
            params['metronome frequency'] * (params['exposure time (ms)']) / 1000
        ))

        # calculate the number of samples during camera readout
        self.sample_number_off_duty = self.sample_number_total - self.sample_number_on_duty

    def get_configs_for_metronome(self):
        """

        :param params: dictionary, the configuration parameters of all the specific device
        :param nidaq_terminals: dict. the configurations of all the wiring of daq cards for all devices.
        :return:
        """
        # for mode 1, one period of daq sequences should be one camera exposure + one readout time.
        # camera exposure trigger is the trigger for the daq cards
        # t = (params['exposure time (ms)'] + params['camera read out time (ms)']) / 1000  # cycle time, unit = s
        # number_of_samples = params['metronome frequency'] / t
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

    def get_configs_scanning_galvo(self, params):
        """
        Note that the 'distance (um) to voltage (v) conversion factor (v/um)' should be done during the calibration
        stage.

        Now think about the specifics of this scanning galvo.
        1. Perhaps during alignment, we need to set a "neutral position" in the calibration ste, where the lightsheet
        is in parallel with the optical axis of O1.
        2. We also need the 'distance (um) to voltage (v) conversion factor (v/um)' during the calibration step.
        3. Based on the acquisition parameters, we can calculate the total scanning range of the SG galvo.
            tExposure * stage scanning speed = scanning range.

        4. now think about how do we configure 1 sequence of data.
            if we continue to use the camera trigger, the sequnce cut-off should happen per slice.
            we need to be able to swap-in different sequences. perhaps need to stop and write again.

        When everything is set at the "home" position, the light sheet should exit O1 parallel to it's optical
        axis.
        have to test it!!!!!! test it now. create an issue first.
        # todo test stop-write-start sequence for daq device control without closing the device.
        In this class, we simply prepare two sequences of the data for both view 1 and view 2.


        Here is the demo parameters for mode 1 acquisition:
        {
         'name': 'demo mode1',
         'type': 'mode1',
         'looping order': '[mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]',
         'camera read out time (ms)': 10,
         'exposure time (ms)': 90,
         'mag-factor': 5,
         'n slices': 354.0,
         'pixel size in xy (um)': 0.4,
         'metronome frequency': 1000, # Hz
         'scanning galvo scan range limit (um)': 0.8,
         'scanning galvo scan range per slice (um)': 2.545584412271571,
         'scanning range (um)': 1001.2632021601514,
         'scanning speed (nm/ms)': 28.284271247461902,
         'slice distance (um)': 2.0,
         'stage retraction time (ms)': 23,
         'time per stack per view (s)': 35.423,
         'time per time point (s)': 141.692
        }

        :param params:
        :param nidaq_terminals:
        :return:
        """
        # scanning range in delta distance.
        sr = params['scanning range (um)']

        # home voltage for view 1 and view 2:
        vhome_view1 = self.configs_scanning_galvo['home voltage offset for view 1']
        vhome_view2 = self.configs_scanning_galvo['home voltage offset for view 2']

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

        # ahh should think about a design pattern here and update later.
        dg = DAQDataGenerator()
        if self.configs_scanning_galvo['data generator'] == 'linear_ramp_soft_retraction':
            data_view1 = dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view1,
                                                               v1=v_stop_view1,
                                                               n_sample_ramp=self.sample_number_on_duty,
                                                               n_sample_retraction=self.sample_number_off_duty)

            data_view2 = dg.getfcn_linear_ramp_soft_retraction(v0=v_start_view2,
                                                               v1=v_stop_view2,
                                                               n_sample_ramp=self.sample_number_on_duty,
                                                               n_sample_retraction=self.sample_number_off_duty)

            self.configs_scanning_galvo['data for view 1'] = data_view1
            self.configs_scanning_galvo['data for view 2'] = data_view2
        else:
            raise Exception('sorry, please choose from the available data generators')

        return self.configs_scanning_galvo

    def get_configs_view_switching_galvo_1(self, params, nidaq_terminals):
        self.configs_view_switching_galvo_1['data configs']['sample number'] = self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_view_switching_galvo_1['data generator'] == 'constant':
            self.configs_view_switching_galvo_1['data for view 1'] = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_1['home voltage offset for view 1'],
                 )
            self.configs_view_switching_galvo_1['data for view 2'] = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_1['home voltage offset for view 2'],
                 )

        return self.configs_view_switching_galvo_1

    def get_configs_view_switching_galvo_2(self, params, nidaq_terminals):
        self.configs_view_switching_galvo_2['data configs']['sample number'] = self.sample_number_total
        dg = DAQDataGenerator()
        if self.configs_view_switching_galvo_2['data generator'] == 'constant':
            self.configs_view_switching_galvo_2['data for view 1'] = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_2['home voltage offset for view 1'],
                 )
            self.configs_view_switching_galvo_2['data for view 2'] = \
                dg.constant(
                    n_samples=self.sample_number_total,
                    constant=self.configs_view_switching_galvo_2['home voltage offset for view 2'],
                 )

        return self.configs_view_switching_galvo_2

    def get_configs_gamma_galvo_strip_reduction(self, params, nidaq_terminals):
        self.configs_gamma_galvo_strip_reduction['data'] = None
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp start'] = None
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp stop'] = None
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp sample number'] = None
        self.configs_gamma_galvo_strip_reduction['data configs']['soft retraction sample number'] = None
        return self.configs_gamma_galvo_strip_reduction

    def get_configs_beta_galvo_light_sheet_incident_angle(self, params, nidaq_terminals):
        self.configs_beta_galvo_light_sheet_incident_angle['data'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['on-duty sample number'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['off-duty sample number'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['acquisition mode'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['number of options for the sequence'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['voltage on'] = None
        self.configs_beta_galvo_light_sheet_incident_angle['data configs']['voltage off'] = None
        return self.configs_beta_galvo_light_sheet_incident_angle

    def get_configs_o1(self, params, nidaq_terminals):
        self.configs_o1['data'] = None
        self.configs_o1['data configs']['on-duty sample number'] = None
        self.configs_o1['data configs']['off-duty sample number'] = None
        self.configs_o1['data configs']['acquisition mode'] = None
        self.configs_o1['data configs']['number of options for the sequence'] = None
        self.configs_o1['data configs']['voltage on'] = None
        self.configs_o1['data configs']['voltage off'] = None
        return self.configs_o1

    def get_configs_o3(self, params, nidaq_terminals):
        self.configs_o3['data'] = None
        self.configs_o3['data configs']['on-duty sample number'] = None
        self.configs_o3['data configs']['off-duty sample number'] = None
        self.configs_o3['data configs']['acquisition mode'] = None
        self.configs_o3['data configs']['number of options for the sequence'] = None
        self.configs_o3['data configs']['voltage on'] = None
        self.configs_o3['data configs']['voltage off'] = None
        return self.configs_o3

    def get_configs_405_laser(self, params, nidaq_terminals):
        self.configs_405_laser['data'] = None
        self.configs_405_laser['data configs']['on-duty sample number'] = None
        self.configs_405_laser['data configs']['off-duty sample number'] = None
        self.configs_405_laser['data configs']['acquisition mode'] = None
        self.configs_405_laser['data configs']['number of options for the sequence'] = None
        self.configs_405_laser['data configs']['voltage on'] = None
        self.configs_405_laser['data configs']['voltage off'] = None
        return self.configs_405_laser

    def get_configs_488_laser(self, params, nidaq_terminals):
        self.configs_488_laser['data'] = None
        self.configs_488_laser['data configs']['on-duty sample number'] = None
        self.configs_488_laser['data configs']['off-duty sample number'] = None
        self.configs_488_laser['data configs']['acquisition mode'] = None
        self.configs_488_laser['data configs']['number of options for the sequence'] = None
        self.configs_488_laser['data configs']['voltage on'] = None
        self.configs_488_laser['data configs']['voltage off'] = None
        return self.configs_488_laser

    def get_configs_561_laser(self, params, nidaq_terminals):
        self.configs_561_laser['data'] = None
        self.configs_561_laser['data configs']['on-duty sample number'] = None
        self.configs_561_laser['data configs']['off-duty sample number'] = None
        self.configs_561_laser['data configs']['acquisition mode'] = None
        self.configs_561_laser['data configs']['number of options for the sequence'] = None
        self.configs_561_laser['data configs']['voltage on'] = None
        self.configs_561_laser['data configs']['voltage off'] = None
        return self.configs_561_laser

    def get_configs_639_laser(self, params, nidaq_terminals):
        self.configs_639_laser['data'] = None
        self.configs_639_laser['data configs']['on-duty sample number'] = None
        self.configs_639_laser['data configs']['off-duty sample number'] = None
        self.configs_639_laser['data configs']['acquisition mode'] = None
        self.configs_639_laser['data configs']['number of options for the sequence'] = None
        self.configs_639_laser['data configs']['voltage on'] = None
        self.configs_639_laser['data configs']['voltage off'] = None
        return self.configs_639_laser

    def get_configs_bright_field(self, params, nidaq_terminals):
        self.configs_bright_field['data'] = None
        self.configs_bright_field['data configs']['on-duty sample number'] = None
        self.configs_bright_field['data configs']['off-duty sample number'] = None
        self.configs_bright_field['data configs']['acquisition mode'] = None
        self.configs_bright_field['data configs']['number of options for the sequence'] = None
        self.configs_bright_field['data configs']['voltage on'] = None
        self.configs_bright_field['data configs']['voltage off'] = None
        return self.configs_bright_field
