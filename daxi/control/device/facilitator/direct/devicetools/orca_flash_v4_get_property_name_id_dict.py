from copylot.hardware.orca_camera.dcam import *


def dcam_get_properties_name_id_dict(iDevice=0):
    """
    Show supported properties.
    This method will close the camera eventually, so it should not be used in any ongoing processes.

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
