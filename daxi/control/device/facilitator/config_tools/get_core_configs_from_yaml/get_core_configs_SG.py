# input should be a loaded yaml file result that's already converted into a dictionary.

# output format should be:
# {'device': 'scanning_galvo',
#  'name': 'Scanning Galvo with linear ramp soft retraction',
#  'task type': 'AO subtask',
#  'idle state': 'LOW',
#  'voltage output terminal': None,
#  'home voltage offset for view 1': None,
#  'home voltage offset for view 2': None,
#  'distance (um) to voltage (v) conversion factor (v/um)': None,
#  'data for view 1': None,
#  'data for view 2': None,
#  'data generator': 'linear_ramp_soft_retraction',
#  'data configs': {'type': 'ao subtask configuration',
#   'linear ramp start for view 1': None,
#   'linear ramp stop for view 1': None,
#   'linear ramp start for view 2': None,
#   'linear ramp stop for view 2': None,
#   'linear ramp sample number': None,
#   'soft retraction sample number': None}}


def _get_core_sg_configs(process_configs: dict):
    """
    This function generates the SG core configurations based on the input yaml file.

    @param process_configs: This will be the dictionary loaded from the yaml file that.
    @return:
    """

    # first, set place holder for all other acquisition modes:
    name = 'Scanning Galvo, idle'
    data_generator = 'constant'
    data_configs = {'type': 'ao subtask configuration', 'sample number': None}

    # set configurations for mode 1
    if process_configs['process type'] == 'acquisition, mode 1':
        name = 'Scanning Galvo with linear ramp soft retraction'
        data_generator = 'linear_ramp_soft_retraction'
        data_configs = {'type': 'ao subtask configuration',
                        'linear ramp start for view 1': None,
                        'linear ramp stop for view 1': None,
                        'linear ramp start for view 2': None,
                        'linear ramp stop for view 2': None,
                        'linear ramp sample number': None,
                        'soft retraction sample number': None}

    # set configurations for mode 7
    if process_configs['process type'] == 'acquisition, mode 7':
        # name = 'Scanning Galvo, static'
        # data_generator = 'constant'
        # data_configs = {'type': 'ao subtask configuration', 'sample number': None}
        name = 'Scanning Galvo with linear ramp soft retraction'
        data_generator = 'linear_ramp_soft_retraction'
        data_configs = {'type': 'ao subtask configuration',
                        'linear ramp start for view 1': None,
                        'linear ramp stop for view 1': None,
                        'linear ramp start for view 2': None,
                        'linear ramp stop for view 2': None,
                        'linear ramp sample number': None,
                        'soft retraction sample number': None}

    # configure other parameteres to this galvanometer configs from the calibration and alignment records.
    voltage_output_terminal = process_configs['device configurations']['nidaq_terminals'] \
        ['scanning galvo']['voltage output terminal']
    home_v1 = process_configs['device configurations']['alignment_records']['scanning galvo'] \
        ['home voltage offset for view 1']
    home_v2 = process_configs['device configurations']['alignment_records']['scanning galvo'] \
        ['home voltage offset for view 2']
    convertion_factor = process_configs['device configurations']['calibration_records'] \
        ['scanning galvo']['distance (um) to voltage (v) conversion factor (v/um)']

    output = \
        {'device': 'scanning_galvo',
         'name': name,
         'task type': 'AO subtask',
         'idle state': 'LOW',
         'voltage output terminal': voltage_output_terminal,
         'home voltage offset for view 1': home_v1,
         'home voltage offset for view 2': home_v2,
         'distance (um) to voltage (v) conversion factor (v/um)': convertion_factor,
         'data for view 1': None,
         'data for view 2': None,
         'data generator': data_generator,
         'data configs': data_configs}

    return output
