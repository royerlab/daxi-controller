# ms2k.py
# this file is copied over from the example scripts of the official ASI-stage API
# offical API site:
# http://asiimaging.com/docs/python

# Note - I'm keeping it consistent with the offical API example codes. - Xiyu Yi, 2022-08-05
#

from asistage.serialport import SerialPort


class MS2000(SerialPort):
    """
    A utility class for operating the MS2000 from Applied Scientific Instrumentation.

    Move commands use ASI units: 1 unit = 1/10 of a micron.
    Example: to move a stage 1 mm on the x axis, use self.moverel(10000)

    Manual:
        http://asiimaging.com/docs/products/ms2000

    """

    # all valid baud rates for the MS2000
    # these rates are controlled by dip switches
    BAUD_RATES = [9600, 19200, 28800, 115200]

    def __init__(self, com_port: str, baud_rate: int = 115200, report: str = True):
        super().__init__(com_port, baud_rate, report)
        # validate baud_rate input
        if baud_rate in self.BAUD_RATES:
            self.baud_rate = baud_rate
            print('The selected baud rate is' + str(baud_rate))
        else:
            raise ValueError("The baud rate is not valid. Valid rates: 9600, 19200, 28800, or 115200.")

    # ------------------------------ #
    #     MS2000 Serial Commands     #
    # ------------------------------ #

    def moverel(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        """Move the stage with a relative move."""
        self.send_command(f"MOVREL X={x} Y={y} Z={z}\r")
        self.read_response()

    def moverel_axis(self, axis: str, distance: int) -> None:
        """Move the stage with a relative move."""
        self.send_command(f"MOVREL {axis}={distance}\r")
        self.read_response()

    def move(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        """Move the stage with an absolute move."""
        self.send_command(f"MOVE X={x} Y={y} Z={z}\r")
        self.read_response()

    def scan(self, x: int = 1000, y: int = 1000):
        """ try scan """
        message = f"SCAN x={x} y={y}\r"
        self.send_command(message)
        print(self.read_response())

    def move_axis(self, axis: str, distance: int) -> None:
        """Move the stage with an absolute move."""
        self.send_command(f"MOVE {axis}={distance}\r")
        self.read_response()

    def set_max_speed(self, axis: str, speed: int) -> None:
        """Set the speed on a specific axis. Speed is in mm/s."""
        self.send_command(f"SPEED {axis}={speed}\r")
        self.read_response()

    def get_position(self, axis: str) -> int:
        """Return the position of the stage in ASI units (tenths of microns)."""
        self.send_command(f"WHERE {axis}\r")
        response = self.read_response()
        return int(response.split(" ")[1])

    def get_position_um(self, axis: str) -> float:
        """Return the position of the stage in microns."""
        self.send_command(f"WHERE {axis}\r")
        response = self.read_response()
        x=response.split(" ")[1]
        print('x is ')
        print(x)
        return float(x) / 10.0

    # ------------------------------ #
    #    MS2000 Utility Functions    #
    # ------------------------------ #

    def is_axis_busy(self, axis: str) -> bool:
        """Returns True if the axis is busy."""
        self.send_command(f"RS {axis}?\r")
        return "B" in self.read_response()

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
