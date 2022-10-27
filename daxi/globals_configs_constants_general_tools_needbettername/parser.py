# this is supposed to parse information from the configuration file into python objects


class NIDAQConfigsParser:
    def __init__(self):
        self.configs_path = None
        self.counter_configs = None
        self.metronome_configs = None
        self.oscilloscope1_configs = None
        self.taskbundle_ao_confgs = None
        self.scanning_galvo_configs = None
        self.oscilloscope1_configs = None
        self.oscilloscope2_configs = None
        self.oscilloscope3_configs = None

    def set_configs_path(self, path):
        self.configs_path = path

    def get_config_by_keyword(self, keyword):
        """
        This method will find the configuration path, parse the information,
        and store it in counter_configs
        :return:
        counter configurations, dict.
        """
        with open(self.configs_path, 'r') as file:
            data = file.read()

        k = data.split('Virtual Tools Section: '+keyword)[1]\
            .split('definition start.')[1].split('definition end.')[0]

        configs = eval(k)
        return configs

    def get_counter_configs(self):
        """
        This will extract the counter configuration info.
        :return:
        counter configurations, dict.
        """
        self.counter_configs = self.get_config_by_keyword('counter')
        return self.counter_configs

    def get_metronome_configs(self):
        """
        This will extract the metronome configuration info.
        :return:
        metronome configurations, dict.
        """
        self.metronome_configs = self.get_config_by_keyword('metronome')
        return self.metronome_configs

    def get_ao_task_bundle_configs(self):
        """
        This will extract the ao task bundle configuration info.
        :return:
        taskbundle_ao_confgs configurations, dict.
        """
        self.taskbundle_ao_confgs = self.get_config_by_keyword('task-bundle-ao')
        return self.taskbundle_ao_confgs

    def get_configs_by_path_section_keyword(self, section, keyword, verbose=True):
        # todo: refactor this once the names are settled. Think about whether you should
        #  combine the configuration files or not, or change the way thoe files were organized.
        """
        There should be a UI where you configured the devices....

        :return:
        """
        with open(self.configs_path, 'r') as file:
            data = file.read()
        if verbose:
            print('testing...')
            print(section + ': ' + keyword)
        k = data.split(section + ': ' + keyword)[1]\
            .split('definition start.')[1].split('definition end.')[0]
        if verbose:
            print('executing the following command:')
            print(k)
        configs = eval(k)
        if keyword == 'oscilloscope_channel1':
            self.oscilloscope1_configs = configs

        if keyword == 'oscilloscope_channel2':
            self.oscilloscope2_configs = configs

        if keyword == 'oscilloscope_channel3':
            self.oscilloscope3_configs = configs

        if keyword == 'scanning_galvo_soft_retraction' or 'scanning_galvo':
            self.scanning_galvo_configs = configs

        return configs

    def get_oscilloscope1_configs(self):
        self.oscilloscope1_configs = \
            self.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                     keyword='oscilloscope_channel1')
        return self.oscilloscope1_configs

    def get_oscilloscope2_configs(self):
        self.oscilloscope2_configs = \
            self.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                     keyword='oscilloscope_channel2')
        return self.oscilloscope2_configs

    def get_oscilloscope3_configs(self):
        self.oscilloscope3_configs = \
            self.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                                     keyword='oscilloscope_channel3')
        return self.oscilloscope3_configs
