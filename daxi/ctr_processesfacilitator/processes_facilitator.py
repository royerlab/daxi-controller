from daxi.ctr_processesfacilitator.processes_facilitator_gui import ProcessesFcltrGUI
import yaml


class ProcessesFcltr(ProcessesFcltrGUI):
    def __init__(self):
        self.process_type = None
        self.process_parameters = None
        self.configs_nidaq = None
        self.configs_asistage = None
        self.configs_hamamatsu = None
        self.configs_save_data = None

    def start(self):
        self.get_process_type()
        self.get_process_parameters()
        self.get_nidaq_configurations()
        self.get_asistage_configurations()
        self.get_hamamatsu_configurations()

    def get_process_type(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        :return:
        """
        self.process_type = 'acquisition'

    def get_process_parameters(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        (the gui can generate the parameter dictionary from all fileds configurations, or load from a file, etc.).
        :return:
        """
        from daxi.globals_configs_constants_general_tools_needbettername.constants import params_test_selected_params
        from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
        p = NIDAQConfigsParser()
        p.set_configs_path(params_test_selected_params)
        section = 'Selected Parameters Section'
        keyword = 'mode1_demo'
        params = \
            p.get_configs_by_path_section_keyword(section, keyword)
        self.process_parameters = params

    def get_configs_nidaq(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        (the gui can generate the parameter dictionary from all fileds configurations, or load from a file, etc.).
        :return:
        """
        self.configs_nidaq = None
        # todo - perhaps bundle the daq device configurations all into this dictionary.

    def get_configs_asistage(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        (the gui can generate the parameter dictionary from all fileds configurations, or load from a file, etc.).
        :return:
        """
        self.configs_asistage = None

    def get_configs_hamamatsu(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        (the gui can generate the parameter dictionary from all fileds configurations, or load from a file, etc.).
        :return:
        """
        self.configs_hamamatsu = None

    def get_configs_save_data(self):
        """
        this is a place holder, should replace into something that interfaces with the DatastorageFcltr
        :return:
        """
        self.configs_save_data = None


def save_process_configs(path: str, configs: dict):
    """
    save out the process configurations out to the path
    :param path:  full path to the yaml file.
    :param configs:  full path to the yaml file.
    :return:
    """
    with open(path, 'w') as outfile:
        yaml.dump(configs, outfile, default_flow_style=False)
