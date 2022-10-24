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
from daxi.globals_configs_constants_general_tools.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools.constants import virtual_tools_configs_path
from time import sleep

# get configuration of the oscilloscope_channel1.
p11 = NIDAQConfigsParser()
p11.set_configs_path(virtual_tools_configs_path)
scope1_configs = p11.get_oscilloscope1_configs()

p12 = NIDAQConfigsParser()
p12.set_configs_path(virtual_tools_configs_path)
scope2_configs = p12.get_oscilloscope2_configs()

p13 = NIDAQConfigsParser()
p13.set_configs_path(virtual_tools_configs_path)
scope3_configs = p13.get_oscilloscope3_configs()

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
subtask1 = SubTaskAO(scope1_configs)
subtask2 = SubTaskAO(scope2_configs)
subtask3 = SubTaskAO(scope3_configs)

# now we know this subtask data generator is sinusoidal
dg = DAQDataGenerator()
data_configs1 = scope1_configs['data configs']
subtask1.data = dg.getfcn_sinusoidal(amplitude=data_configs1['amplitude'],
                                     center_voltage=data_configs1['center voltage'],
                                     sample_number=data_configs1['sample number'],
                                     sample_number_per_period=data_configs1['sample number per period'],
                                     initial_phase=data_configs1['initial phase'],
                                     )

dg = DAQDataGenerator()
data_configs2 = scope2_configs['data configs']
subtask2.data = dg.getfcn_sinusoidal(amplitude=data_configs2['amplitude'],
                                     center_voltage=data_configs2['center voltage'],
                                     sample_number=data_configs2['sample number'],
                                     sample_number_per_period=data_configs2['sample number per period'],
                                     initial_phase=data_configs2['initial phase'],
                                     )

dg = DAQDataGenerator()
data_configs3 = scope3_configs['data configs']
subtask3.data = dg.getfcn_sinusoidal(amplitude=data_configs3['amplitude'],
                                     center_voltage=data_configs3['center voltage'],
                                     sample_number=data_configs3['sample number'],
                                     sample_number_per_period=data_configs3['sample number per period'],
                                     initial_phase=data_configs3['initial phase'],
                                     )

# 3. get metronome for task bundle
metronome = Metronome()
metronome.set_configurations(metronome_configs)

# 4. prepare AO task bundle
# prepare the object
taskbundle_ao = TaskBundleAO()

# set the ao task bundle configurations
taskbundle_ao.set_configurations(task_bundle_ao_configs)

# add metronome
taskbundle_ao.add_metronome(metronome)

# add sub-tasks
taskbundle_ao.add_subtask(subtask1)
taskbundle_ao.add_subtask(subtask2)
taskbundle_ao.add_subtask(subtask3)

# taskbundle_ao and metronome get ready (sequence of the two does not matter)
taskbundle_ao.get_ready()
metronome.get_ready()

# start (sequence of the two does not matter)
taskbundle_ao.start()
metronome.start()

# wait for the user to quit the process
print('enter q to quit...')
while input() != 'q':
    sleep(0.05)

taskbundle_ao.close()
metronome.close()
