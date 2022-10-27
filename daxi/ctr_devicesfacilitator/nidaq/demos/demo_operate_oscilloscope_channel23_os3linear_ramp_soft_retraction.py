# 1. get configurations for oscilloscope channel 1
# 2. get configurations for oscilloscope channel 2
# 3. get configurations for scanning galvo, and configure it to have linear ramp soft retraction voltage curve.

from daxi.ctr_devicesfacilitator.nidaq.nidaq import Metronome, TaskBundleAO, SubTaskAO
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools_needbettername.constants import virtual_tools_configs_path
from time import sleep

# todo edit this into a demo, after device facilitator class is done.

# 1. get configurations
p = NIDAQConfigsParser()
p.set_configs_path(virtual_tools_configs_path)

scope2_configs = \
    p.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                          keyword="oscilloscope_channel2")
scope3_configs = \
    p.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                          keyword="oscilloscope_channel3")
metronome_configs = \
    p.get_configs_by_path_section_keyword(section='Virtual Tools Section',
                                          keyword="metronome")
SG_configs = \
    p.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                          keyword="scanning_galvo_soft_retraction")
task_bundle_ao_configs = \
    p.get_configs_by_path_section_keyword(section='Physical Devices Section',
                                          keyword="AO_task_bundle")

# 2. prepare the subtasks and calcualte the data for all subtasks.
st1 = SubTaskAO(scope2_configs)
st1.generate_data()

st2 = SubTaskAO(scope3_configs)
st2.generate_data()

st3 = SubTaskAO(SG_configs)
st3.generate_data()

# 3. prepare metronome for task bundle
metronome = Metronome()
metronome.set_configurations(metronome_configs)

# 4. prepare AO task bundle
taskbundle_ao = TaskBundleAO()
taskbundle_ao.set_configurations(task_bundle_ao_configs)

# 5. add metronome to ao task bundle
taskbundle_ao.add_metronome(metronome)

# 6. add sub-tasks
taskbundle_ao.add_subtask(st1)
taskbundle_ao.add_subtask(st2)
taskbundle_ao.add_subtask(st3)

# 7. taskbundle_ao and metronome get ready (sequence of the two does not matter)
taskbundle_ao.get_ready()
metronome.get_ready()

# 8. start the concert
metronome.start()
taskbundle_ao.start()

# 9. wait for the user to quit the process
print('enter q to quit...')
while input() != 'q':
    sleep(0.05)
# 10. end
taskbundle_ao.close()
metronome.close()
