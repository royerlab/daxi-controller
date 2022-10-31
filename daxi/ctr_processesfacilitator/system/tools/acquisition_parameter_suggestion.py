import numpy as np


class AcqParamBase:
    """
    Below are random bits of thoughts - talking to myself.

    perhaps this should be the base class for acquisition tools
    then each acquisition mode would be the child class of this class.
    For this base class, it is estimating the parameter combinations for 1 laser, 1 view.
    uhmmm, maybe intervene acquisition won't match.. think about ti # todo.
    Think about the workflow:
    the user would choose a basic set of parameters based on convention or "feel".
    The parameter to be selected based on "feeling" would be laser power, exposure time per slice, scanning length sale
    (the travel distance of the stage in the LS3 scanning mode).

    Then there will be some parameters that would be selected based on hardware restrictions/constraints,
    such as: camera read out time (user can read about it too), stage retraction time, the limit of the SG range.

    Some parameters can either be selected by "feeling", or by strict on-the-fly calibration:
    travel length (should be decided based on the sample size). total number of time point.

    Usually it is the sampling frequency, pixel size(from calibration), exposure time per slice,
    read out time per image, and stage retraction time (from calibration).

    suggest a list with the following variations:
    magnification factor.
    number of color channels.
    number of views.

    And implement child modules based on the acquisition mode. (currently, there are 6 modes, see the device facilitator
     level readme.md for details.)

    in this base class, everything was calculated for 1 stack 1 view.
    This stack may contain multi color channel, intervene, mixed color, adapted color, etc.
    corresponding to mode 2, slice then color, or color slice, then color-slice together.


    Position list:
    Now think about position list. - all the datapoint should carry the actual time tags.
    need to think about the travel time from position to position.
    Perhaps no need to integrate it here because the position distances will be highly dynamic and we dont really know
    how much time it will take to move from position to position
    Just pass the parameters in.
    and use it to build the acquisition flow.
    maybe define a move speed to move from position to position at somepoint. leave a placeholder here.
    """

    def __init__(self,
                 dx=0.4,
                 length=1000,
                 t_exposure=90,
                 t_readout=10,
                 t_stage_retraction=23,
                 scanning_galvo_range_limit=0.8,
                 number_of_colors_per_slice=1,
                 colors=['488'],
                 number_of_scans_per_timepoint=1,
                 slice_color_list=None,
                 positions=None,
                 views=['1'],
                 positions_views_list=None,
                 ):
        """
        This tool is expected to make the process of selecting imaging parameters easy.
        first, the user will input a series of basic parameters, and the program will
        suggest a list of options of different combinations of the parameters, so the user can make decisions
        by looking at the specific specs of the suggested parameters, and choose one to be the final acquisition parameter

        some facilitator would then take the selected parameteres to generate all the configurations files for all the devies.
        which facilitator shoudl this be?
        thing about it...

        :param dx: pixel size in camera, unit=um
        :param length: scan range along the stage scanning axis
        :param t_exposure: camera exposure time unit = ms
        :param t_readout: camera waiting time, unit = ms
        :param t_stage_retraction: the amount of time the stage needs to move back to the initial position.
        :param number_of_colors_per_slice: number of colors per slice per view.
        :param view_number: total number of views, 1 or 2 for daxi.
        :param number_of_scans_per_timepoint: number of stacks per time point. this number chanes with the acquisiton mode.
        """
        self.dx = float(dx)
        self.length = float(length)
        self.colors = colors
        self.number_of_colors = len(colors)
        self.number_of_colors_per_slice = number_of_colors_per_slice
        self.views = views
        self.number_of_views = len(views)
        self.t_exposure = float(t_exposure)
        self.t_readout = float(t_readout)
        self.t_stage_retraction = float(t_stage_retraction)  # todo - make this a measured value as a calibration modules.
        self.ns = None
        self.ys_list = None
        self.vs_list = None
        self.n_slices_list = None
        self.stack_time_list = None
        self.length_updated_list = None
        self.selected_parameters = None
        self.scanning_galvo_range_per_slice_list = None  # there has to be a limit based on the FOV on top of O1.
        self.scanning_galvo_range_limit = scanning_galvo_range_limit  # set this as the limit (mm)
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        # (when there are multiple colors per slice in intervened mode, we keep scanning the SG to chase the stage,
        # and the laser is alternative per color to acquire multi-channels, and we keep the SG at constant speed even
        # during the read out time of the color channels except for the last color channel.).
        self.t_SG_retraction = self.t_readout  # SG retraction time, this should be during the read out time of the
        # last color channel.
        self.number_of_scans_per_time_point = int(number_of_scans_per_timepoint)
        self.slice_color_list = slice_color_list
        self.positions = positions
        self.positions_views_list = positions_views_list
        self.name = 'base class'
        self.type = 'base'
        self.looping_order = None

    def find_parameter_combinations(self):
        """
        constrains:
        1. =distance between different slices should be integer number of pixel size
            y = N*dx

        2. scanning range (at 45 angle) is associated with the stage speed and exposure times
        sqrt(2)*y = sqrt(2)*N*dx = (tE + tR) * Vs where, Vs is the scanning speed.

        so now calcualte the scannings peed, we have:
        Vs = sqrt(2)*N*dx/(tE + tR)

        3. calculate the total number of slices
        n_slices = floor(L/sqrt(2)*N*dx)

        4. update the true range
        Lupdated = n_slices * sqrt(2)*N*dx

        5. should measure the raster scan retraction time with the current range and speed setting.
        so perhaps arrange two triggers to measure that.
        tS - the amount of time for retraction.

        6. calculate the total amount of time per slice
        n_slices * (tE + tR) + tS, and display it as time resolution
        :return:
        """

        # prepare a list of magnification factor
        ns = np.arange(10)+1  # magnification factor (ratio between axial pixel size, and lateral pixel size)

        # based on the magnification factor, calculate the perpendicular distances between adjacent slices
        ys_list = ns * self.dx

        # based on the perpendicular distances between adjacent slices, calculate the stage travel distances
        # between adjacent slices
        ystage_list = np.sqrt(2) * ys_list

        # based on the stage travel distances and the time differences between adjacent slices, calculate the
        # desired stage scanning speed.
        vs_list = ystage_list / self.t_per_slice  # unit = um/ms

        # based on the input stage travel total distance (self.length) and the
        # stage travel distances between different slices, calculate the total number of slices.
        n_slices_list = np.ceil(self.length / ystage_list)

        # based on the number of slices, update the actual travel length of the scanning stage.
        length_updated_list = n_slices_list * ystage_list

        # based on the number of slices and time spent for each slice, calculate the total amount of time for
        # acquisition per stack per view.
        stack_time_list = n_slices_list * self.t_per_slice + self.t_stage_retraction

        # calculate the SG scanning range per slice for all colors based on the scanning speed and the exposure time.
        scanning_galvo_scan_range_per_slice_list = vs_list*self.t_SG_scan  # unit = um #
        # todo should translate this into voltages.

        # calculate the scanning duration per raster scan
        scan_durations_list = n_slices_list * self.t_per_slice + self.t_stage_retraction
        time_per_datapoint_list = scan_durations_list * self.number_of_scans_per_time_point

        # copy over the parameters to the object:
        self.ns = ns  # list of multiplication factors of slice distances as compared to the xy pixel size
        self.ys_list = ys_list  # (um) list of slice distances
        self.vs_list = vs_list  # (um/ms) list of stage scanning speed.
        self.n_slices_list = n_slices_list  # list of total number of slices
        self.stack_time_list = stack_time_list  # (ms) list of time per stack.
        self.length_updated_list = length_updated_list
        self.scanning_galvo_range_per_slice_list = scanning_galvo_scan_range_per_slice_list
        self.scan_durations_list = scan_durations_list
        self.time_per_datapoint_list = time_per_datapoint_list

    def display_parameter_options(self):
        print("suggested parameter options are shown below, based on different magnification factors:")
        for n, y, n_slices, stack_time, length, vs, sgr, tpd, sd in zip(self.ns,
                                                               self.ys_list,
                                                               self.n_slices_list,
                                                               self.stack_time_list,
                                                               self.length_updated_list,
                                                               self.vs_list,
                                                               self.scanning_galvo_range_per_slice_list,
                                                               self.time_per_datapoint_list,
                                                               self.scan_durations_list):
            print('mag-factor: ' + str(n) +
                  ', slice distance (um): ' + str(np.floor(y*10)/10) + ' um' +
                  ', n slices: ' + str(n_slices) +
                  ', time per stack per view (s): ' + str(np.floor(stack_time/100)/10) + ' s' +
                  ', scanning range(mm): '+str(np.floor(length/10)/100) +
                  ', scanning speed: '+str(np.floor(vs*100000)/100) + 'nm/ms' +
                  # todo should implement based on the constraints of the scanning stage.
                  ', SG range per slice (um): ' + str(sgr) +
                  ', time per datapoint (s): ' + str(tpd/1000) +
                  ', scan duration (s): ' + str(sd/1000)
                  )

    def get_parameter_combination(self, magnification_factor=5):
        n = magnification_factor
        y = n * self.dx
        v = np.sqrt(2) * y / (self.t_exposure + self.t_readout) / self.number_of_colors_per_slice  # unit = um/ms
        n_slices = int(np.ceil(self.length / np.sqrt(2) / n / self.dx))
        length_updated = n_slices * np.sqrt(2) * n * self.dx
        scan_duration = n_slices * self.t_per_slice + self.t_stage_retraction
        time_per_datapoint = scan_duration*self.number_of_scans_per_time_point
        self.stage_travel_distance = float(length_updated)
        self.scanning_galvo_range_per_slice = float(v * self.t_SG_scan)
        self.selected_parameters = \
            {
                'name': self.name,
                'type': self.type,
                'looping order': self.looping_order,
                "pixel size in xy (um)": self.dx,
                "mag-factor": n,
                "slice distance (um)": float(y),
                "n slices": n_slices,
                "time per stack per view (s)": float(scan_duration/1000),
                "time per time point (s)": float(time_per_datapoint/1000),
                "scanning range (um)": float(length_updated),
                "scanning speed (nm/ms)": float(v*1000),
                "exposure time (ms)": self.t_exposure,
                "camera read out time (ms)": self.t_readout,
                "stage retraction time (ms)": self.t_stage_retraction,
                "scanning galvo scan range per slice (um)": self.scanning_galvo_range_per_slice,
                "scanning galvo scan range limit (um)": self.scanning_galvo_range_limit,
                "metronome frequency": int(10000),
                "views": self.views,
                "colors": self.colors,
            }


