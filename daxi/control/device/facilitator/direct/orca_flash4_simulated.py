import copy
from time import sleep

import numpy as np
import threading

from serial import threaded


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class OrcaFlash4Simulation:
    """ This is a simulated camera that mimicks an OrcaFlash4 """

    def __init__(self, camera_index: int = 0):
        self.trigger_source = None
        self.trigger_polarity = None
        self._camera_index = camera_index
        self.dcam = None
        self.exposure_time_ms = None
        self.frame_number = None
        self.trigger_mode = None
        self.devices = None
        self.trigger_times = None
        self.output_trigger_kind = None
        self.output_trigger_polarity = None
        self.master_pulse_mode = None
        self.burst_times = None
        self.master_pulse_trigger = None
        self.buffer_size_frame_number = None
        self.image_dimension_x = None
        self.image_dimension_y = None
        self.dcamapi_initiated = False
        self.timeout_milisec = None
        self.dcam_status = None
        self.last_stack = None
        self.current_stack_index = 0

    def run(self, nb_frame: int = 100000):
        """
        Method to run the camera. It handles camera initializations and
        uninitializations as well as camera buffer allocation/deallocation.

        Parameters
        ----------
        nb_frame : int
            Number of frames to be acquired, default chosen just a big enough number.

        """
        pass

    def live_capturing_and_show(self):
        """
        this function uses the orca camera for live capturing function, and display it in a cv2 window.

        I'm now implementing some methods in a way that doesn't change anything in __init__() and run() that was already
        there when I started.
        Will re-organize these after discussion with AhmetCan.
        -- Xiyu, 2022-11-16

        highly possible we will delete this method after the discussion.
        :return:
        """
        pass

    def live_capturing_return_images_get_ready(self,
                                               nb_buffer_frames=3,
                                               timeout_milisec=100):
        """
        this function only initialize the Dcamapi, allocate buffer, let capturing start for live capturing of images
        using the orca camera. I'm calling it get_ready.

        I'm now implementing some methods in a way that doesn't change anything in __init__() and run() that was already
        there when I started.
        Will re-organize these after discussion with AhmetCan.
        -- Xiyu, 2022-11-16
        :return:
        """
        # initiate Dcamapi
        self.dcamapi_initiated = True

        # keep the symmetry with the real camera module
        if self.dcamapi_initiated:
            self.dcamapi_initiated = True
            self.dcam = SimulatedDcam(self._camera_index)
            if self.dcam.dev_open():
                self.dcam.buf_alloc(nb_buffer_frames)
                if self.dcam.cap_start():
                    self.timeout_milisec = timeout_milisec
                    self.dcam_status = 'started'

    def live_capturing_return_images_capture_image(self):
        """
        this function captures an image and return the captured image as an ndarray.

        I'm now implementing some methods in a way that doesn't change anything in __init__() and run() that was already
        there when I started.
        Will re-organize these after discussion with AhmetCan.
        -- Xiyu, 2022-11-16

        highly possible we will delete this method after the discussion.
        :return:
        """

        if self.dcam_status == 'started':
            if self.dcam.wait_capevent_frameready(self.timeout_milisec) is not False:
                print('capture the image')
                self.data = self.dcam.buf_getlastframedata()
            else:
                dcamerr = self.dcam.lasterr()
                if dcamerr.is_timeout():
                    print('===: timeout')
                else:
                    print('Dcam.wait_event() fails with error{}'.format(dcamerr))
        return self.data

    def live_capturing_return_images_capture_end(self):
        """
        this function closes up the camera, and the buffer, and uninit the api.

        I'm now implementing some methods in a way that doesn't change anything in __init__() and run() that was already
        there when I started.
        Will re-organize these after discussion with AhmetCan.
        -- Xiyu, 2022-11-16

        highly possible we will delete this method after the discussion.
       :return:
        """

        self.dcam.cap_stop()
        self.dcam.buf_release()
        # uninit the Dcamapi
        # Dcamapi.uninit()
        self.dcamapi_initiated = False

    def get_ready(self, camera_ids=[0]):
        """
        This will checkout the camera with the specified camera_id.
        With the Hamamtsu API, this would have to include the following steps:
        1. initiate the dcamapi.

        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :return:
        """
        # 1. initiate the Dcamapi
        # Dcamapi.init()
        self.dcamapi_initiated = True

        for camera_id in camera_ids:
            # 2. create the camera device with the camera index
            self.devices = {'camera ' + str(camera_id): SimulatedDcam(camera_id)}

            # 3. open the camera device
            self.devices['camera ' + str(camera_id)].dev_open()

            # 4. make sure the camera is opened
            assert self.devices['camera ' + str(camera_id)].is_opened()

    def set_configurations(self, camera_configs, camera_ids=[0]):
        """
        This will set the configuraitons for the hamamatsu camera, but without actually configure it in the hardware.
        this only stores the configuration into the object itself.

        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :return:
        """
        # todo should implement the corresponding updates in the real orca camera module.
        self.exposure_time_ms = camera_configs['exposure time (ms)']
        self.frame_number = camera_configs['frame number']
        self.trigger_mode = camera_configs['trigger mode']
        self.trigger_source = camera_configs['trigger source']
        self.trigger_polarity = camera_configs['trigger polarity']
        self.output_trigger_kind = camera_configs['output trigger kind']
        self.trigger_times = camera_configs['trigger times']
        self.output_trigger_polarity = camera_configs['output trigger polarity']
        self.master_pulse_mode = camera_configs['master pulse mode']
        self.burst_times = camera_configs['burst times']
        self.master_pulse_interval = camera_configs['master pulse interval']
        self.master_pulse_trigger = camera_configs['master pulse trigger']
        self.buffer_size_frame_number = camera_configs['buffer size (frame number)']
        self.buffer_size_stack_number = 3  # fix this ring buffer to contain 3 stacks
        self.xdim = camera_configs['xdim']
        self.ydim = camera_configs['ydim']

        # make sure all the cameras are open before setting it's configurations.
        for camera_id in camera_ids:
            if self.devices is not None:
                self.devices['camera ' + str(camera_id)].xdim = self.xdim
                self.devices['camera ' + str(camera_id)].ydim = self.ydim
                if self.devices['camera ' + str(camera_id)].is_opened():
                    pass
                else:
                    raise SystemError('open the camera first!')
            else:
                raise SystemError('the camera is not readt yet, use the .get_ready() first.')

        # takeout the Dcam object references.
        if len(camera_ids) != 1:
            print('Only 1 camera is supported right now, now we are using the first detected camera')

        # implement the case with only 1 camera.
        dcam = self.devices['camera ' + str(camera_ids[0])]  # take out the dcam object for the camera

        # set exposure time
        v = dcam.prop_setgetvalue(fValue=self.exposure_time_ms / 1000)  # The unit here seems to be in seconds.
        self.devices['camera ' + str(camera_ids[0])].exposure_time_seconds = self.exposure_time_ms / 1000
        assert abs(v - self.exposure_time_ms / 1000) < 0.00001  # make sure the exposure time is set correctly.

        # set trigger source
        if self.trigger_source == 'MASTER PULSE':
            v = dcam.prop_setgetvalue(fValue=4)  # fValue = 4 sets the trigger source to be 'MASTER PULSE'
            assert abs(v - 4) < 0.00001  # make sure it is successful.
        else:
            raise ValueError('camera trigger mode was set to ' + str(self.trigger_mode) + '; '
                                                                                          'Only \'MASTER PULSE\' is supported'
                             )

        # set trigger mode
        if self.trigger_mode == 'NORMAL':
            v = dcam.prop_setgetvalue(fValue=1)  # fValue = 1 sets the trigger mode to be 'NORMAL'.
            assert abs(v - 1) < 0.00001
        else:
            raise ValueError('camera trigger mode set to ' + str(self.trigger_mode) + '; '
                                                                                      'only \'NORMAL\' is suppoprted.')

        # set trigger polarity
        if self.trigger_polarity == 'POSITIVE':
            v = dcam.prop_setgetvalue(
                fValue=2)  # fValue = 2 sets the trigger polarity to be 'POSITIVE', 1 to be negative
            assert abs(v - 2) < 0.00001
        elif self.trigger_polarity == 'NEGATIVE':
            v = dcam.prop_setgetvalue(
                fValue=2)  # fValue = 1 sets the trigger polarity to be 'POSITIVE', 1 to be negative
            assert abs(v - 1) < 0.00001
        else:
            raise ValueError('camera trigger polarity is set to ' + str(self.trigger_polarity) + '; '
                                                                                                 'only \'POSITIVE\' and \'NEGATIVE\' are supported.')

        # set trigger times
        v = dcam.prop_setgetvalue(
            fValue=self.trigger_times)  # fValue = 1 sets the trigger times to be 10... find out what it means.
        assert abs(v - self.trigger_times) < 0.00001

        # set output trigger kind
        if self.output_trigger_kind == 'TRIGGER READY':
            v = dcam.prop_setgetvalue(fValue=4)  # fValue = 4 sets the output trigger kind to be TRIGGER READY
            assert abs(v - 4) < 0.00001
        else:
            raise ValueError('output trigger kind is set to ' + str(self.output_trigger_kind) + '; '
                                                                                                'only \'TRIGGER READY\' is supported')

        # set output trigger polairty
        if self.output_trigger_polarity == 'POSITIVE':
            v = dcam.prop_setgetvalue(fValue=2)  # fValue = 2 sets the trigger polarity to be 'POSITIVE'
            assert abs(v - 2) < 0.00001

        elif self.output_trigger_polarity == 'NEGATIVE':
            v = dcam.prop_setgetvalue(fValue=1)  # fValue = 2 sets the trigger polarity to be 'POSITIVE'
            assert abs(v - 1) < 0.00001
        else:
            raise ValueError('output trigger polairty is set to ' + str(self.output_trigger_polarity) + ';'
                                                                                                        'only \'POSITIVE\' and \'NEGATIVE\' are supported.')

        # set output trigger base sensor
        v = dcam.prop_setgetvalue(fValue=1)  # fValue = 1 sets the output trigger sensor to be 'VIEW 1'.
        assert abs(v - 1) < 0.00001

        # set master pulse mode
        if self.master_pulse_mode == 'CONTINUOUS':
            v = dcam.prop_setgetvalue(fValue=1)  # fValue = 3 is burst mode, 1 is continuous mode. 2 is start mode.
            assert abs(v - 1) < 0.00001
        elif self.master_pulse_mode == 'START':
            v = dcam.prop_setgetvalue(fValue=2)  # fValue = 3 is burst mode, 1 is continuous mode. 2 is start mode.
            assert abs(v - 2) < 0.00001
        elif self.master_pulse_mode == 'BURST':
            v = dcam.prop_setgetvalue(fValue=3)  # fValue = 3 is burst mode, 1 is continuous mode. 2 is start mode.
            assert abs(v - 3) < 0.00001
            # set master pulse burst times

            v = dcam.prop_setgetvalue(fValue=self.burst_times)
            assert abs(v - self.burst_times) < 0.00001
        else:
            raise ValueError('master pulse mode is set to ' + str(self.master_pulse_mode) + ';'
                                                                                            'only \'CONTINUOUS\', \'START\' and \'BURST\' are supported.')

        # set master pulse interval
        v = dcam.prop_setgetvalue(fValue=self.master_pulse_interval)
        assert abs(v - self.master_pulse_interval) < 0.00001

        # -- set master pulse trigger to be external trigger:
        if self.master_pulse_trigger == 'EXTERNAL':
            v = dcam.prop_setgetvalue(fValue=1)  # this sets the trigger source to be external.
            assert abs(v - 1) < 0.00001
        elif self.master_pulse_trigger == 'SOFTWARE':
            v = dcam.prop_setgetvalue(fValue=2)  # 2 sets the trigger source to be software trigger.
            assert abs(v - 2) < 0.00001
        else:
            raise ValueError('master pulse trigger is set to ' + str(self.master_pulse_trigger) + ';'
                                                                                                  'only \'CONTINUOUS\', \'EXTERNAL\' and \'SOFTWARE\' are supported.')

        # allocate buffer
        dcam.buf_alloc(self.buffer_size_frame_number)  # in real devices, should subtract 1.

    def start(self, camera_ids=[0]):
        """
        This will start the cameres

        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :return:
        """
        for camera_id in camera_ids:
            self.devices['camera ' + str(camera_id)].cap_start()

    def capture(self):
        """
        This will capture an image, and return the image as an ndarray

        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :return:
        """
        pass

    def stop(self, camera_ids=[0]):
        """
        this will stop the capturing of the cameras
        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :param camera_ids:
        :return:
        """
        for camera_id in camera_ids:
            self.devices['camera ' + str(camera_id)].cap_stop()

    def release_buffer(self, camera_ids=[0]):
        """
        this will release the buffers for all the cameras
        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :param camera_ids:
        :return:
        """
        for camera_id in camera_ids:
            self.devices['camera ' + str(camera_id)].buf_release()

    def close(self, camera_ids=[0]):
        """
        This will close the camera device, and un-initi the Dcamapi.

        I'm implementing this with similar "pattern" as I used in Daxi-controller for now - Xiyu.

        :return:
        """
        for camera_id in camera_ids:
            self.devices['camera ' + str(camera_id)].dev_close()

        # Dcamapi.uninit()
        self.dcamapi_initiated = False

    def retrieve_1_frame_from_1_camera(self, camera_id, frame_index):
        # dcam = self.devices['camera '+str(camera_id)]
        frame = self.devices['camera ' + str(camera_id)].buf_getframedata(frame_index)
        return frame

    def get_any_stack(self, camera_id, stack_index):
        """This will return the last acquired stack as an numpy.ndarray"""
        ind = stack_index
        z = int(self.buffer_size_frame_number/3)
        stack = np.ones([self.xdim, self.ydim, z], dtype='float')
        for i in np.arange(z):
            frame_index = ind*z + i
            image = self.retrieve_1_frame_from_1_camera(camera_id=camera_id, frame_index=frame_index)
            stack[:, :, i] = image

        self.last_stack = stack
        return self.last_stack

    def capturing_data_message(self, option, camera_ids=[0]):
        if option == 'on':
            for camera_id in camera_ids:
                self.devices['camera ' + str(camera_id)].message = True

        if option == 'off':
            for camera_id in camera_ids:
                self.devices['camera ' + str(camera_id)].message = False

    def get_current_stack_index(self, current_frame_count):
        frame_index = current_frame_count
        # self.devices['camera ' + str(camera_id)].current_buffer_index
        stack_index = int(frame_index/(int(self.buffer_size_frame_number/3)))
        self.current_stack_index = stack_index
        return stack_index

    def get_current_stack(self, camera_id, current_frame_count):
        """This will return the last acquired stack as an numpy.ndarray"""
        stack_index = self.get_current_stack_index(current_frame_count=current_frame_count)
        self.get_any_stack(camera_id=camera_id, stack_index=stack_index)
        print('current stack index is '+ str(current_frame_count))
        return self.last_stack


