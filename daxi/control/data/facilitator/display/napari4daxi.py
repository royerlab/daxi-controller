import napari
import time

from napari._qt.qthreading import thread_worker
from cv2 import VideoCapture
from napari.layers import Points
from skimage.color import rgb2gray
import numpy as np
from skimage import draw

camera_index = 0


def acquire_image(camera : VideoCapture):
    """
    Acquires an image from a given camera
    """

    # acquire image
    _, picture = camera.read()
    if picture is None:
        return
    # convert to single channel image
    return rgb2gray(picture)


def get_random_images():
    picture = np.random.randn(1024, 1024)
    return picture


class DaXiViewer:
    def __init__(self):
        self.camera_index = 0

    def update_layers(self, images_data: dict):
        """
        Add images to napari is layer or updates a pre-existing layer
        """
        for name in images_data.keys():
            self.image = images_data[name]
            for layer in self.viewer.layers:
                if layer.name == name:
                    layer.data = self.image
                    self.image = None
                    break

            if self.image is not None:
                if "point" in name:
                    self.viewer.add_points(self.image, name=name, face_color='red')
                else:
                    self.viewer.add_image(self.image, name=name)

    def process_image(self, image):
        if isinstance(self.camera, VideoCapture):
            # estimate maximum position
            from scipy.ndimage import center_of_mass
            y, x = center_of_mass(np.power(image, 10000))

            # put a point around maximum
            self.points = np.asarray([[y, x]])

            # send dictionary of images back to napari
            return {
                "original": image,
                "brightest point": self.points
            }
        else:
            return {
                "stitched mips": image,
            }

    def prepare(self, image_feeder=None, camera=None, processor=None, counter=None):
        # create a viewer window
        self.viewer = napari.Viewer()

        # connect to webcam
        self.camera = camera  # VideoCapture(camera_index)

        # image feeder
        self.image_feeder = image_feeder

        # processor
        self.processor = processor

        # counter
        self.counter = counter

        # release camera
        if isinstance(self.camera, VideoCapture):
            self.camera_release = self.camera.release
        else:
            self.camera_release = self.camera_release_orca

    def camera_release_orca(self):
        self.camera.stop()
        self.camera.release_buffer()
        self.camera.close()


    # https://napari.org/guides/stable/threading.html
    @thread_worker
    def loop_run(self):
        while True:  # endless loop
            self.image = self.image_feeder(camera=self.camera, processor=self.processor, counter=self.counter)
            yield self.process_image(self.image)
            time.sleep(0.05)

    def start(self):
        # Start the loop
        self.worker = self.loop_run()
        self.worker.yielded.connect(self.update_layers)
        self.worker.aborted.connect(self.camera_release_orca)
        self.worker.start()

        # Start napari
        napari.run()
