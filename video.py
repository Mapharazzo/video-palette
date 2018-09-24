import cv2
import numpy as np
import matplotlib.pyplot as plt


class Video:
    def __init__(self, path):
        self.video_path = path
        self.video = cv2.VideoCapture(path)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self._current_frame = None
        self._is_done = True
        self.frame_width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_count = self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    def is_over(self):
        return not self._is_done

    def step(self):
        self._is_done, self._current_frame = self.video.read()
        self._current_frame = cv2.cvtColor(self._current_frame, cv2.COLOR_BGR2RGB)

    def get_frame(self):
        return self._current_frame

