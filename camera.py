# camera.py
from threading import Lock
import cv2
import os, subprocess
class VideoCamera(object):
    def __init__(self, index):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #pass
        self.lock = Lock()
        self.video = cv2.VideoCapture(index)
        self.frame = ''
        if not self.video.isOpened():
            raise Exception("Camera failed to open")
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        pass#self.video.release()
    
    def update_frame(self):
        with self.lock:
            #os.system("streamer -c /dev/video0 -b 16 -o outfile.jpeg")
            #subprocess.call("streamer -c /dev/video0 -b 16 -o ./outfile.jpeg", shell=True)
            success, image = self.video.read()
            #print image
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            ret, jpeg = cv2.imencode('.jpg', image)
            self.frame = jpeg.tobytes()#open("outfile.jpeg", "r").read()
    def get_frame(self):
        with self.lock:
            return self.frame