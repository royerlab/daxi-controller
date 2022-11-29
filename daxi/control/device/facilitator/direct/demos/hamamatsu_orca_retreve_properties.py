from copylot.hardware.orca_camera.dcam import *


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


def dcam_get_properties_text_dict(name_id_dict, dcam, name, fvalue):

    idprop = name_id_dict[name]
    text = dcam.prop_getvaluetext(idprop=idprop, fValue=fvalue)
    return text


if __name__ == "__main__":
    name_id_dict = dcam_get_properties_name_id_dict()
    Dcamapi.init()
    dcam = Dcam(iDevice=0)
    dcam.dev_open()
    name = 'TRIGGER MODE'
    vs = [0, 1, 2, 3, 4]
    for v in vs:
        text = dcam.prop_getvaluetext(idprop=name_id_dict[name], fValue=v)
        if text is not False:
            print('name: ' + name + '; fValue='+str(v),'; '+text)
        1;


prop_names = []
prop_names.append('TRIGGER SOURCE')
prop_names.append('EXPOSURE TIME')
prop_names.append()

# set external
