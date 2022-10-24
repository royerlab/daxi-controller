from sys import platform
import numpy as np


def getfcn_sinusoidal(configs = None, amplitude = 1, center_voltage = 0, sample_number = 1000, AO_terminal = "cDAQ1AO/ao0"):
    """

    :param configs:
    :param amplitude:
    :param center_voltage:
    :param sample_number:
    :param AO_terminal:
    :return:
    """
    if configs is None:
        # set some example configs
        configs = {}
        configs['name'] = 'sinusoidal funciton'
        configs['amplitude'] = amplitude # voltage
        configs['sample number'] = sample_number  # 
        configs['analog output terminal'] = AO_terminal
        configs['center voltage'] = center_voltage

    N = configs['sample number']
    x = np.arange(0, N)/N
    data = list(configs['amplitude']*np.sin(x*2*np.pi) + configs['center voltage'])
    return data


def getfcn_linear_ramp(configs = None, starting_voltage=0, ending_voltage=0.4, sample_number=500):
    """

    :param configs:
    :param starting_voltage:
    :param ending_voltage:
    :param sample_number:
    :return: data
    """
    if configs is None:
        configs = {'type': 'ao subtask configuration',
                   'name': 'linear ramp function',
                   'sample number': sample_number,
                   'starting voltage': starting_voltage,
                   'ending voltagee': ending_voltage}

    v0 = configs['starting voltage']
    v1 = configs['ending voltagee']
    n = configs['sample number']
    dv = (v1 - v0)/(n - 1)
    data = np.arange(0, n)*dv + v0
    return data


def getfcn_linear_ramp_soft_retraction(confgs = None, 
                                        starting_voltage=0, 
                                        ending_voltage=1, 
                                        sample_number_ramp=500, 
                                        sample_number_retraction=10,
                                        max_ddV=0.1,
                                        buffer_dV=0.1):
    """_summary_

    Args:
        confgs (_type_, optional): configuration dictionary. Defaults to None.
        starting_voltage (int, optional): the starting voltage of the linear ramp. Defaults to 0.
        ending_voltage (int, optional): the ending voltage of the linear ramp. Defaults to 1.
        sample_number_ramp (int, optional): the number of samples on the linear ramp. Defaults to 500.
        sample_number_retraction (int, optional): the number of samples during the soft retraction curve. Defaults to 10.
        max_dV (float, optional): maximum d2V/dt2 between different steps. Defaults to 0.1.
        buffer_dV (float, optional): cusion range for the soft retraction. Defaults to 0.1.
    """
    if configs is None:
        configs = {'type': 'ao subtask configuration',
                   'name': 'linear ramp function with soft retraction',
                   'sample number ramp': sample_number_ramp,
                   'sample number retraction': sample_number_retraction,
                   'starting voltage': starting_voltage,
                   'ending voltagee': ending_voltage,
                   'max delta V per step': max_ddV,
                   'buffer dV': buffer_dV}


# def test_getfcn_linear_ramp():
#     """
#     test function for getfcn_linear_ramp
#     """
#     data=getfcn_linear_ramp(starting_voltage=0, ending_voltage=0.4, sample_number=500)
#     assert isinstance(data, isinstance(data, np.ndarray))
#     assert len(data) == 500
#     assert data[0] == starting_voltage
#     assert data[-1] == ending_voltage


# def test_getfcn_linear_ramp_soft_retraction():
#     data=getfcn_linear_ramp_soft_retraction(
#                                         starting_voltage=0.0, 
#                                         ending_voltage=1.0, 
#                                         sample_number_ramp=500, 
#                                         sample_number_retraction=100,
#                                         max_ddV=0.1,
#                                         buffer_dV=0.1
#                                         ):
#     assert isinstance(data, isinstance(data, np.ndarray)) # returned data has to be an numpy array
#     assert len(data) == 600 # the length of the data should be the sampe of the specified sample number for both ramping and retraction
#     assert data[0] == 0.0 # initial voltage on the ramp should be precisely the starting_voltage
#     assert data[sample_number_ramp-1] == 1.0 # ending voltage on the ramp should be precisely the ending voltage.
#     data2 = np.asarray(list(data)*2) # create both ends of the retraction-ramp connection.
#     dddata = np.gradient(np.gradient(data2)) # caluclate the second order derivative the the voltage profile
#     assert dddata <= 0.1 # make sure the 'acceleration' of the voltage during retraction is smaller than the maximum allowed 'acceleration' ddV
#     assert np.min(data) >= np.min(starting_voltage, ending_voltage) - 0.2 # make sure the ramp is within range.
#     assert np.max(data) <= np.max(starting_voltage, ending_voltage) + 0.2 # make sure the ramp is within range.

