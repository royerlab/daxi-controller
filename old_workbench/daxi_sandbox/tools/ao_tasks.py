import nidaqmx


def ao_task_implement_metronome(ao_task_bundle, metronome_configs):
    # add the timing options to the ao task.
    # analogous to implementing the metronome to the ao task bundle.
    ao_task_bundle['task handle'].timing.cfg_samp_clk_timing(
         rate=metronome_configs['frequency'],
         source=metronome_configs['output terminal'], # make the ao timing to be triggerd by the output of the retriggerable counter.
         sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
     )
    return ao_task_bundle


def ao_task_add_subtask(ao_task_bundle, ao_subtask_configs):
    # add a subtask configuration to the ao task channel. and configure the task.
    # generate a sinusoidal function based on the configs.
    # tentative: perhaps use this as a type of 'decorator' function that decorates the "configs" dictionary.
    #
    # first, store a local copy of the subtask configuration to the ao_task_configs
    ao_task_bundle['subtask list'].append(ao_subtask_configs)
    #
    # sanity check:
    # 1. the sampling rate for each channel has to be the same with the grand sampling rate of the ao.
    # 2. the sampling rate of the ao task should be the same with the metronome.
    # 3. check all the terminals and make sure the "wiring" of the terminmals makes sense.
    # 4. number of ticks on the metronome should be the same for the sample.
    # -- open floor --
    #
    # now add the subtask to the task
    #
    # - add the ao channel
    ao_task_bundle['task handle'].ao_channels.add_ao_voltage_chan(ao_subtask_configs['voltage output terminal'])
    # - make sure the data is not None
    if ao_subtask_configs['data'] is None:
        try:
            ao_subtask_configs['data'] = ao_subtask_configs['data generator'](ao_subtask_configs)
        except:    
            raise ValueError('the data of this subtask is not generated yet. '
                             'Properly configure the data for this subtask before adding it to the task bundle.')
    
    # - append the data to the data list
    ao_task_bundle['data list'].append(ao_subtask_configs['data']) # data for this subtask.
    return ao_task_bundle  # returns the updated ao_task_configs dict.


def ao_task_implement_trigger(ao_task_bundle):
    """_summary_

    Args:
        ao_task_bundle (_type_): _description_
    """
    if ao_task_bundle['trigger edge'] == 'RISING':
        ao_task_bundle['task handle'].triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source=ao_task_bundle['trigger terminal'], trigger_edge=nidaqmx.constants.Slope.RISING
        )
    
    if ao_task_bundle['trigger edge'] == 'FALLING':
        ao_task_bundle['task handle'].triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source=ao_task_bundle['trigger terminal'], trigger_edge=nidaqmx.constants.Slope.FALLING
        )
    return ao_task_bundle
    

def ao_task_write_data(ao_task_bundle):
    """_summary_

    Args:
        ao_task_bundle (_type_, optional): _description_. Defaults to ao_task_bundle.
    """
    # write the data of all the ao subtasks to all the ao channels
    if len(ao_task_bundle['subtask list']) == 1:
        ao_task_bundle['task handle'].write(ao_task_bundle['data list'][0])

    if len(ao_task_bundle['subtask list']) > 1:
        ao_task_bundle['task handle'].write(ao_task_bundle['data list'])