import nidaqmx
from daxi.tools.generate_functions import *
# change these into some static data type in the future.

# define metronome configs
metronome_configs={}
metronome_configs['name'] = 'demo metronome'
metronome_configs['type'] = 'metronome'
metronome_configs['idle state'] = 'LOW'
metronome_configs['frequency'] = 1000  # Hz
metronome_configs['acquisition type'] = 'FINITE'
metronome_configs['number of ticks'] = 500
metronome_configs['trigger source'] = "/cDAQ1/PFI0"
metronome_configs['trigger edge'] = 'RISING'
metronome_configs['retriggerable'] = True
metronome_configs['task name'] = 'metronome demo'
metronome_configs['output terminal'] = "/cDAQ1/Ctr0InternalOutput"
metronome_configs['counter channel str'] = "cDAQ1/_ctr0" # this is the pysical channle of the counter

# define ao task bundle settings.
ao_task_bundle = {}
ao_task_bundle['task handle'] = nidaqmx.Task("demo sinusoidal function task")
ao_task_bundle['subtask list'] = []  # this is a list of subtasks
ao_task_bundle['data list'] = []
ao_task_bundle['status - number of subtasks added to the task'] = 0
ao_task_bundle['configs - metronome'] = 0
ao_task_bundle['trigger terminal'] = "/cDAQ1/PFI0"

sinusoidal_configs = {}
sinusoidal_configs['type'] = 'ao subtask configuration'
sinusoidal_configs['name'] = 'sinusoidal funciton'
sinusoidal_configs['amplitude'] = 2 # voltage
sinusoidal_configs['sample number'] = 200  #
sinusoidal_configs['voltage output terminal'] = "cDAQ1AO/ao0"
sinusoidal_configs['center voltage'] = 0
sinusoidal_configs['initial phase'] = 0
sinusoidal_configs['data'] = None
sinusoidal_configs['data generator'] = getfcn_sinusoidal


sinusoidal2_configs = {}
sinusoidal2_configs['type'] = 'ao subtask configuration'
sinusoidal2_configs['name'] = 'sinusoidal funciton v2'
sinusoidal2_configs['amplitude'] = 4 # voltage
sinusoidal2_configs['sample number'] = 200
# The eventual data generated to the ao channel will be determined by the number
# of ticks in the metronome, and this number is the number of samples used to
# sample the function, and it will be used circularly based on the number of
# ticks requested by the metronome.
sinusoidal2_configs['voltage output terminal'] = "cDAQ1AO/ao1"
sinusoidal2_configs['center voltage'] = 0
sinusoidal2_configs['initial phase'] = 0
sinusoidal2_configs['data'] = None
sinusoidal2_configs['data generator'] = getfcn_sinusoidal

print('default configurations imported.')
