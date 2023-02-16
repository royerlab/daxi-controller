from daxi.control.data.facilitator.processing.process_stacks import get_3d_mips

stack = self.devices_fcltr.camera.get_current_stack(camera_id=0, current_frame_count=14)
mip0, mip1, mip2, stitched = get_3d_mips(stack, stitched_mips_only=False)
from skimage.io import imsave, imread
m = np.transpose(stack, (2, 0, 1))
imsave('test.tif', m)
