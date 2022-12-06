from daxi.control.process.facilitator.processes_facilitator_gui import ProcessesFcltrGUI
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
        self.get_configs_nidaq()
        self.get_configs_asistage()
        self.get_configs_hamamatsu()

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
        configs = {
            "speed": 100,
            "position name 1": {'x': 1, 'y': 10},
            "position name 2": {'x': 2, 'y': 11},
        }  # this is a place holder, should expand in the future. this is currently in the parameter selection and it is
        # part of the acquisition_configs. the information should be extracted from the GUI.
        self.configs_asistage = configs

    def get_configs_hamamatsu(self):
        """
        this is a place holder, should change this into retrieving data from the GUI.
        (the gui can generate the parameter dictionary from all fileds configurations, or load from a file, etc.).
        :return:
        """
        configs = {
            "camera name": 'hamamatsu orca flash 4',
        }  # this is a placeholder.
        self.configs_hamamatsu = configs

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


def load_process_configs(path: str):
    """
    save out the process configurations out to the path
    :param path:  full path to the yaml file.
    :param configs:  full path to the yaml file.
    :return:
    """
    with open(path, 'r') as stream:
        output = yaml.safe_load(stream)

    return output
