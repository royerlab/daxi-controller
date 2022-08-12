# daxi_ms2k.py
# this file is disseminate from the example scripts of the official ASI-stage API
# it inherits the serialport.py class used in the example script.
# official API site:
# http://asiimaging.com/docs/python


# Note - I'm trying tp keep it consistent with the offical API example codes. - Xiyu Yi, 2022-08-10

from asistage.serialport import SerialPort
from time import sleep
import copy

class DaxiMs2kStageData:
    """define a data container for configurations and records here. organize in the very end."""
    pass


class DaxiMs2kStage(SerialPort):
    """
    This contains the tools for operating MS2000 for controlling a DaXi microscope.

    Note:
    Move commands use ASI units: 1 unit = 1/10 of a micron.
    Example: to move a stage 1 mm on the x axis, use self.moverel(10000)

    relevant publications:

    """

    # all valid baud rates for the MS2000
    # these rates are controlled by dip switches

    def __init__(self, com_port: str, baud_rate: int = 115200, report: str = True):
        super().__init__(com_port, baud_rate, report)
        # validate baud_rate input
        self.BAUD_RATES = [9600, 19200, 28800, 115200]

        if baud_rate in self.BAUD_RATES:
            self.baud_rate = baud_rate
            print('The selected baud rate is ' + str(baud_rate))
        else:
            raise ValueError("The baud rate is not valid. Valid rates: 9600, 19200, 28800, or 115200.")

        # define some container attribute
        self.stored_positions = {'current position': {'unit': 'mm', 'X': 0.0,
                                                      'Y': 0.0}}  # may want some structure to these positions.
        # in the stored positions, store X, Y, unit, and scanning configurations.
        self.connect_to_serial()
        if not self.is_open():
            print("daxims2k is not open.")

        self.default_raster_scan_configs = {'scan speed': 0.0528,
                                            'scan range': 10.0,
                                            'start position': None,
                                            'end position': None,
                                            'encoder divide': 24,
                                            }

    # ---------------------------------------------------------------------------- #
    #     MS2000 Serial Commands to be used when controlling a DaXi microscope     #
    # ---------------------------------------------------------------------------- #

    def is_device_busy(self) -> bool:
        """Returns True if any axis is busy."""
        self.send_command("/")
        return "B" in self.read_response()

    def wait_for_device(self, report: bool = False) -> None:
        """Waits for the all motors to stop moving."""
        if not report:
            print("Waiting for device...")
        temp = self.report
        self.report = report
        busy = True
        while busy:
            busy = self.is_device_busy()
        self.report = temp

    def config_speed(self, scan_configs=None, speed: float = 0.528):
        """

        Parameters
        ----------
        scan_configs: dict, dictionary of scanning configurations.
        speed: float, unit: um/ms (equivalent to mm/s)

        Returns
        -------

        """
        if scan_configs is None:
            msg_speed = f"SPEED X={speed}\r"
        else:
            msg_speed = f"SPEED X={scan_configs['scan speed']}\r"
        self.send_command(msg_speed)
        self.read_response()
        self.wait_for_device()

    def config_raster_scan(self, scan_configs: dict, start: float = None, end: float = None, encoder_divide: int = None):
        """

        Parameters
        ----------
        start: float, unit of mm
            starting position along the scanning axis.
        end: float, unit of mm
            ending position along the scanning axis
        encoder_divide: int
            to better understand the encode_divide, refer to the following website:
            Specifically, the following paragraphS:
            "Let’s go through an example where we wish to scan a 1 mm × 1 mm region at a resolution of about 0.5 μm on
            an XY stage. We will consider the X axis to be the ‘horizontal’ direction, and Y to be the ‘vertical’
            direction. (Although any axis is eligible to be ‘horizontal’, only one will have been wired at the factory
            for encoder output signals – see the SCAN command’s parameters for alternative configurations.) For a
            standard 6.35 mm pitch lead-screw stage, the (rotary) encoder resolution is 45396 counts/mm or 0.022
            μm/count. However, this includes all of the quadrature edges of the two encoder channels and the counting
            circuit is only looking at the positive edges of one encoder signal, so the input clock pulse to the
            controller would be at 0.0881 μm intervals. Hence the output clock pulse can only be set to be an integer
            multiple of 0.0881 μm which is 4 encoder counts (for 4 TPI leadscrew with rotary encoders; if you are not
            sure of the encoder resolution of the scanned axis, issue the command INFO X, where X is the axis in
            question, to query the controller about the parameters that are used.). This 0.0881 μm distance (or
            equivalent [4000/C]) is multiplied by the SCANR Z setting to get the distance between output clock pulses.
            The maximum output clock would is with SCANR Z set to 8, or just over 176 nm.

            If we generate a clock pulse every 24 encoder counts (6 full periods of a single encoder signal), then our
            pixel clock resolution will be 0.022 × 24 = 0.528 μm. To set up the ‘horizontal’ raster, we issue the
            command:

            SCANR X=0.0 Y=1.0 Z=24 (X= start, Y= stop, Z=encoder_divide)"


        Returns
        -------

        """
        if scan_configs is None:
            msg_raster_scan = f"SCANR X={start} Y={end} Z={encoder_divide}\r"
        else:
            start = scan_configs['start position']
            end = scan_configs['end position']
            encoder_divide = scan_configs['encoder divide']
            msg_raster_scan = f"SCANR X={start} Y={end} Z={encoder_divide}\r"

        self.send_command(msg_raster_scan)
        self.read_response()
        self.wait_for_device()

    def get_current_position(self, unit: str = 'mm'):
        """
        read the current position of the stage, return a dictionary in units of mm.
        unit, str, options: "asi", "mm"
        """

        pos = {'unit': unit}  # store the axis positions
        for axis_tag in ['X', 'Y']:
            self.send_command(f"WHERE " + axis_tag + "\r")  # send a serial command to get the X axis position
            resp = self.read_response()  # receive the responses with position information expressed in a string
            print('now print resp')
            print(resp)
            pos_str = resp.split(" ")[1]  # parse the string to obtain the position substring in ASI unit (10 um).
            # convert position string to number, with given unit.
            pos[axis_tag] = pos_str2num(pos_str, unit)
            # wait for the device
            # self.wait_for_device() # this doesn't work. hold.
            sleep(0.1)  # todo - should replace this into some proper waiting time. leave it for now.

        pos['scan configurations'] = copy.deepcopy(self.default_raster_scan_configs)
        pos['scan configurations']['start position'] = pos['X']
        pos['scan configurations']['end position'] = self.default_raster_scan_configs['scan range']+pos['X']

        print('current position:')
        print(pos)
        return pos

    def append_current_position(self, name: str, unit: str = 'mm'):
        """
        store the current position to the stored positions
        store om unit of mm. -- need to somehow standardize the format of this position attribute.
        """
        pos = self.get_current_position(unit)
        self.stored_positions[name] = pos

    def define_explicit_position(self, name:str, unit:str = 'mm', x:float = 1.0, y:float = 1.0):
        pos= {'unit': unit,
              'X': x,
              'Y': y,
              'scan configurations': copy.deepcopy(self.default_raster_scan_configs)}
        pos['scan configurations']['start position'] = pos['X']
        pos['scan configurations']['end position'] = self.default_raster_scan_configs['scan range']+pos['X']

        return pos

    def move_to(self, destination_name: str):
        """

        Parameters
        ----------
        destination_name: str
            name of the stored destination position.

        Returns
        -------

        """

        # retrieve the position under the destination_name
        pos = self.stored_positions[destination_name]
        # convert the position to asi unit
        pos_asi = pos_2asi(pos)
        # move to the position
        self.send_command(f"MOVE X={pos_asi['X']} Y={pos_asi['Y']}\r")
        self.read_response()

    def store_current_position(self):
        self.append_current_position(name='current position')

    def raster_scan_get_configs(self, position_name: str = 'current position', scan_range: float = 10,
                                encoder_divide: int = 24, scan_speed: float = 0.528):
        """
        this method prepares the configuration for a scanning.
        It will drive the stageto a position of choice, configure the raster scanning range, resolution (encode divider)
        and speed.

        Parameters
        ----------
        position_name: str  # todo standardize the position data format.
        scan_range: float, unit = mm
        encoder_divide: int, number of cycles for each encoder period (determins the step size)
        scan_speed: float,  unit = mm/s or um/ms

        Returns
        -------

        """

        # note that in SCANR, the start and end position uses unit of mm.
        # get position in mm unit:
        pos_mm = pos_2mm(self.stored_positions[position_name])

        # - - start/stop position - define the scan region
        pos_start = pos_mm['X']
        pos_end = pos_mm[
                      'X'] + scan_range  # todo, there might be numerical errors where the rounded scan range do not
        # todo, --- match with the number of frames exactly.

        # configure scanning parameters - store info to the list
        scan_configs = {'scan speed': scan_speed,
                        'scan range': scan_range,
                        'start position': pos_start,
                        'end position': pos_end,
                        'encoder divide': encoder_divide,
                        }
        self.stored_positions[position_name]['scan configurations'] = scan_configs

    def raster_scan_ready(self, position_name: str = 'current position'):

        # retrieve the configuration parameters for this position.
        configs = self.stored_positions[position_name]['scan configurations']

        # move to the position
        self.move_to(position_name)

        # configure scanning parameters - scanning speed
        self.config_speed(scan_configs=configs)

        # configure scanning parameters - scan range and resolution
        self.config_raster_scan(scan_configs=configs)
        #  todo - keep some configuration parameter (when updated values are necessary)

    def raster_scan_go(self):
        """
        start the raster scan.

        Returns
        -------

        """
        self.send_command("SCAN\r")
        self.read_response()


def pos_str2num(pos_str: str, unit: str = 'mm'):
    """
    convert the position string (returned from the serial port) to a number with the specified unit.
    """
    if unit not in ['asi', 'mm']:
        print('unit is not supported, choose between asi and mm')  # need to standardize this part.
        return

    if unit == 'asi':
        # convert the position (as a string) to float number, in unit of mm.
        val = float(pos_str)

    if unit == 'mm':
        val = float(pos_str) / 10000.0  # convert the position (as a string) to float number, in unit of mm.if

    return val


def check_unit(unit):
    if unit not in ['asi', 'mm']:
        raise ValueError('the unit should be either \"asi\" or \"mm\"')


def pos_2asi(pos):
    check_unit(pos['unit'])
    if pos['unit'] == 'asi':
        val = pos

    if pos['unit'] == 'mm':
        val = {'unit': 'asi', 'X': pos['X'] * 10000.0, 'Y': pos['Y'] * 10000.0}

    return val


def pos_2mm(pos):
    check_unit(pos['unit'])
    if pos['unit'] == 'mm':
        val = pos

    if pos['unit'] == 'asi':
        val['unit'] = 'mm'
        val['X'] = pos['X'] / 10000.0
        val['Y'] = pos['Y'] / 10000.0

    return val
