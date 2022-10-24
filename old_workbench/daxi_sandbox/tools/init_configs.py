import nidaqmx
from old_workbench.daxi_sandbox.tools.generate_functions import *


# change these into some static data type in the future.


# define metronome configs
def init_configs_metronome(name='demo metronome',
                           frequency=1000,
                           nticks=500,
                           trigger_source="/cDAQ1/PFI0",
                           output_terminal="/cDAQ1/Ctr0InternalOutput",
                           counter_ch_str="cDAQ1/_ctr0",
                           ):
    """

    Parameters
    ----------
    name
    frequency
    nticks
    trigger_source
    output_terminal
    counter_ch_str

    Returns
    -------

    """
    metronome_configs = {}
    metronome_configs['name'] = name
    metronome_configs['type'] = 'metronome'
    metronome_configs['idle state'] = 'LOW'
    metronome_configs['frequency'] = frequency  # Hz
    metronome_configs['acquisition type'] = 'FINITE'
    metronome_configs['number of ticks'] = nticks
    metronome_configs['trigger source'] = trigger_source
    metronome_configs['trigger edge'] = 'RISING'
    metronome_configs['retriggerable'] = True
    metronome_configs['task name'] = 'metronome demo'
    metronome_configs['output terminal'] = output_terminal
    metronome_configs['counter channel str'] = counter_ch_str  # this is the pysical channle of the counter
    return metronome_configs


# define ao task bundle settings.
def init_configs_ao_taskbundle(trigger_terminal="/cDAQ1/PFI0"):
    ao_task_bundle = {}
    ao_task_bundle['task handle'] = nidaqmx.Task("demo sinusoidal function task")
    ao_task_bundle['subtask list'] = []  # this is a list of subtasks
    ao_task_bundle['data list'] = []
    ao_task_bundle['status - number of subtasks added to the task'] = 0
    ao_task_bundle['configs - metronome'] = 0
    ao_task_bundle['trigger terminal'] = trigger_terminal
    ao_task_bundle['trigger edge'] = 'RISING'
    print('ao task bundle type is ' + str(type(ao_task_bundle)))
    return ao_task_bundle


def init_configs_sinusoidal(subtask_name='sinusoidal function',
                            amplitude=2,
                            sample_number=500,
                            voltage_output_terminal="cDAQ1AO/ao0",
                            center_voltage=0,
                            initial_voltage=0,
                            ):
    sinusoidal_configs = {}
    sinusoidal_configs['type'] = 'ao subtask configuration'
    sinusoidal_configs['name'] = subtask_name
    sinusoidal_configs['amplitude'] = amplitude  # voltage
    sinusoidal_configs['sample number'] = sample_number  #
    sinusoidal_configs['voltage output terminal'] = voltage_output_terminal
    sinusoidal_configs['center voltage'] = center_voltage
    sinusoidal_configs['initial phase'] = initial_voltage
    sinusoidal_configs['data generator'] = getfcn_sinusoidal
    sinusoidal_configs['data'] = getfcn_sinusoidal(sinusoidal_configs)
    return sinusoidal_configs


def init_configs_linear_ramp(subtask_name='linear ramp function',
                             sample_number=500,
                             voltage_output_terminal="cDAQ1AO/ao3",
                             starting_voltage=0,
                             ending_voltage=0.5,
                             ):
    linear_ramp_configs = {}
    linear_ramp_configs['type'] = 'ao subtask configuration'
    linear_ramp_configs['name'] = subtask_name
    linear_ramp_configs['sample number'] = sample_number  #
    linear_ramp_configs['voltage output terminal'] = voltage_output_terminal
    linear_ramp_configs['starting voltage'] = starting_voltage
    linear_ramp_configs['ending voltagee'] = ending_voltage
    linear_ramp_configs['data generator'] = getfcn_linear_ramp
    linear_ramp_configs['data'] = getfcn_linear_ramp(linear_ramp_configs)
    # update the ending voltage to make it precise.

    return linear_ramp_configs


print('default configurations imported.')
