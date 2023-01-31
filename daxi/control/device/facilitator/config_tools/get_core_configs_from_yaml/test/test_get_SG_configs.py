from daxi.control.device.facilitator.config_tools.get_core_configs_from_yaml.demo.demo_get_SG import demo_get_sg_configs


def test_sg_configs():
    msg = demo_get_sg_configs()
    assert msg == 'success'
