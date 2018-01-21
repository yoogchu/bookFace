import cv2
import facial
import compare_face

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.people = []

        self.count = 0
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_fps(self):
        return self.video.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        (image, people) = facial.recog(self.people, self.video)

        #success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        return (image, people)


class VideoFeedback(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        self.video = cv2.VideoCapture('current_low_output.mp4')

    def __del__(self):
        self.video.release()

    def get_fps(self):
        return self.video.get(cv2.CAP_PROP_FPS)


    def get_frame(self):
    #(image, people) = facial.recog(self.people, self.video)

        success, image = self.video.read()
    # We are using Motion JPEG, but OpenCV defaults to capture raw images,
    # so we must encode it into JPEG in order to correctly display the
    # video stream.
        return image
