from daxi.ctr_devicesfacilitator.nidaq.devicetools.configuration_generator_base import NIDAQDevicesConfigsGeneratorBase


class NIDAQDevicesConfigsGeneratorMode6(NIDAQDevicesConfigsGeneratorBase):
    """
    This class takes the acquisition parameters, and generate the configuration dictionaries for all the devices.
    This class is designed for mode6 acquisition

    the looping order for this acquisition mode is:
    [mode 6] - [layer 1: position, view] - [layer 2: slice, color]
    """
    def get_config_for_metronome(self, params):
        pass

    def get_config_for_counter(self, params):
        pass

    def get_config_do_task_bundle(self, params):
        pass

    def get_config_ao_task_bundle(self, params):
        pass

    def get_config_scanning_galvo(self, params):
        pass

    def get_config_view_switching_galvo_1(self, params):
        pass

    def get_config_view_switching_galvo_2(self, params):
        pass

    def get_config_gamma_galvo_strip_reduction(self, params):
        pass

    def get_config_beta_galvo_light_sheet_incident_angle(self, params):
        pass

    def get_config_o1(self, params):
        pass

    def get_config_o3(self, params):
        pass

    def get_config_405_laser(self, params):
        pass

    def get_config_488_laser(self, params):
        pass

    def get_config_561_laser(self, params):
        pass

    def get_config_639_laser(self, params):
        pass

    def get_config_bright_field(self, params):
        pass
