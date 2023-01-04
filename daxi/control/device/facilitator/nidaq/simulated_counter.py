import copy
from daxi.control.device.facilitator.nidaq.counter import Counter


class SimulatedCounter(Counter):
    def __init__(self, devices_connected=True, camera=None, camera_id=None):
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
        self.camera = camera
        self.camera_id = camera_id

    def read(self):
        """
        this will read out the current count
        :return:
        returns the current count, int.
        """
        if self.camera is None:
            self.current_count = 0
        else:
            self.current_count = \
                self.camera.devices['camera ' + str(self.camera_id)].current_buffer_index
        return self.current_count
