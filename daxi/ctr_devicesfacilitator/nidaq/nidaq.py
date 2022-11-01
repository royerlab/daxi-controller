# general description:
import nidaqmx
from daxi.ctr_devicesfacilitator.nidaq.devicetools.generate_functions import DAQDataGenerator

"""
    To manage the DAQ card controlled devices, we have the module level manager class defined as the DAQDeviceManager
    class. 

    DAQDeviceManager interfaces with many "bundles of tasks" defined by the TaskBundle class. And is responsible for 
    verifying and firing the DAQ card.
    A "bundle of tasks" manages a series of "sub tasks", for which we define as the SubTask. 
    A series of SubTask shall be attached to a TaskBundle object as attributes.
    
    A TaskBundle object configures (instead of performs) the connection and wiring with and across the SubTasks objects 
    
    Different types of task bundles shall be implemented as child classes of the TaskBundle class.
    Different types of sub tasks shall be implemented as child classes of the SubTask class.
    
    # todo need a "swap data" method for the daq task bundles (think about it). so it changes 
    with the change of [laser id, view id, acquisition mode]. but one set is one cycle.
"""


def _get_nidaqmx_constants(type, value):
    if type == 'sample mode':
        if value == 'FINITE':
            constant = nidaqmx.constants.AcquisitionType.FINITE
        if value == 'CONTINUOUS':
            constant = nidaqmx.constants.AcquisitionType.CONTINUOUS

    if type == 'trigger edge':
        if value == 'RISING':
            constant = nidaqmx.constants.Slope.RISING
        if value == 'FALLING':
            constant = nidaqmx.constants.Slope.FALLING

    return constant


class SubTask:
    """
    todo
    This is a class for configuring a single "sub task".

    Different types of sub task bundles shall be implemented
    as child class of TaskBundle

    Two types of sub tasks are implemented:
        1. SubTaskAO for AO sub task.
        2. SubTaskDO for DO sub task.

    What to include in the child class:
        1. the specific condiguration handles? but it shoudl be done with the AO task handle I guess.

    Required information to be included as attributes
        2. device to be controlled : str
        3. data profile: numpy.array
        4. data profile generator function
        5. data profile configuration
        6. number of samples
        7. sample rate
        8. trigger_source_terminal: (good redundancy).
        9. trigger_edge

    Manager's responsibility for a sub task in terms of pre-performance inspection:
        1. check that output terminal is configured for the device this subtask controls
        2. check that trigger terminal is configured to the metronome output terminal
        3. check that the data generator is valid.
        4. make sure the data profile length matches with the number of samples.
        5. make sure the number of samples matches with the metronome trigger train length.
        6. make sure the sample rate, metronome sampling frequency matches up.

    """

    def __init__(self):
        self.device: str  # device to be controlled
        self.name: str
        self.data: list  # data profile
        self.data_generator: DAQDataGenerator  # DataGenerator should be a base class for all DAQDataGenerator
        self.data_configuration: dict  # input parameter for the data generation method.
        self.sample_number: int  # number of samples to be used in the sub task.
        self.sample_rate: float  # sampling rate (Hz)
        self.trigger_source_terminal: str
        self.trigger_edge: str  # rising or falling.
        self.idle_state: str
        "open floor..."


class TaskBundle:
    def __init__(self):
        self.name = None, str  # name of the AO or DO task (a bundle)
        self.task_handle = None
        self.sub_tasks = []  # a list of SubTask objects.
        self.data_list = []
        self.trigger_terminal = None
        self.trigger_edge = None
        self.metronome = None
        self.sample_mode = None

    def set_configurations(self, task_bundle_configs):
        self.name = task_bundle_configs['name']
        self.trigger_terminal = task_bundle_configs['trigger terminal']
        self.trigger_edge = task_bundle_configs['trigger edge']
        self.sample_mode = task_bundle_configs['sample mode']

    def add_metronome(self, metronome):
        self.metronome = metronome

    def add_subtask(self, subtask):
        """
        append the subtask to the list of subtasks of this object.
        We expect the manager to get a series of subtasks from elsewhere,
        and append it to the bundle.
        The same format applies to both AO and DO task bundles and the
        associated subtasks.
        Parameters
        ----------
        subtask

        Returns
        -------

        """
        self.sub_tasks.append(subtask)

    def get_ready(self):
        """
        This method has to be implemented for AO and DO task bundles specifically.
        Returns
        -------

        """
        pass

    def start(self):
        self.task_handle.start()

    def stop(self):
        self.task_handle.stop()

    def close(self):
        self.task_handle.close()


