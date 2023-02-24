from sys import platform
import numpy as np


def get_soft_retraction(v_start, v_end, n_total):
    """
    this function generate a soft retraction curve that rampls from v0 to v1 over n_total data points.
    the retraction would keep a constant amplitude of acceleration throughout the curve, with inverse signs
    for each half of the curve.

    Parameters
    ----------
    v_start: starting value
    v_end: ending value
    n_total: total number of data points (samples)

    Returns
    -------
    the soft retraction curve with constant amplitude of acceleration but flipped sign in the middle.

    """
    n = np.floor(n_total / 2) - 1  # calculate the half-curve data points, with 1 extra data point of buffer.

    a = (v_end - v_start) / 2 / (n - 1) ** 2  # calculate the acceleration a in equation y(x) = a*x**2 + b
    b = v_start  # calculate the offset b in equation y(x) = a*x**2 + b

    x = np.arange(n)  # prepare location coordiantes
    y = a * x ** 2 + b  # calculate position sequences.

    # patch two segments of the positions to create two segments with flipped acceleration sign.
    ys_mid = list(y[:-1]) + list(-np.flip(y) + 2 * y[-1])
    # prepare an empty vecgor for the final position sequence, and it should end at v1.
    ys = np.ones(n_total) * v_end
    # position should starts at v0
    ys[0] = v_start
    # in the middle we copy over the calculated soft retraction curve
    ys[1:len(ys_mid) + 1] = ys_mid
    return list(ys)


class DAQDataGenerator:
    """
    this is the base class for DAQ data generator classes that generates the data
    profiles to write to the daq task channels.
    """

    def __init__(self):
        self.data = None

    def getfcn_sinusoidal(self,
                          amplitude=1,
                          center_voltage=0,
                          sample_number=1000,
                          sample_number_per_period=None,
                          initial_phase=0):
        """

        Parameters
        ----------
        amplitude
        center_voltage
        sample_number
        sample_number_per_period
        initial_phase

        Returns
        -------

        """
        if sample_number_per_period is None:
            sample_number_per_period = sample_number

        n = sample_number
        x = np.arange(0, n) / sample_number_per_period
        data = list(amplitude * np.sin(x * 2 * np.pi + initial_phase / 180 * np.pi) + center_voltage)
        self.data = data
        return data

    def getfcn_linear_ramp_soft_retraction(self, v0, v1, n_sample_ramp, n_sample_retraction):
        """
        this method produces a linear ramp profile with soft retraction.
        the voltage would first ramp from v0 to v1 in a linear fashion over n_sample_ramp data points,
        after which it will then retract from v1 to v0 with a soft retraction curve over
        n_sample_retraction data points. The soft retraction is designed in a way to have 2 pieces of
        parabolic curves to feature constant and smallest allowable amplitude of acceleration over the
        range of travel for the retraction process.
        Parameters
        ----------
        v0: starting point in the linear ramp segment
        v1: ending point in the linear ramp segment
        n_sample_ramp: number of data points inside the linear ramping segment.
        n_sample_retraction: number of dat points over the retraction segment.


        Returns
        -------
        a list of data points that features the linear ramp + soft retraction curve.
        """
        # first, get the linear ramp part
        self.data = list(np.ones(n_sample_ramp + n_sample_retraction) * v0)
        dv = (v1 - v0) / (n_sample_ramp - 1)
        data_ramp = np.arange(0, n_sample_ramp) * dv + v0
        self.data[:len(data_ramp)] = data_ramp
        # now get the soft retraction part
        data_retraction = get_soft_retraction(v_start=v1, v_end=v0, n_total=n_sample_retraction)
        self.data[len(data_ramp):] = data_retraction
        self.data=list(self.data)
        return self.data

    def getfcn_sequence(self,
                        n_sample_duty_on=None,
                        n_sample_duty_off=None,
                        acquisition_mode=None,
                        n_sequences=None,
                        v_on=None,
                        v_off=None,
                        signal_type='analog',
                        ):
        # todo, implement the sequence data generator. try the following: stop task, rewrite data,
        #  # start task, does the sequence change. how fast can it change
        """

        :param n_sample_duty_on:
        :param n_sample_duty_off:
        :param acquisition_mode:
        :param n_sequences:
        :param v_on:
        :param v_off:
        :return:
        """
        """
        below are just thoughts:
        
        Perhaps, define an acquisition mode (1 of the six as defined in the readme
        at the devicefacilitator level)
        perhaps will need to generate a list of data, and shuffle from the list during operation by 
        the facilitators
        
        perhaps take the input samples, the acquisition modes, and the device type, generate the sequences.
        let's see.
        sequence: 
        assume - onduty = 4 (slices), off duty = 2,
        draw in ppt. 
        
        color: all lasers
        view: VSG1, VSG2, beta, O1, O3.
        
        sequence dependent devices: laser, view switching galvo.
        in the mode 1 - [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
         488 (0/1): 1111-00-|0000-00-|1111-00-|0000-00-|
         561 (0/1): 0000-00-|1111-00-|0000-00-|1111-00-|
        VSG1 (a/b): aaaa-aa-|aaaa-aa-|bbbb-bb-|bbbb-bb-|
        VSG2 (m/n): aaaa-aa-|aaaa-aa-|bbbb-bb-|bbbb-bb-|
        beta (p/q): aaaa-aa-|aaaa-aa-|bbbb-bb-|bbbb-bb-|
        SG-0 (a/b): aaaa-00-|aaaa-00-|bbbb-00-|bbbb-00-|
        gamma  (n): xxxx-00-|xxxx-00-|xxxx-00-|xxxx-00-|
        
        [mode 2] - [layer 1: position] - [layer 2: view] - [layer 3: slice] - [layer 4: color]
        chase over longer distances where each color is chasing the same segment on the sample but different segment 
        reletive to the stage.
        
        always repeat for each slice devices
        scanning
        
        """
        if signal_type == 'digital':
            v_on = True
            v_off = False

        a = [v_on] * n_sample_duty_on
        b = [v_off] * n_sample_duty_off
        self.data = a + b
        return self.data

    def constant(self,
                 n_samples=None,
                 constant=None
                 ):

        self.data = np.ones(n_samples) * constant
        return self.data

    def on_off_sequence(self,
                        n_samples_on=None,
                        n_samples_off=None,
                        on_value=None,
                        off_value=None):
        self.data = [on_value] * n_samples_on + [off_value] * n_samples_off
        return self.data
