from old_workbench.daxi_sandbox import *
from time import *
print('import completed')
nsample_AO = 500
# initiate the configuration of a metronome
configs_metronome = init_configs_metronome(name='demo metronome',
                                           frequency=1000,
                                           nticks=500,
                                           trigger_source="/cDAQ1/PFI0",
                                           output_terminal="/cDAQ1/Ctr0InternalOutput",
                                           counter_ch_str="cDAQ1/_ctr0",
                                           )

# initiate the configurations for two sinusoidal functions
configs_sinu1 = init_configs_sinusoidal(subtask_name='sinu1',
                                        amplitude=2,
                                        sample_number=nsample_AO,
                                        voltage_output_terminal="cDAQ1AO/ao0",
                                        center_voltage=0,
                                        initial_voltage=0,
                                        )

configs_sinu2 = init_configs_sinusoidal(subtask_name='sinu2',
                                        amplitude=2,
                                        sample_number=nsample_AO,
                                        voltage_output_terminal="cDAQ1AO/ao1",
                                        center_voltage=0,
                                        initial_voltage=0,
                                        )

# initiate the configuration for one linear ramp function
configs_line1 = init_configs_linear_ramp(subtask_name='linear ramp function',
                                         sample_number=nsample_AO,
                                         voltage_output_terminal="cDAQ1AO/ao2",
                                         starting_voltage=0,
                                         ending_voltage=2,
                                         )

# initiate the configuration of the ao task bundle:
ao_task_bundle = init_configs_ao_taskbundle(trigger_terminal="/cDAQ1/PFI0")

# prepare the task for the metronome based on its configuration:
task_metronome = get_metronome(configs=configs_metronome)

# decorate the ao task bundle with the sinusoidal functions as two subtasks, and the linear ramp as the third subtask.
ao_task_bundle = ao_task_add_subtask(ao_task_bundle=ao_task_bundle, ao_subtask_configs=configs_sinu1)
ao_task_bundle = ao_task_add_subtask(ao_task_bundle=ao_task_bundle, ao_subtask_configs=configs_sinu2)
ao_task_bundle = ao_task_add_subtask(ao_task_bundle=ao_task_bundle, ao_subtask_configs=configs_line1)

# implement the metronome in the ao task bundle
ao_task_bundle = ao_task_implement_metronome(ao_task_bundle=ao_task_bundle, metronome_configs=configs_metronome)

# implement the trigger in the ao task bundle
ao_task_bundle = ao_task_implement_trigger(ao_task_bundle=ao_task_bundle)

# write the data of all ao subtasks to the device
ao_task_write_data(ao_task_bundle=ao_task_bundle)

# start the metronome task:
# after the start, the task enteres a 'stand-by mode', waiting for their trigger to start performing the task.
task_metronome.start()

# start the ao task (all the ao subtasks shall start at the same time, after the metronome is started):
# after the start, the task enteres a 'stand-by mode', waiting for their trigger to start performing the task.
ao_task_bundle['task handle'].start()
print('now tasks are started')

# wait for the user to quit the process
print('enter q to quit...')
while input() != 'q':
    sleep(0.05)

# close up the tasks
# stop the ao_task and the metronome tasks
ao_task_bundle['task handle'].stop()
task_metronome.stop()

# close the ao_task and the metronome tasks
ao_task_bundle['task handle'].close()
task_metronome.close()