class SimulatedDcam():
    def __init__(self, camera_id):
        self.devices_opened = None
        self.camera_id = camera_id
        self.readme = 'this is a simualted Dcam object'
        self.device_opened = False
        self.capture_status = None
        self.exposure_time_seconds = 0.001
        self.buffer_allocated = False
        self.buffer = None
        self.capture_thread_handle = None
        self.message = True
        self.xdim = None
        self.ydim = None
        self.current_buffer_index = None
        # may need to remove this out from the Dcam.

    def dev_open(self):
        self.device_opened = True
        return True

    def dev_close(self):
        self.devices_opened = False

    def is_opened(self):
        return self.device_opened

    def cap_start(self):
        self.capture_status = 'started'
        # once the camera starts, it should start the data feeder into its buffer
        # on the simulated dcam object
        self.capture_thread_handle = self.simulated_camera_data_feeder()
        return True

    def buf_alloc(self, buffer_size):
        self.buffer_allocated = True
        self.buffer = np.zeros([self.xdim, self.ydim, buffer_size], dtype='int16')

    def wait_capevent_frameready(self, timeout_milisec):
        print('wait for a capture event for ' + str(timeout_milisec) + 'ms, then return True. '
                                                                       'This is simulated dcam object, '
                                                                       'so we will just let it go and return True.')
        return True

    def buf_getlastframedata(self):
        if self.capture_status == 'started':
            im = np.random.randn(self.xdim, self.ydim) * 1000
            data = im.astype('uint16')
        else:
            data = None
        return data

    def lasterror(self):
        return 'no error, this is a simualted device'

    def is_timeout(self):
        print('no time out, this is a simualted device')
        return False

    def cap_stop(self):
        self.capture_status = 'stopped'
        sleep(0.05)
        self.capture_thread_handle.join()

    def buf_release(self):
        self.buffer = None

    def buf_getframedata(self, frame_index):
        data = self.buffer[:, :, frame_index]
        return data

    def prop_setgetvalue(self, idprop=None, fValue=None):
        """

        this only sets the same format with the prop_setgetvalue from dcam, but
        it will always work successfully in this simulated dcam.

        """

        print('setting this idproperty:' + str(idprop))
        return fValue

    @threaded
    def simulated_camera_data_feeder(self):
        x, y, buffer_size = self.buffer.shape
        z = int(buffer_size / 3)
        while self.capture_status == 'started':
            for i0 in np.arange(3):
                object = simulate_a_random_object_3d_stack(x, y, z)
                for i1 in np.arange(z):
                    i = i0 * z + i1
                    if self.capture_status == 'started':
                        if self.message is True:
                            print(' simulated camera on a threaded process - acquiring frame '
                                  + str(i) + ' in buffer [o] to [' + str(buffer_size) +
                                  '], type m-off to hide this message')
                        frame = object[:, :, i1]
                        sleep(self.exposure_time_seconds)
                        self.buffer[:, :, i] = copy.deepcopy(frame.astype('uint16'))
                        self.current_buffer_index = i
                        sleep(0.01)
                    else:
                        break


def simulate_a_random_object_3d_stack(x=100, y=200, z=300):
    stack = np.random.rand(x, y, z)
    x0 = int(np.random.rand(1) * x / 5)
    x1 = int(min(x - 1, x0 + x / 10 + x / 10 * np.random.rand(1) * 5))

    y0 = int(np.random.rand(1) * y / 5)
    y1 = int(min(y - 1, y0 + y / 10 + y / 10 * np.random.rand(1) * 5))

    z0 = int(np.random.rand(1) * z / 5)
    z1 = int(min(z - 1, z0 + z / 10 + z / 10 * np.random.rand(1) * 5))
    stack[x0:x1, y0:y1, z0:z1] = max(stack.ravel())*1.2
    print('x range is ' + str(x0) + ' to ' + str(x1))
    print('y range is ' + str(y0) + ' to ' + str(y1))
    print('z range is ' + str(z0) + ' to ' + str(z1))
    return stack
