from old_workbench.hamamatsu.dcamapi_helpers import *
import cv2

iDevice = 0  # Define the index of the device


def dcamtest_show_framedata(data, windowtitle, iShown):
    """
    Show numpy buffer as an image

    Arg1:   NumPy array
    Arg2:   Window name
    Arg3:   Last window status.
        0   open as a new window
        <0  already closed
        >0  already openend
    """
    if iShown > 0 and cv2.getWindowProperty(windowtitle, 0) < 0:
        return -1  # Window has been closed.
    if iShown < 0:
        return -1  # Window is already closed.

    if data.dtype == np.uint16:
        imax = np.amax(data)
        if imax > 0:
            imul = int(65535 / imax)
            # print('Multiple %s' % imul)
            data = data * imul

        cv2.imshow(windowtitle, data)
        return 1
    else:
        print('-NG: dcamtest_show_image(data) only support Numpy.uint16 data')
        return -1


if Dcamapi.init() is True:  # initialize Dcamapi, return True if succeeded.
    print('dcamapi initialized')
    dcam = Dcam(iDevice)  # define the instance of the device
    print('created camera instance')
    if dcam.dev_open() is True:  # open the device, return True if succeeded.
        if dcam.buf_alloc(1) is True:  # allocate buffer for the device.
            ###############################################################

            # dcamtest_thread_live(dcam)  # live acquisition
            if dcam.cap_start() is True:  # capturing start
                timeout_milisec = 1000  # define a time out value in ms.
                iWindowStatus = 0  # ??
                imind=0
                while iWindowStatus >= 0:
                    if dcam.wait_capevent_frameready(timeout_milisec) is True:  # ??
                        data = dcam.buf_getlastframedata()  # read out the last frame
                        print('image'+str(imind))
                        imind+=1
                        iWindowStatus = dcamtest_show_framedata(data, 'test', iWindowStatus)
                    else:
                        dcamerr = dcam.lasterr()
                        if dcamerr.is_timeout():
                            print('===: timeout')
                        else:
                            print('-NG: Dcam.wait_event() fails with error {}'.format(dcamerr))
                            break

                    key = cv2.waitKey(1)
                    if key == ord('q') or key == ord('Q'):  # if 'q' was pressed with the live window, close it
                        break

                dcam.cap_stop()

            ###############################################################

            dcam.buf_release()  # release the buffer
        dcam.dev_close()
Dcamapi.uninit()
