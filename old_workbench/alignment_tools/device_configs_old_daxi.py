# define configurations for the devices
# may need to replace this to port information from a GUI. ToDo - Xiyu, 2022-09-07


# Define parameters
# in this cell we don't store the final voltages.
SG_view1={} # scanning galvo
SG_view1['instrument name'] = "old DaXi"
SG_view1['channel I/O type'] = "AO"   #
SG_view1['channel_string'] = "cDAQ1AO/ao0"  # name of the DAQ channel that will be used to control the device
SG_view1['controlled device name'] = "scanning galvo"  # name of the deviced to be controlled.
SG_view1['description'] = "at C-BFP, to scan the position of the light sheet."  # purpose of this device.
SG_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
SG_view1['home offset voltage'] = 1.57  # this is an offset voltage to set on top of the home voltage value.
SG_view1['home offset option'] = True  # the offset will be applied when this option is True.
SG_view1['verbose'] = False  # when True, status messages will be printed.

# in this cell we don't store the final voltages.
SG_view2={} # scanning galvo
SG_view2['instrument name'] = "old DaXi"
SG_view2['channel I/O type'] = "AO"   #
SG_view2['channel_string'] = "cDAQ1AO/ao0"  # name of the DAQ channel that will be used to control the device
SG_view2['controlled device name'] = "scanning galvo"  # name of the deviced to be controlled.
SG_view2['description'] = "at C-BFP, to scan the position of the light sheet."  # purpose of this device.
SG_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
SG_view2['home offset voltage'] = 1.57  # this is an offset voltage to set on top of the home voltage value.
SG_view2['home offset option'] = True  # the offset will be applied when this option is True.
SG_view2['verbose'] = False  # when True, status messages will be printed.

# O1
O1_view1={} # scanning galvo
O1_view1['instrument name'] = "old DaXi"
O1_view1['channel I/O type'] = "AO"  #
O1_view1['channel_string'] = "cDAQ1AO2/ao1"  # name of the DAQ channel that will be used to control the device
O1_view1['controlled device name'] = "o1"  # name of the deviced to be controlled.
O1_view1['description'] = "set O1 offset."  # purpose of this device.
O1_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
O1_view1['home offset voltage'] = 0  # this is an offset voltage to set on top of the home voltage value.
O1_view1['home offset option'] = True  # the offset will be applied when this option is True.
O1_view1['verbose'] = False  # when True, status messages will be printed.

# O1
O1_view2={} # scanning galvo
O1_view2['instrument name'] = "old DaXi"
O1_view2['channel I/O type'] = "AO"  #
O1_view2['channel_string'] = "cDAQ1AO2/ao1"  # name of the DAQ channel that will be used to control the device
O1_view2['controlled device name'] = "o1"  # name of the deviced to be controlled.
O1_view2['description'] = "set O1 offset."  # purpose of this device.
O1_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
O1_view2['home offset voltage'] = 0  # this is an offset voltage to set on top of the home voltage value.
O1_view2['home offset option'] = True  # the offset will be applied when this option is True.
O1_view2['verbose'] = False  # when True, status messages will be printed.

# define parameters
gamma_G_view1={} # gamma galvo
gamma_G_view1['instrument name'] = "old DaXi"
gamma_G_view1['channel I/O type'] = "AO"  #
gamma_G_view1['channel_string'] = "cDAQ1AO/ao3"  # name of the DAQ channel that will be used to control the device
gamma_G_view1['controlled device name'] = "gamma galvo"  # name of the deviced to be controlled.
gamma_G_view1['description'] = " at C-FP, introduce in-plane tilts in the light sheet, used for strip reduction"  # purpose of this device.
gamma_G_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
gamma_G_view1['home offset voltage'] = 0.18  # this is an offset voltage to set on top of the home voltage value.
gamma_G_view1['home offset option'] = True  # the offset will be applied when this option is True.
gamma_G_view1['verbose'] = False  # when True, status messages will be printed.

# define parameters
gamma_G_view2={} # gamma galvo
gamma_G_view2['instrument name'] = "old DaXi"
gamma_G_view2['channel I/O type'] = "AO"  #
gamma_G_view2['channel_string'] = "cDAQ1AO/ao3"  # name of the DAQ channel that will be used to control the device
gamma_G_view2['controlled device name'] = "gamma galvo"  # name of the deviced to be controlled.
gamma_G_view2['description'] = " at C-FP, introduce in-plane tilts in the light sheet, used for strip reduction"  # purpose of this device.
gamma_G_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
gamma_G_view2['home offset voltage'] = 0.18  # this is an offset voltage to set on top of the home voltage value.
gamma_G_view2['home offset option'] = True  # the offset will be applied when this option is True.
gamma_G_view2['verbose'] = False  # when True, status messages will be printed.

