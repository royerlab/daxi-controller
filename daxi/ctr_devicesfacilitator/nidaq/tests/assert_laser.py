from daxi.development_tools.general_test_utils import sys_msg


def assert_laser(verbose=True, laser=None):
    """
    This function asserts the basic requirements of a laser object

    Parameters
    ----------
    verbose: option for output messages.
    laser: input laser object (base class: LaserBase)

    Returns
    -------
    None.

    """
    # manager
    sys_msg(msg="echo asserting a laser ...", verbose=verbose)

    # laser_line_names
    sys_msg(msg="laser should have a list of laser lines, each specified by a name (str)", verbose=verbose)
    assert hasattr(laser, 'laser_line_names')
    assert isinstance(laser.laser_line_names, list)
    if len(laser.laser_line_names) > 0:
        for x in laser.laser_line_names:
            assert isinstance(x, str)

    # daq_terminal_names
    sys_msg(msg="each laser line should be connected to a terminal on the daq card\
                , and the laser should have an attribute of \'daq_terminal_names\' \
                to store the list of terminal names", verbose=verbose)
    assert hasattr(laser, 'daq_terminal_names')
    sys_msg(msg="terminal number should be the same with the total number of laser lines ...")
    assert len(laser.daq_terminal_names) == len(laser.laser_line_names)
    if len(laser.daq_terminal_names) > 0:
        for x in laser.daq_terminal_names:
            assert isinstance(x, str)
            # todo - add something to check that the laser is properly connected to the daq card.

    # on_voltage and off_voltage
    sys_msg(msg="check attributes of on_voltage and off_voltage", verbose=verbose)
    assert hasattr(laser, 'on_voltage')
    assert isinstance(laser.on_voltage, float)
    assert hasattr(laser, 'off_voltage')
    assert isinstance(laser.off_voltage, float)

    sys_msg(msg="check switch on and switch_off methods", verbose=verbose)
    assert hasattr(laser, 'switch_on')
    assert hasattr(laser, 'switch_off')

    sys_msg(msg="echo done asserting the lase.", verbose=verbose)
