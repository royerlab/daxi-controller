from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools_needbettername.constants import configs_core_daq_devices


class NIDAQDevicesConfigsGeneratorBase:
    """
    This will take a parameter dictionary and generate the corresponding configurations
    """
    def __init__(self,
                 nidaq_terminals,
                 calibration_records=None,
                 alignment_records=None,
                 verbose=True):
        """
        upon initialization, the program will first take the tempalte of configs_core_daq_devices (this is the
        fundamental tempalte for the daq devices for a DaXi microscope, without any configurations that are specific to
        a specific wiring of a specific DaXi microscope. The core configurations is a list of place holders that defines
        the outline of the configurations for all daq devices)

        this class also requires an input instance of nidaq_termianls, which is a dictionary that specifies the
        wiring of daq card terminals and the hardware for a specific DaXi microscope, and is expected to be filled out
        by the optical engineer when they build the microscope.

        :param nidaq_terminals:
        """
        self.configs_metronome = None
        self.configs_counter = None
        self.configs_do_task_bundle = None
        self.configs_ao_task_bundle = None
        self.configs_scanning_galvo = None
        self.configs_view_switching_galvo_1 = None
        self.configs_view_switching_galvo_2 = None
        self.configs_gamma_galvo_strip_reduction = None
        self.configs_beta_galvo_light_sheet_incident_angle = None
        self.configs_o1 = None
        self.configs_o3 = None
        self.configs_405_laser = None
        self.configs_488_laser = None
        self.configs_561_laser = None
        self.configs_639_laser = None
        self.configs_bright_field = None
        self.sample_number_total = None
        self.sample_number_on_duty = None
        self.sample_number_off_duty = None
        self.parser = NIDAQConfigsParser()
        self.parser.set_configs_path(configs_core_daq_devices)
        self.nidaq_terminals = nidaq_terminals
        self.calibration_records = calibration_records
        self.alignment_records = alignment_records
        self.verbose = verbose

    def _get_core_configs_for_all(self):
        """
        This method runs all the _get_core_configs_* methods of this class.
        It will take the core template  of the configuration files for all the daq controlled devices, and at the same
        time take the terminal wiring profile that is specific to the specific DaXi microscope, and copy-over the
        terminal configurations to each configuration dictionary.
        :return:
        """
        self._get_core_configs_for_metronome()
        self._get_core_configs_for_counter()
        self._get_core_configs_for_do_task_bundle()
        self._get_core_configs_for_ao_task_bundle()
        self._get_core_configs_scanning_galvo()
        self._get_core_configs_view_switching_galvo_1()
        self._get_core_configs_view_switching_galvo_2()
        self._get_core_configs_gamma_galvo_strip_reduction()
        self._get_core_configs_beta_galvo_light_sheet_incident_angle()
        self._get_core_configs_o1()
        self._get_core_configs_o3()
        self._get_core_configs_405_laser()
        self._get_core_configs_488_laser()
        self._get_core_configs_561_laser()
        self._get_core_configs_639_laser()
        self._get_core_configs_bright_field()

    def _get_core_configs_for_metronome(self):
        # now load in the configurations for all devices from the core configurations,
        # and populate up the terminals.
        self.configs_metronome = \
            self.parser.get_configs_by_path_section_keyword(section='Virtual Tools Section',
                                                            keyword='metronome',
                                                            verbose=self.verbose)
        self.configs_metronome['counter terminal'] = \
            self.nidaq_terminals['metronome terminals']['counter terminal']
        self.configs_metronome['counting output terminal'] = \
            self.nidaq_terminals['metronome terminals']['counting output terminal']
        self.configs_metronome['trigger terminal'] = \
            self.nidaq_terminals['metronome terminals']['trigger terminal']

    def _get_core_configs_for_counter(self):
        self.configs_counter = \
            self.parser.get_configs_by_path_section_keyword(section='Virtual Tools Section',
                                                            keyword='counter',
                                                            verbose=self.verbose)
        self.configs_counter['counter terminal'] = \
            self.nidaq_terminals['counter terminals']['counter terminal']
        self.configs_counter['counting input terminal'] = \
            self.nidaq_terminals['counter terminals']['counting input terminal']

    def _get_core_configs_for_do_task_bundle(self):
        self.configs_do_task_bundle = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='DO_task_bundle',
                                                            verbose=self.verbose)
        self.configs_do_task_bundle['trigger terminal'] = \
            self.nidaq_terminals['do task bundle']['trigger terminal']

    def _get_core_configs_for_ao_task_bundle(self):
        self.configs_ao_task_bundle = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='AO_task_bundle',
                                                            verbose=self.verbose)
        self.configs_ao_task_bundle['trigger terminal'] = \
            self.nidaq_terminals['ao task bundle']['trigger terminal']

    def _get_core_configs_scanning_galvo(self):
        self.configs_scanning_galvo = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='scanning_galvo',
                                                            verbose=self.verbose)
        self.configs_scanning_galvo['voltage output terminal'] = \
            self.nidaq_terminals['scanning galvo']['voltage output terminal']
        self.configs_scanning_galvo['distance (um) to voltage (v) conversion factor (v/um)'] = \
            self.calibration_records['scanning galvo']['distance (um) to voltage (v) conversion factor (v/um)']
        self.configs_scanning_galvo['home voltage offset for view 1'] = \
            self.alignment_records['scanning galvo']['home voltage offset for view 1']
        self.configs_scanning_galvo['home voltage offset for view 2'] = \
            self.alignment_records['scanning galvo']['home voltage offset for view 2']

    def _get_core_configs_view_switching_galvo_1(self):
        self.configs_view_switching_galvo_1 = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='view_switching_galvo_1',
                                                            verbose=self.verbose)
        self.configs_view_switching_galvo_1['voltage output terminal'] = \
            self.nidaq_terminals['view switching galvo 1']['voltage output terminal']
        self.configs_view_switching_galvo_1['home voltage offset for view 1'] = \
            self.alignment_records['view switching galvo 1']['home voltage offset for view 1']
        self.configs_view_switching_galvo_1['home voltage offset for view 2'] = \
            self.alignment_records['view switching galvo 1']['home voltage offset for view 2']

    def _get_core_configs_view_switching_galvo_2(self):
        self.configs_view_switching_galvo_2 = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='view_switching_galvo_2',
                                                            verbose=self.verbose)
        self.configs_view_switching_galvo_2['voltage output terminal'] = \
            self.nidaq_terminals['view switching galvo 2']['voltage output terminal']
        self.configs_view_switching_galvo_2['home voltage offset for view 1'] = \
            self.alignment_records['view switching galvo 2']['home voltage offset for view 1']
        self.configs_view_switching_galvo_2['home voltage offset for view 2'] = \
            self.alignment_records['view switching galvo 2']['home voltage offset for view 2']

    def _get_core_configs_gamma_galvo_strip_reduction(self):
        self.configs_gamma_galvo_strip_reduction = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='gamma_galvo_strip_reduction',
                                                            verbose=self.verbose)
        self.configs_gamma_galvo_strip_reduction['voltage output terminal'] = \
            self.nidaq_terminals['gamma galvo strip reduction']['voltage output terminal']
        self.configs_gamma_galvo_strip_reduction['home voltage offset for view 1'] = \
            self.alignment_records['gamma galvo strip reduction']['home voltage offset for view 1']
        self.configs_gamma_galvo_strip_reduction['home voltage offset for view 2'] = \
            self.alignment_records['gamma galvo strip reduction']['home voltage offset for view 2']
        self.configs_gamma_galvo_strip_reduction['data configs']['linear ramp sample number'] = \
            self.sample_number_on_duty
        self.configs_gamma_galvo_strip_reduction['data configs']['soft retraction sample number'] = \
            self.sample_number_off_duty

    def _get_core_configs_beta_galvo_light_sheet_incident_angle(self):
        self.configs_beta_galvo_light_sheet_incident_angle = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='beta_galvo_light_sheet_incident_angle',
                                                            verbose=self.verbose)
        self.configs_beta_galvo_light_sheet_incident_angle['voltage output terminal'] = \
            self.nidaq_terminals['beta galvo light sheet incident angle']['voltage output terminal']
        self.configs_beta_galvo_light_sheet_incident_angle['home voltage offset for view 1'] = \
            self.alignment_records['beta galvo light sheet incident angle']['home voltage offset for view 1']
        self.configs_beta_galvo_light_sheet_incident_angle['home voltage offset for view 2'] = \
            self.alignment_records['beta galvo light sheet incident angle']['home voltage offset for view 2']

    def _get_core_configs_o1(self):
        self.configs_o1 = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='O1',
                                                            verbose=self.verbose)
        self.configs_o1['voltage output terminal'] = \
            self.nidaq_terminals['O1']['voltage output terminal']

        self.configs_o1['home voltage offset for view 1'] = \
            self.alignment_records['O1']['home voltage offset for view 1']
        self.configs_o1['home voltage offset for view 2'] = \
            self.alignment_records['O1']['home voltage offset for view 2']

    def _get_core_configs_o3(self):
        self.configs_o3 = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='O3',
                                                            verbose=self.verbose)
        self.configs_o3['voltage output terminal'] = \
            self.nidaq_terminals['O3']['voltage output terminal']

        self.configs_o3['home voltage offset for view 1'] = \
            self.alignment_records['O3']['home voltage offset for view 1']
        self.configs_o3['home voltage offset for view 2'] = \
            self.alignment_records['O3']['home voltage offset for view 2']

    def _get_core_configs_405_laser(self):
        self.configs_405_laser = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='405-laser',
                                                            verbose=self.verbose)
        self.configs_405_laser['voltage output terminal'] = \
            self.nidaq_terminals['405 laser']['voltage output terminal']

    def _get_core_configs_488_laser(self):
        self.configs_488_laser = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='488-laser',
                                                            verbose=self.verbose)
        self.configs_488_laser['voltage output terminal'] = \
            self.nidaq_terminals['488 laser']['voltage output terminal']

    def _get_core_configs_561_laser(self):
        self.configs_561_laser = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='561-laser',
                                                            verbose=self.verbose)
        self.configs_561_laser['voltage output terminal'] = \
            self.nidaq_terminals['561 laser']['voltage output terminal']

    def _get_core_configs_639_laser(self):
        self.configs_639_laser = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='639-laser',
                                                            verbose=self.verbose)
        self.configs_639_laser['voltage output terminal'] = \
            self.nidaq_terminals['639 laser']['voltage output terminal']

    def _get_core_configs_bright_field(self):
        self.configs_bright_field = \
            self.parser.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                            keyword='bright-field',
                                                            verbose=self.verbose)
        self.configs_bright_field['voltage output terminal'] = \
            self.nidaq_terminals['bright field']['voltage output terminal']

    def get_configs_for_metronome(self):
        pass

    def get_configs_for_counter(self):
        pass

    def get_configs_do_task_bundle(self):
        pass

    def get_configs_ao_task_bundle(self):
        pass

    def get_configs_scanning_galvo(self, params):
        pass

    def get_configs_view_switching_galvo_1(self, params, nidaq_terminals):
        pass

    def get_configs_view_switching_galvo_2(self, params, nidaq_terminals):
        pass

    def get_configs_gamma_galvo_strip_reduction(self, params, nidaq_terminals):
        pass

    def get_configs_beta_galvo_light_sheet_incident_angle(self, params, nidaq_terminals):
        pass

    def get_configs_o1(self, params, nidaq_terminals):
        pass

    def get_configs_o3(self, params, nidaq_terminals):
        pass

    def get_configs_405_laser(self, params, nidaq_terminals):
        pass

    def get_configs_488_laser(self, params, nidaq_terminals):
        pass

    def get_configs_561_laser(self, params, nidaq_terminals):
        pass

    def get_configs_639_laser(self, params, nidaq_terminals):
        pass

    def get_configs_bright_field(self, params, nidaq_terminals):
        pass

    def get_configs_single_cycle(self, params):
        pass
