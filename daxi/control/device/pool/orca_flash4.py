from copylot.hardware.orca_camera.camera import OrcaCamera
import numpy as np


class OrcaFlash4(OrcaCamera):
    """
    directly use the OrcaCamera class from coPylot, which was used as a dependency.
    """
    def __init__(self):
        pass

    def retrieve_1_frame_from_1_camera(self, camera_id, frame_index, data_window=None):
        # dcam = self.devices['camera '+str(camera_id)]
        frame = self.devices['camera ' + str(camera_id)].buf_getframedata(frame_index)
        if data_window is None:
            output = frame
        else:
            x0=data_window['x start index']
            x1=data_window['x end index']
            y0=data_window['y start index']
            y1=data_window['y end index']
            if isinstance(frame, bool):
                output = frame
            else:
                output = frame[x0:x1, y0:y1]
        return output

    def get_any_stack(self, camera_id, stack_index, data_window=None):
        """This will return the last acquired stack as an numpy.ndarray"""
        ind = stack_index
        z = int(self.buffer_size_frame_number / 3)
        if data_window is None:
            stack = np.ones([self.xdim, self.ydim, z], dtype='float')
            z_start=0
            z_end=z
        else:
            x_dim = data_window['x end index'] - data_window['x start index']
            y_dim = data_window['y end index'] - data_window['y start index']
            z_dim = data_window['z end index'] - data_window['z start index']
            z_start = data_window['z start index']
            z_end = data_window['z end index']
            stack = np.ones([x_dim, y_dim, z_dim], dtype='float')

        for i in np.arange(z_start, z_end):
            frame_index = ind*z + i
            image = self.retrieve_1_frame_from_1_camera(camera_id=camera_id,
                                                        frame_index=frame_index,
                                                        data_window=data_window)
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
        print('current stack index is' + str(stack_index))
        return stack_index

    def get_current_stack(self, camera_id, current_frame_count, data_window=None):
        """This will return the last acquired stack as an numpy.ndarray"""
        stack_index = self.get_current_stack_index(current_frame_count=current_frame_count)
        self.get_any_stack(camera_id=camera_id, stack_index=stack_index, data_window=data_window)
        print('current stack index is '+ str(current_frame_count))
        return self.last_stack
