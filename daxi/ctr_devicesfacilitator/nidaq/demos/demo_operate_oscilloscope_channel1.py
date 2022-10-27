# This file provides a demonstration of how to configure an AO output terminal on daq card to generate sinusoidal wave.
# The daq card should be waiting for a trigger sent from the camera.
# we wire the terminal on a oscilloscope, and you should see the sinusoidal wave being generated witht he camera output
# trigger signal.
#
# This demo is implemented without awareness of the device facilitator, and it can serve as an example to configure
# devicefacilitator methods.
#
# we expect each "operation" to be defined as methods in the facilitators' level.

from daxi.ctr_devicesfacilitator.nidaq.nidaq import Metronome, TaskBundleAO, SubTaskAO
from daxi.ctr_devicesfacilitator.nidaq.devicetools.generate_functions import DAQDataGenerator
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools_needbettername.constants import virtual_tools_configs_path
from time import sleep


# get configuration of the oscilloscope_chanenl1.
p1 = NIDAQConfigsParser()
p1.set_configs_path(virtual_tools_configs_path)
scope1_configs = p1.get_oscilloscope1_configs()

# get configuration for the metronome
p2 = NIDAQConfigsParser()
p2.set_configs_path(virtual_tools_configs_path)
metronome_configs = p2.get_metronome_configs()

# get configuration for the ao task bundle
p3 = NIDAQConfigsParser()
p3.set_configs_path(virtual_tools_configs_path)
section = 'Physical Devices Section'
keyword = 'AO_task_bundle'
task_bundle_ao_configs = \
    p3.get_configs_by_path_section_keyword(section, keyword)

# 2. prepare the subtask
subtask = SubTaskAO(scope1_configs)

# now we know this subtask data generator is sinusoidal
dg = DAQDataGenerator()
data_configs = scope1_configs['data configs']
subtask.data = dg.getfcn_sinusoidal(amplitude=data_configs['amplitude'],
                                    center_voltage=data_configs['center voltage'],
                                    sample_number=data_configs['sample number'],
                                    initial_phase=data_configs['initial phase'],
                                    )

# 3. get metronome for task bundle
metronome = Metronome()
metronome.set_configurations(metronome_configs)
metronome.get_ready()

# 4. prepare AO task bundle

# prepare the object
taskbundle_ao = TaskBundleAO()

# set the ao task bundle configurations
taskbundle_ao.set_configurations(task_bundle_ao_configs, metronome)

# add metronome
taskbundle_ao.add_metronome(metronome)

# add sub-task
taskbundle_ao.add_subtask(subtask)

# configure sub-task data generator (this action would be organized into a manager class)

# taskbundle_ao get ready
taskbundle_ao.get_ready()

# start
metronome.start()
taskbundle_ao.start()
# wait for the user to quit the process
print('enter q to quit...')
while input() != 'q':
    sleep(0.05)

taskbundle_ao.close()
metronome.close()
