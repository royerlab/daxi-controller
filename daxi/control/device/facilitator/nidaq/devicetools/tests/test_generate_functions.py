from daxi.control.device.facilitator.nidaq.devicetools.generate_functions import DAQDataGenerator
from daxi.control.device.facilitator.nidaq.devicetools.generate_functions import get_soft_retraction


def test_getfcn_sinusoidal(amplitude=1,
                           center_voltage=0,
                           sample_number=1000):
    dg = DAQDataGenerator()
    data = dg.getfcn_sinusoidal(amplitude=1,
                                center_voltage=0,
                                sample_number=1000,
                                initial_phase=0
                                )
    assert len(data) == sample_number
    assert isinstance(data, list)
    assert max(data) == center_voltage + amplitude
    assert min(data) == center_voltage - amplitude


def test_get_soft_retraction():
    data = get_soft_retraction(v_start=10, v_end=100, n_total=100)
    assert len(data) == 100
    assert isinstance(data, list)
    assert data[0] == 10
    assert data[-1] == 100

    data = get_soft_retraction(v_start=100, v_end=10, n_total=1000)
    assert len(data) == 1000
    assert isinstance(data, list)
    assert data[0] == 100
    assert data[-1] == 10


def test_getfcn_linear_ramp_soft_retraction():
    dg = DAQDataGenerator()
    data = dg.getfcn_linear_ramp_soft_retraction(v0=10,
                                                 v1=100,
                                                 n_sample_ramp=1000,
                                                 n_sample_retraction=100)

    assert len(data) == 1100
    assert isinstance(data, list)
    assert data[0] == 10
    assert data[-1] == 10
    assert data[999] == 100

    data = dg.getfcn_linear_ramp_soft_retraction(v0=200,
                                                 v1=40,
                                                 n_sample_ramp=500,
                                                 n_sample_retraction=100)

    assert len(data) == 600
    assert isinstance(data, list)
    assert data[0] == 200
    assert data[-1] == 200
    assert data[499] == 40