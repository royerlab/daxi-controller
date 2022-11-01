from daxi.ctr_devicesfacilitator.demos.demo_devicesfcltr_checkout_configs_from_all_cycles_by_key import \
    demo_devicefcltr_checkout_configs_from_all_cycles_by_key


def test_devicefcltr_checkout_configs_from_all_cycles_by_key():
    msg = demo_devicefcltr_checkout_configs_from_all_cycles_by_key(verbose=False)
    assert msg is 'success'

