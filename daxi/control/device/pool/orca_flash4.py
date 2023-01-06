from copylot.hardware.orca_camera.camera import OrcaCamera
import numpy as np


class OrcaFlash4(OrcaCamera):
    """
    directly use the OrcaCamera class from coPylot, which was used as a dependency.
    """
    def __init__(self):
        pass

    def retrieve_1_frame_from_1_camera(self, camera_id, frame_index):
        # dcam = self.devices['camera '+str(camera_id)]
        frame = self.devices['camera ' + str(camera_id)].buf_getframedata(frame_index+1)
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
