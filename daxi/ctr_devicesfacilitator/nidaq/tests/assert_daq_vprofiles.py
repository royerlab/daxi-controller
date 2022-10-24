from daxi.development_tools.general_test_utils import sys_msg
from daxi.ctr_devicesfacilitator.nidaq.tool_daqprofile import DaqVoltageProfileBase, DaqAOProfile, DaqDOProfile


def assert_daq_vprofile_baseclass(verbose=True, profile_obj=None):
    assert isinstance(profile_obj, DaqVoltageProfileBase)
    assert hasattr(profile_obj, 'name')
    assert hasattr(profile_obj, 'sample_number')
    assert hasattr(profile_obj, 'data')
    assert hasattr(profile_obj, 'resting_voltage')


def assert_daq_aoprofile(verbose=True, aoprofile=None):
    assert isinstance(aoprofile, DaqAOProfile)
    assert hasattr(aoprofile, 'analog_output_terminal')
    assert_daq_vprofile_baseclass(verbose=verbose, profile_obj=aoprofile)


def assert_daq_doprofile(verbose=True, doprofile=None):
    assert isinstance(doprofile, DaqDOProfile)
    assert hasattr(doprofile, 'digital_output_terminal')
    assert_daq_vprofile_baseclass(verbose=verbose, profile_obj=doprofile)

