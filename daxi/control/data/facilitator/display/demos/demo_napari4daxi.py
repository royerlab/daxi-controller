from daxi.control.data.facilitator.display.napari4daxi import DaXiViewer, acquire_image
from cv2 import VideoCapture


def demo_daxiviewer():
    a = DaXiViewer()
    a.prepare(image_feeder=acquire_image,
              camera=VideoCapture(0)
              )
    a.go()
    return 'success'


if __name__ == '__main__':
    demo_daxiviewer()