class TaskBundleAO(TaskBundle):
    """
    This is a class for configuring the AO task bundles.
    """

    def get_ready(self):
        """
        1. prepare the task bundle task object
        2. configure timing, triggering ,etc. (check the correct order)
        3. add channels
        4. calculate data
        5. writes data.
        % should subtask calculate the data? Or should the manger
        call the data generator to calculate the data?
        it would be better when the manager says go, the data is already
        prepared somewhere. Because that allows for modification of the data
        without the manager's attention.

        Returns
        -------

        """
        # 1, checkout a task
        self.task_handle = nidaqmx.Task(self.name)

        # 2, decorate the ao task bundle with its subtasks
        for sub_task in self.sub_tasks:
            self.task_handle.ao_channels.add_ao_voltage_chan(
                sub_task.configs['voltage output terminal']
            )

        # 3, implement the metronome to the ao task bundle
        # todo - check if the following is true, metronome has to be FINITE,
        #  but taskbundle has to be continuous
        self.task_handle.timing.cfg_samp_clk_timing(
            rate=self.metronome.frequency,
            source=self.metronome.counting_output_terminal,  #
            sample_mode=_get_nidaqmx_constants(type='sample mode', value=self.sample_mode),  #
        )

        # 4, implement trigger to the ao task bundle (this is specific to ao)
        self.task_handle.triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source=self.trigger_terminal,
            trigger_edge=_get_nidaqmx_constants(type='trigger edge', value=self.trigger_edge)
        )

        # 5, write data of all ao sub_task to the device
        for sub_task in self.sub_tasks:
            self.data_list.append(sub_task.generate_data())

        if len(self.data_list) == 1:
            self.task_handle.write(self.data_list[0])

        if len(self.data_list) > 1:
            self.task_handle.write(self.data_list)


class TaskBundleDO(TaskBundle):
    """
    This is a class for configuring the DO task bundls.
    note that for DO task bundles, there is no need for
    configuring the trigger in the 'get_ready' method

    """

    def get_ready(self):
        # 1. checkout a task (same with ao)
        self.task_handle = nidaqmx.Task(self.name)

        # 2, decorate the do task bundle with its subtasks (special for do)
        for sub_task in self.sub_tasks:
            self.task_handle.do_channels.add_do_chan(
                sub_task.configs['voltage output terminal']
            )

        # 3, implement the metronome to the do task bundle (same with ao)
        self.task_handle.timing.cfg_samp_clk_timing(
            rate=self.metronome.frequency,
            source=self.metronome.counting_output_terminal,  #
            sample_mode=_get_nidaqmx_constants(type='sample mode', value=self.sample_mode),  #
        )

        # Note! DO task do not need trigger.

        # 5. write data of all do subtasks to the device (same with ao)
        for sub_task in self.sub_tasks:
            self.data_list.append(sub_task.generate_data())

        if len(self.data_list) == 1:
            self.task_handle.write(self.data_list[0])

        if len(self.data_list) > 1:
            self.task_handle.write(self.data_list)


class SubTaskAO(SubTask):
    """
    This is the base class for all ao sub tasks.
    An SubTaskAO parses information from the data acquisition configurations, and populate up the pre-set attributes
    that stores the desired information

    There can be different objects of this task, examples include:
     1. a sinusoidal function generator
     2. draws a raster scanning line for the scanning galvo
     3. draws an improved raster scanning line profile for the scanning galvo with soft retraction profile
     4. draws a profile to have uniform brightness for the strip reduction galvo
    etc.
    the devicefacilitator would configure the specific objects of this subtask

    Different types of the AO sub_tasks shall be implemented as the child class of this AOSubTaskBase class.

    Content to be included in this AOSubTaskBase:
        Everything from the SubTask class.


    """

    def __init__(self, subtask_configs):
        super().__init__()
        self.configs = subtask_configs
        self.data_generator = subtask_configs['data generator']
        self.data_configs = subtask_configs['data configs']
        self.data = None
        self.name = subtask_configs['name']
        self.device = subtask_configs['device']

    def generate_data(self):
        """this is a method to get the subtask ready
        todo: think about the following:
        does a sub task object needs to get_ready handle? perhaps yes, because it needs to generate data.
        the devicesfacilitator would configure all the subtask objects, and get them ready, etc.
        But perhaps only generate_data is really required in this "get ready" action, so why not call
        just it generate_data? keep thinking about it.
        """
        print(self.data_generator)
        if self.data_generator == 'sinusoidal':
            dg = DAQDataGenerator()
            data = dg.getfcn_sinusoidal(
                amplitude=self.data_configs['amplitude'],
                center_voltage=self.data_configs['center voltage'],
                sample_number=self.data_configs['sample number'],
                sample_number_per_period=self.data_configs['sample number per period'],
                initial_phase=self.data_configs['initial phase'])
            self.data = data

        if self.data_generator == 'linear_ramp_soft_retraction':
            dg = DAQDataGenerator()
            data = dg.getfcn_linear_ramp_soft_retraction(
                v0=self.data_configs['linear ramp start'],
                v1=self.data_configs['linear ramp stop'],
                n_sample_ramp=self.data_configs['linear ramp sample number'],
                n_sample_retraction=self.data_configs['soft retraction sample number'])
            self.data = data

        if self.data_generator == 'sequence':
            dg = DAQDataGenerator()
            data = dg.getfcn_sequence(n_sample_duty_on=self.data_configs['on-duty sample number'],
                                      n_sample_duty_off=self.data_configs['off-duty sample number'],
                                      acquisition_mode=self.data_configs['on-duty sample number'],
                                      n_sequences=self.data_configs['number of options for the sequence'],
                                      v_on=self.data_configs['voltage on'],
                                      v_off=self.data_configs['voltage off'])

            # todo - implement this function. see DAQDataGenerator comments for thoughts.
            self.data = data

        return data


