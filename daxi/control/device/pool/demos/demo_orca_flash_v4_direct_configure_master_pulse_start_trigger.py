import datetime
from copylot.hardware.orca_camera.dcam import Dcamapi, Dcam
from copylot.hardware.orca_camera.dcamapi4 import *

import numpy as np


def dcam_get_properties_name_id_dict(iDevice=0):
    """
    Show supported properties
    """
    name_id_dict = {}
    if Dcamapi.init() is not False:
        dcam = Dcam(iDevice)
        if dcam.dev_open() is not False:
            idprop = dcam.prop_getnextid(0)
            while idprop is not False:
                nameprop = dcam.prop_getname(idprop)
                if nameprop is not False:
                    name_id_dict[nameprop] = idprop

                idprop = dcam.prop_getnextid(idprop)

            dcam.dev_close()
        else:
            print('-NG: Dcam.dev_open() fails with error {}'.format(dcam.lasterr()))
    else:
        print('-NG: Dcamapi.init() fails with error {}'.format(Dcamapi.lasterr()))

    Dcamapi.uninit()
    return name_id_dict


def get_first_pixel_sequences():
    first_pixels=[]
    for i0 in  np.arange(1000):
        a=dcam.buf_getframedata(i0)
        if a is not False:
            first_pixels.append(a[0][0])
    ps = np.asarray(first_pixels)
    return ps

# initiate Dcamapi:
Dcamapi.init()

# create the (camera device) Dcam object with the device index
iDevice = 0
dcam = Dcam(iDevice)


# open the deivce
dcam.dev_open()

dcam.is_opened()



# -- try to set exposure time # todo - need to verify if this is working. and think about the order.
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.EXPOSURETIME,
                          fValue=0.2)  # The unit here seems to be in seconds.
print('1 - ' + str(v))

print('exposure time: '+str(v)+' seconds.')
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGER_MODE,
                          fValue=3)  # fValue = 1 sets the trigger mode to be 'NORMAL'.
print('2 - ' + str(v))

dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGER_CONNECTOR, fValue=2)

v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGERACTIVE,
                      fValue=1)  # 1 set the TRIGGER ACTIVE to be EDGE. (seems like it can only be EDGE, or SYNCREADOUT(3))
print(v)


v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGERPOLARITY,
                          fValue=2)  # fValue = 2 sets the trigger polarity to be 'POSITIVE', 1 to be negative
print(v)


# -- set master pulse
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGERSOURCE,
                          fValue=4)  # fValue = 4 sets the trigger source to be 'MASTER PULSE'
print(v)


# -- set master pulse trigger to be external trigger:
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.MASTERPULSE_TRIGGERSOURCE,
                          fValue=1)  # this sets the trigger source to be external.
print(v)



# -- choose master pulse burst mode
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.MASTERPULSE_MODE,
                          fValue=2)  # fValue = 3 is burst mode, 1 is continuous mode. 2 is start mode.
print(v)


# # -- set burst mode burst times:
# v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.MASTERPULSE_BURSTTIMES,
#                           fValue=30)

# -- set burst mode burst times:
v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.MASTERPULSE_INTERVAL,
                          fValue=0.01)
print(v)


# v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.TRIGGERTIMES,
#                           fValue=10)  # fValue = 1 sets the trigger times to be 10... find out what it means.
# print(v)

v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.OUTPUTTRIGGER_KIND,
                          fValue=4)  # fValue = 4 sets the output trigger kind to be TRIGGER READY
print(v)

v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.OUTPUTTRIGGER_POLARITY,
                          fValue=2)  # fValue = 2 sets the trigger polarity to be 'POSITIVE'
print(v)

v = dcam.prop_setgetvalue(idprop=DCAM_IDPROP.OUTPUTTRIGGER_BASESENSOR,
                          fValue=1)  # fValue = 1 sets the output trigger sensor to be 'VIEW 1'.

print(v)

# allocate buffer
dcam.buf_alloc(200)

# -- capturing start:
dcam.cap_start()

p = ''
while p != 'q':
    p = input('press q to exit ...')

# -- define timeout time
timeout_milisec = 300000  # when testing, run this script at debug mode, and pause here at this line.

# -- stop the capturing
dcam.cap_stop()

# dcam.prop_getvaluetext(idprop = DCAM_IDPROP.OUTPUTTRIGGER_BASESENSOR, fValue=2)

# release buffer
dcam.buf_release()

# close device
dcam.dev_close()

# un init the Dcamapi
Dcamapi.uninit()

