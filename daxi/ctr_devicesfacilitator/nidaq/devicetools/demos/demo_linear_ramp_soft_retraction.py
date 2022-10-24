from matplotlib import pyplot as plt
from daxi.ctr_devicesfacilitator.nidaq.devicetools.generate_functions import DAQDataGenerator

dg = DAQDataGenerator()
data = dg.getfcn_linear_ramp_soft_retraction(v0=200,
                                             v1=200,
                                             n_sample_ramp=500,
                                             n_sample_retraction=100)

plt.plot(data)
plt.show()