class SubTaskDO(SubTask):
    """
    This is the base class for do sub tasks.
    An SubTaskDO parses information from the data acquisition configurations, and populate up the pre-set attributes
    that stores the desired information

    There can be different types of do SubTask, examples include:
     1. control laser on/off
     2. different choices of other stuff....

    etc.

    Different types of the AO sub_tasks shall be implemented as the child class of this AOSubTaskBase class.

    Content to be included in this AOSubTaskBase:
        Everything from the SubTask class.

    """

    def __init__(self, subtask_configs):
        super().__init__()
        self.configs = subtask_configs
        self.data_generator = subtask_configs['data generator']
        self.data_configs = subtask_configs['data configs']
        self.data = None
        self.name = subtask_configs['name']
        self.device = subtask_configs['device']

    def generate_data(self):
        dg = DAQDataGenerator()
        data = dg.getfcn_sequence(n_sample_duty_on=self.data_configs['on-duty sample number'],
                                  n_sample_duty_off=self.data_configs['off-duty sample number'],
                                  acquisition_mode=self.data_configs['on-duty sample number'],
                                  n_sequences=self.data_configs['number of options for the sequence'],
                                  signal_type='digital')
        self.data = data
        return self.data


class Counter:
    """
    This is a counter task, it does not have sub tasks.
    It counts.
    It is essentially a CI task with interface for the daxi managers.
    you can use it to count the number of slices, volumes, loops, etc.
    """

    def __init__(self):
        self.name = None, str  # this should be the name of this counter
        self.counter_terminal = None, str  # this should be a counter terminal string from the DAQ card.
        self.task_handle = None  # this should be an nidaqmx.task.Task object
        self.counting_input_terminal = None, str  # this should be the signal to be counted.
        self.counting_edge = None, str
        self.initial_count = None, int  # this should be the the initial count.
        self.purpose = None, str  # should provide a description of the purpose of this counter.
        self.current_count = None, int  # this will be
        self.verbose = None, bool  # display output message or not.

    def set_configurations(self, counter_configs):
        """
        it will take the counter_configs dictionary from its manager.
        Keep in mind, the Counter class do not interface with pasers.
        :param counter_configs: dict.
        :return: None
        """
        self.name = counter_configs['name']
        self.counter_terminal = counter_configs['counter terminal']
        self.task_handle = None  # this task handle will be created at aself.get_ready()
        self.counting_input_terminal = counter_configs['counting input terminal']
        self.counting_edge = counter_configs['counting edge']
        self.initial_count = counter_configs['initial count']
        self.purpose = counter_configs['purpose']
        self.current_count = counter_configs['current count']
        self.verbose = counter_configs['verbose']

    def get_ready(self):
        """
        This will actually create the counter.
        :return:
        it returns 0 when the process is successful.
        """
        # checkout a task
        self.task_handle = nidaqmx.Task(self.name)

        # configure counter and the counting edge type
        if self.counting_edge == 'RISING':
            ctr = self.task_handle.ci_channels.add_ci_count_edges_chan(
                self.counter_terminal, edge=nidaqmx.constants.Edge.RISING
            )

        if self.counting_edge == 'FALLING':
            ctr = self.task_handle.ci_channels.add_ci_count_edges_chan(
                self.counter_terminal, edge=nidaqmx.constants.Edge.FALLING
            )

        # configure the input signal to count
        ctr.ci_count_edges_term = self.counting_input_terminal

    def start(self):
        """
        this starts the counter
        :return:
        it returns 0 when the process was successful.
        """
        self.task_handle.start()

    def read(self):
        """
        this will read out the current count
        :return:
        returns the current count, int.
        """
        self.current_count = self.task_handle.read()
        return self.current_count

    def stop(self):
        """
        this stops the counter
        :return:
        it returns 0 when the process is successful.
        """
        self.task_handle.stop()

    def close(self):
        """
        this closes the counter
        it returns 0 when the process is successful.
        :return:
        """
        self.task_handle.close()