# define parameters
beta_G_view1={} # beta galvo
beta_G_view1['instrument name'] = "old DaXi"
beta_G_view1['channel I/O type'] = "AO"
beta_G_view1['channel_string'] = "cDAQ1AO2/ao0"  # name of the DAQ channel that will be used to control the device
beta_G_view1['controlled device name'] = "beta galvo"  # name of the deviced to be controlled.
beta_G_view1['description'] = "at C-FP, introduce out-of-plane tilt in the"  \
                        + "light sheet, used for changing pitch angle"  # purpose of this device.
beta_G_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
beta_G_view1['home offset voltage'] = 0.4  # this is an offset voltage to set on top of the home voltage value.
beta_G_view1['home offset option'] = True  # the offset will be applied when this option is True.
beta_G_view1['verbose'] = False  # when True, status messages will be printed.

# define parameters
beta_G_view2={} # beta galvo
beta_G_view2['instrument name'] = "old DaXi"
beta_G_view2['channel I/O type'] = "AO"
beta_G_view2['channel_string'] = "cDAQ1AO2/ao0"  # name of the DAQ channel that will be used to control the device
beta_G_view2['controlled device name'] = "beta galvo"  # name of the deviced to be controlled.
beta_G_view2['description'] = "at C-FP, introduce out-of-plane tilt in the"  \
                        + "light sheet, used for changing pitch angle"  # purpose of this device.
beta_G_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
beta_G_view2['home offset voltage'] = 0.4  # this is an offset voltage to set on top of the home voltage value.
beta_G_view2['home offset option'] = True  # the offset will be applied when this option is True.
beta_G_view2['verbose'] = False  # when True, status messages will be printed.

# define parameters
VSG1_view1 = {}  # view switching galvo 1 for view 1 (1 mirror view)
VSG1_view1['instrument name'] = "Dold aXi"
VSG1_view1['channel I/O type'] = "AO"  #
VSG1_view1['channel_string'] = "cDAQ1AO/ao1"  # name of the DAQ channel that will be used to control the device
VSG1_view1['controlled device name'] = "view switching galvo 1 (closer to O1)"  # name of the deviced to be controlled.
VSG1_view1['description'] = "not in C planes, used for switching the view."  # purpose of this device.
VSG1_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
VSG1_view1['home offset voltage'] = -4.28  # this is an offset voltage to set on top of the home voltage value.
VSG1_view1['home offset option'] = True  # the offset will be applied when this option is True.
VSG1_view1['verbose'] = False  # when True, status messages will be printed.

# define parameters
VSG2_view1 = {}  # view switching galvo 2 for view 1 (1 mirror view)
VSG2_view1['instrument name'] = "old DaXi"
VSG2_view1['channel I/O type'] = "AO"  #
VSG2_view1['channel_string'] = "cDAQ1AO/ao2"  # name of the DAQ channel that will be used to control the device
VSG2_view1['controlled device name'] = "view switching galvo 2 (closer to O2)"  # name of the deviced to be controlled.
VSG2_view1['description'] = "not in C planes, used for switching the view."  # purpose of this device.
VSG2_view1['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
VSG2_view1['home offset voltage'] = 4.65  # this is an offset voltage to set on top of the home voltage value.
VSG2_view1['home offset option'] = True  # the offset will be applied when this option is True.
VSG2_view1['verbose'] = False  # when True, status messages will be printed.

# define parameters
VSG1_view2 = {} # view switching galvo 1 for view 2 (2 mirror view)
VSG1_view2['instrument name'] = "old DaXi"
VSG1_view2['channel I/O type'] = "AO"  #
VSG1_view2['channel_string'] = "cDAQ1AO/ao1"  # name of the DAQ channel that will be used to control the device
VSG1_view2['controlled device name'] = "view switching galvo 1 (closer to O1)"  # name of the deviced to be controlled.
VSG1_view2['description'] = "not in C planes, used for switching the view."  # purpose of this device.
VSG1_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
VSG1_view2['home offset voltage'] = 4.125  # this is an offset voltage to set on top of the home voltage value.
VSG1_view2['home offset option'] = True  # the offset will be applied when this option is True.
VSG1_view2['verbose'] = False  # when True, status messages will be printed.

# define parameters
VSG2_view2={} # view switching galvo 2 for view 2 (2 mirror view)
VSG2_view2['instrument name'] = "old DaXi"
VSG2_view2['channel I/O type'] = "AO"  #
VSG2_view2['channel_string'] = "cDAQ1AO/ao2"  # name of the DAQ channel that will be used to control the device
VSG2_view2['controlled device name'] = "view switching galvo 2 (closer to O2)"  # name of the deviced to be controlled.
VSG2_view2['description'] = "not in C planes, used for switching the view."  # purpose of this device.
VSG2_view2['home voltage'] = 0  # voltage of the home value to be sent to the specified DAQ channel.
VSG2_view2['home offset voltage'] = -3.525  # this is an offset voltage to set on top of the home voltage value.
VSG2_view2['home offset option'] = True  # the offset will be applied when this option is True.
VSG2_view2['verbose'] = False  # when True, status messages will be printed.

