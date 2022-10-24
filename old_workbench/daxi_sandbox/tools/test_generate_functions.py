from generate_functions import *

def test_getfcn_linear_ramp():
    """
    test function for getfcn_linear_ramp
    """
    data=getfcn_linear_ramp(starting_voltage=0, ending_voltage=0.4, sample_number=500)
    assert isinstance(data, np.ndarray)
    assert len(data) == 500
    assert data[0] == 0
    assert data[-1] == 0.4


def test_getfcn_linear_ramp_soft_retraction():
    pass