class Metronome:
    """
    This is a Metronome class.
    """

    def __init__(self):
        self.name = None, str  # this should be the name of the metronome
        self.counter_terminal = None, str  # this should be a counter terminal string from the DAQ card.
        self.counting_output_terminal = None, str  # this is the internal output terminal for other objects to use.
        self.task_handle = None  # this should be an nidaqmx.task.Task object
        self.idle_state = None, str  # 'LOW' or 'HIGH'
        self.frequency = None, float  # frequency of the output ticks
        self.sample_mode = None, str  # 'FINITE' or 'CONTINUOUS'
        self.number_of_samples = None, int  # this is the number of ticks to output
        self.trigger_terminal = None, str  # this should be the signal to trigger the output counter.
        self.trigger_edge = None, str  # 'RISING' or 'FALLING'
        self.retriggerable = None, bool  #
        self.purpose = None, str  # should provide a description of the purpose of this counter.

    def set_configurations(self, metronome_configs):
        """
        it takes the metronome_configs handed over by its manager, and populate it up to its attributes.
        Keep in mind, metronome class do not interface with the parser.
        :param metronome_configs: dict.
        :return: None
        """
        self.name = metronome_configs['name']
        self.counter_terminal = metronome_configs['counter terminal']
        self.counting_output_terminal = metronome_configs['counting output terminal']
        self.idle_state = metronome_configs['idle state']
        self.frequency = metronome_configs['frequency']
        self.sample_mode = metronome_configs['sample mode']
        self.number_of_samples = metronome_configs['number of samples']
        self.trigger_terminal = metronome_configs['trigger terminal']
        self.retriggerable = metronome_configs['retriggerable']
        self.purpose = metronome_configs['purpose']
        self.trigger_edge = metronome_configs['trigger edge']

    def get_ready(self):
        """
        This will create the metronome (an output counter)
        :return:
        it returns 0 when the process is successful.
        """
        # figure out constantsL
        # parse the configuration settings to the corresponding nimxdaq constants.
        if self.idle_state == 'LOW':
            idle_state_const = nidaqmx.constants.Level.LOW
        elif self.idle_state == 'HIGH':
            idle_state_const = nidaqmx.constants.Level.HIGH

        if self.sample_mode == 'FINITE':
            # FINITE tells the metronome to acquire or generate a finite number of ticks."
            sample_mode_const = nidaqmx.constants.AcquisitionType.FINITE
        elif self.sample_mode == 'CONTINUOUS':
            # CONTINUOUS tells the metronome to acquire or generate ticks until you tell it to stop."
            sample_mode_const = nidaqmx.constants.AcquisitionType.CONTINUOUS

        if self.trigger_edge == 'RISING':
            trigger_edge_const = nidaqmx.constants.Slope.RISING
        elif self.trigger_edge == 'FALLING':
            trigger_edge_const = nidaqmx.constants.Slope.FALLING

        # checkout a counter task for this metronome
        self.task_handle = nidaqmx.Task(self.name)

        # add the channel to the metronome
        self.task_handle.co_channels.add_co_pulse_chan_freq(
            self.counter_terminal,
            idle_state=idle_state_const,
            freq=self.frequency
        )

        # configure metronome timing:
        self.task_handle.timing.cfg_implicit_timing(
            sample_mode=sample_mode_const,
            samps_per_chan=self.number_of_samples,
        )

        # configure metronome trigger
        self.task_handle.triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source=self.trigger_terminal,
            trigger_edge=trigger_edge_const,
        )
        # self.task_handle.triggers.start_trigger.retriggerable = self.retriggerable
        self.task_handle.triggers.start_trigger.retriggerable = True

    def start(self):
        """
        this starts the metronome, it will enter a stand-by mode and start to putput ticks upon receival of a trigger.
        :return:
        it returns 0 when the process is successful.
        """
        self.task_handle.start()

    def stop(self):
        """
        this stops the metronome.
        :return:
        """
        self.task_handle.stop()

    def close(self):
        """
        this closes the metronome
        :return:
        """
        self.task_handle.close()

