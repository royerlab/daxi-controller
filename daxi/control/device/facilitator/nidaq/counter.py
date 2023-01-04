import nidaqmx


class Counter:
    """
    This is a counter task, it does not have sub tasks.
    It counts.
    It is essentially a CI task with interface for the daxi managers.
    you can use it to count the number of slices, volumes, loops, etc.
    """

    def __init__(self, devices_connected=True):
        self.name = None, str  # this should be the name of this counter
        self.counter_terminal = None, str  # this should be a counter terminal string from the DAQ card.
        self.task_handle = None  # this should be an nidaqmx.task.Task object
        self.counting_input_terminal = None, str  # this should be the signal to be counted.
        self.counting_edge = None, str
        self.initial_count = None, int  # this should be the the initial count.
        self.purpose = None, str  # should provide a description of the purpose of this counter.
        self.current_count = None, int  # this will be
        self.verbose = None, bool  # display output message or not.
        self.devices_connected = devices_connected
        self.status = 'counter initiated'

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
        if self.devices_connected:
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
        else:
            self.status = 'counter ready'

    def start(self):
        """
        this starts the counter
        :return:
        it returns 0 when the process was successful.
        """
        if self.devices_connected:
            self.task_handle.start()
        else:
            self.status = 'counter started'

    def read(self):
        """
        this will read out the current count
        :return:
        returns the current count, int.
        """
        if self.devices_connected:
            self.current_count = self.task_handle.read()
        else:
            self.current_count = 0

        return self.current_count

    def stop(self):
        """
        this stops the counter
        :return:
        it returns 0 when the process is successful.
        """
        if self.devices_connected:
            self.task_handle.stop()
        else:
            self.status = 'counter stopped'

    def close(self):
        """
        this closes the counter
        it returns 0 when the process is successful.
        :return:
        """
        if self.devices_connected:
            self.task_handle.close()
        else:
            self.status = 'counter closed'