class AcqParamMode1(AcqParamBase):
    """
    loop layers:
    [mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]
    this acquisition mode maximize the time resolution within a color chanel, but with increased offsets between
    different color channels.
    When would this be useful? This mode could be use when measuring the interaction of 2 objects each labeled with
    one color, one moves fast and we have to image with the fasted time resolution possible for this channel
    to avoid motion blur within the single color channel, the other one moves slow so the offset between time
    doesn't matter. Some fast dynamics of object 1 and study it's interaction with a super-static structure.

    example 1:
    How immune cells migrate away from blood vessels. immune cells need high time resolution, blood vessels is static.
    """

    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = 1
        self.number_of_scans_per_time_point = self.number_of_views * self.number_of_colors
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode1'
        self.type = 'mode1'
        self.looping_order = '[mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]'


class AcqParamMode2(AcqParamBase):
    """
    [mode 2] - [layer 1: position] - [layer 2: view] - [layer 3: slice] - [layer 4: color]
    This mode corresponds to the intervened acquisiton mode. for each slice, it takes the list of all colors acquisition
    first, then move on to the next slice.
    """

    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = len(self.colors)
        self.number_of_scans_per_time_point = self.number_of_views
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode2'
        self.type = 'mode2'
        self.looping_order = '[mode 2] - [layer 1: position] - [layer 2: view] - [layer 3: slice] - [layer 4: color]'


