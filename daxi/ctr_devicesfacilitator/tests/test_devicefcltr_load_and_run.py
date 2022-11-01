from daxi.ctr_devicesfacilitator.demos.demo_devicesfcltr_load_and_run import demo_devicefcltr_load_and_run
from daxi.ctr_devicesfacilitator.demos.demo_devicesfcltr_receive_map_checkout_and_run import \
    demo_devicefcltr_receive_map_checkout_and_run


def test_devicefcltr_load_and_run():
    msg = demo_devicefcltr_load_and_run(verbose=False, interactive=False)
    assert msg is 'success'


def test_devicefcltr_load_and_run():
    msg = demo_devicefcltr_receive_map_checkout_and_run(verbose=False, interactive=False)
    assert msg is 'success'
