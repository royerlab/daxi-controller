import numpy as np
from daxi.control.data.facilitator.processing.process_stacks import get_3d_mips
from matplotlib import pyplot as plt

from daxi.control.device.facilitator.direct.orca_flash4_simulated import simulate_a_random_object_3d_stack


def demo_calcualted_3d_mips(istest=True):
    stack = simulate_a_random_object_3d_stack(x=150, y=200, z=50)
    mip0, mip1, mip2, stitched_mips = get_3d_mips(stack=stack)
    if istest is False:
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 2, 1)
        plt.imshow(stitched_mips)
        plt.subplot(2, 2, 2)
        plt.imshow(mip0)
        plt.subplot(2, 2, 3)
        plt.imshow(mip1)
        plt.subplot(2, 2, 4)
        plt.imshow(mip2)
        plt.show()
    return 'success'


if __name__ == '__main__':
    demo_calcualted_3d_mips(istest=False)
