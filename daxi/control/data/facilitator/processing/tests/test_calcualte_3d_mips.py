from daxi.control.data.facilitator.processing.demos.demo_calcualte_3d_mips import demo_calcualted_3d_mips


def test_calculate_3d_mips():
    msg = demo_calcualted_3d_mips(istest=True)
    assert msg == 'success'