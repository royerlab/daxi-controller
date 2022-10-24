import nidaqmx


# get a metronome
def get_metronome(configs=None, verbose=False, metronome=None,
                  frequency=10,
                  acquisition_type='FINITE',
                  number_of_ticks=10,
                  trigger_source="/cDAQ1/PFI0",
                  trigger_edge='RISING',
                  retriggerable=True,
                  output_terminal="/cDAQ1/Ctr0InternalOutput",
                  counter_channel_str="cDAQ1/_ctr0",
                  idle_state='LOW',
                  metronome_name='demo metronome',
                  task_type='metronome',
                  ):
    # This funciton generates a metronome task based on the input configurations
    #
    # the following is the default config for this metronome"
    if configs is None:
        # the following codes serves as an example to define a configuration dictionary for a metronome.
        # first of all, the metronome is a counter task, and this configs parameter stores all the 
        # specifications for this counter task.
        configs = {}
        configs['name'] = metronome_name
        configs['task type'] = task_type
        configs['idle state'] = idle_state
        configs['frequency'] = frequency  # Hz
        configs['acquisition type'] = acquisition_type
        configs['number of ticks'] = number_of_ticks
        configs['trigger source'] = trigger_source
        configs['trigger edge'] = trigger_edge
        configs['retriggerable'] = retriggerable
        configs['task name'] = 'metronome demo'
        configs['output terminal'] = output_terminal
        configs['counter channel str'] = counter_channel_str  # this is the pysical channle of the counter

    # parse the configuration settings to the corresponding nimxdaq constants.    
    if configs['idle state'] == 'LOW':
        if verbose: print('setting the idle state ...')
        idle_state_const = nidaqmx.constants.Level.LOW
        if verbose: print('idle_state_const is set to be ' + str(idle_state_const))
    elif configs['idle state'] == 'HIGH':
        idle_state_const = nidaqmx.constants.Level.HIGH
        if verbose: print('idle_state_const is set to be ' + str(idle_state_const))
    print('idle_state_const type is ' + str(type(idle_state_const)))

    if configs['acquisition type'] == 'FINITE':
        # FINITE tells the metronome to acquire or generate a finite number of ticks."
        sample_mode_const = nidaqmx.constants.AcquisitionType.FINITE
    elif configs['acquisition type'] == 'CONTINUOUS':
        # CONTINUOUS tells the metronome to acquire or generate ticks until you tell it to stop."
        sample_mode_const = nidaqmx.constants.AcquisitionType.CONTINUOUS

    if configs['trigger edge'] == 'RISING':
        trigger_edge_const = nidaqmx.constants.Slope.RISING
    elif configs['trigger edge'] == 'FALLING':
        trigger_edge_const = nidaqmx.constants.Slope.FALLING

    # now checkout the task
    if metronome is None:
        print('should define metronome and pass it into this function in the future')
        metronome = nidaqmx.Task(configs['task name'])

    try:
        # add a counter output channel to this task
        if verbose: print('adding the counter...')

        metronome.co_channels.add_co_pulse_chan_freq(
            # specify the counter to be used of this task
            configs['counter channel str'],
            # configure the idle state of this counter, 
            # i.e. "Specifies the resting state of the output terminal."
            idle_state=idle_state_const,
            # configure the frequency of the generated pulses. 
            # pulses are equivalent to the ticks of the metronome
            freq=configs['frequency'],
        )
        if verbose: print('counter added.')

        # configure the timing of this metronome (sample mode, and number of samples)
        if verbose: print('setting the metronome timing...')
        metronome.timing.cfg_implicit_timing(
            # sample mode (continuous or finite)
            sample_mode=sample_mode_const,
            # total number of ticks to be produced by the metronome
            samps_per_chan=configs['number of ticks'],
        )
        if verbose: print('metronome timing set.')

        # configure the starting trigger of this metronome
        if verbose: print('configure the metronome trigger source...')
        metronome.triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source=configs['trigger source'],
            trigger_edge=trigger_edge_const,
        )
        if verbose: print('metronome trigger source configured.')

        # configure for the retriggerable property
        if verbose: print('configure the retriggerable property for the metronome')
        metronome.triggers.start_trigger.retriggerable = configs['retriggerable']

        # output
        if verbose: print('successfully configured the metronome.')
    except:
        print('failed')
        metronome.close()
    return metronome


def get_counter(configs=None, verbose=False):
    pass
