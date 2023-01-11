import numpy as np

# need to think about some format standard here that will cover all 6 acquisition modes.
# the comonality is stack by stack... so make a stack a unit.


class StackProcessing:
    def __init__(self):
        print('stack processing initiated...')
        self.camera = None  # this will be the device object that belongs to the camera category.
        self.last_frame = None
        self.mip0 = None
        self.mip1 = None
        self.mip2 = None
        self.stitched_mips = None
        self.last_stack = abs(np.random.randn(100, 100, 100))
        self.data_window = {'x start index': 100,
                               'x end index': 300,
                               'y start index': 100,
                               'y end index': 400,
                               'z start index': 0,
                               'z end index': 100}

        # need to think about something about the 3 time points ring buffer.
        # maybe should do the ring buffer in the camera module. But here, just take the last stack
        # use the simulated camera for this.

    def get_last_frame(self):
        data = self.camera.buf_getlastframedata()
        self.last_frame = data
        return data

    def _retrieve_last_stack(self, camera_id, current_frame_count):
        """this will take the entire stack from the current buffer"""
        # ToDo - need to implement this method in the camera module.
        self.last_stack = self.camera.get_current_stack(camera_id=camera_id,
                                                        current_frame_count=current_frame_count,
                                                        data_window=self.data_window)
        return self.last_stack

    def _get_current_3d_mips(self):
        self.mip0, self.mip1, self.mip2, self.stitched_mips = get_3d_mips(self.last_stack)

    def get_current_stitched_mips(self, camera_id, current_frame_count):
        self._retrieve_last_stack(camera_id=camera_id,
                                  current_frame_count=current_frame_count)
        self._get_current_3d_mips()
        return self.stitched_mips


def get_3d_mips(stack, stitched_mips_only=False):
    mip0 = np.max(stack, axis=0)
    mip1 = np.max(stack, axis=1)
    mip2 = np.max(stack, axis=2)
    dim0, dim1, dim2 = stack.shape
    stitched = np.zeros([dim0+dim2, dim1+dim2], dtype='float32')
    stitched[0:dim0, 0:dim1] = mip2
    stitched[dim0:dim0+dim2, 0:dim1] = mip0.T
    stitched[0:dim0, dim1:dim1+dim2] = mip1
    stitched[dim0:dim0+dim2, dim1:dim1+dim2] = np.ones([dim2, dim2], dtype='float32')*mip2[dim0-10, dim1-10]
    if stitched_mips_only is True:
        return stitched
    else:
        return mip0, mip1, mip2, stitched
