

class DaqVoltageProfileBase:
    def __init__(self):
        self.name = 'DAQ voltage profile base class'
        self.sample_number = None
        self.data = None
        self.resting_voltage = None
        # base class do not have an output terminal -
        # give it a sense of "pre-ready" project
        return 0

    def generate_profile(self):
        self.data = None
        return 0


class DaqAOProfile(DaqVoltageProfileBase):
    def __init__(self, ao_terminal=None):
        self.analog_output_terminal = ao_terminal
        return 0


class DaqDOProfile(DaqVoltageProfileBase):
    def __init__(self, do_terminal=None):
        self.digital_output_terminal = do_terminal
        return 0