class AcqParamMode3(AcqParamBase):
    """
    [mode 3] - [layer 1: position] - [layer 2: view] - [layer 3: slice, color]
    this acquisition mode uses a pre-defined list of slice/color. user can choose which slice to use which color
    during the acquisition
    """
    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = 1
        self.number_of_scans_per_time_point = self.number_of_views
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode3'
        self.type = 'mode3'
        self.looping_order = '[mode 3] - [layer 1: position] - [layer 2: view] - [layer 3: slice, color]'


class AcqParamMode4(AcqParamBase):
    """
    [mode 4] - [layer 1: position, view] - [layer 2: color] - [layer 3: slice]
    this acquisition mode uses a pre-defined list of slice/color. user can choose which slice to use which color
    during the acquisition
    """
    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = 1
        self.number_of_scans_per_time_point = self.number_of_views * self.number_of_colors
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode4'
        self.type = 'mode4'
        self.looping_order = '[mode 4] - [layer 1: position, view] - [layer 2: color] - [layer 3: slice]'


class AcqParamMode5(AcqParamBase):
    """
    [mode 5] - [layer 1: position, view] - [layer 2: slice] - [layer 3: color]
    this acquisition mode uses a pre-defined list of slice/color. user can choose which slice to use which color
    during the acquisition
    """
    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = len(self.colors)
        self.number_of_scans_per_time_point = self.number_of_views
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode5'
        self.type = 'mode5'
        self.looping_order = '[mode 5] - [layer 1: position, view] - [layer 2: slice] - [layer 3: color]'


class AcqParamMode6(AcqParamBase):
    """
    [mode 6] - [layer 1: position, view] - [layer 2: slice, color]
    this acquisition mode uses a pre-defined list of slice/color. user can choose which slice to use which color
    during the acquisition
    """
    def adapt(self):
        # change the initialization parameters to adapt to this specific acquisition mode.
        self.number_of_colors_per_slice = 1
        self.number_of_scans_per_time_point = self.number_of_views
        self.t_per_slice = (self.t_exposure + self.t_readout)*self.number_of_colors_per_slice  # time per slice (ms)
        self.t_SG_scan = self.t_per_slice - self.t_readout  # SG scanning time (more below)
        self.name = 'mode6'
        self.type = 'mode6'
        self.looping_order = '[mode 6] - [layer 1: position, view] - [layer 2: slice, color]'

