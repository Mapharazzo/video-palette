import cv2
import numpy as np
import video
import time
import matplotlib.pyplot as plt
from collections import Counter


class Cluster:
    estimated_shot_length = 4

    def __init__(self, vid, colors_cluster, num_clusters):
        self._video = vid
        self.stochastic_constant = 0.1
        self.number_clusters = num_clusters
        self.colors_per_cluster = colors_cluster
        self._default_labels = None
        self._default_on = False

        # Number of seconds in each of the color clusters
        self.part_seconds = self._video.frame_count // self._video.fps // self.number_clusters
        self.colors = []
        self.color_freq = []

    def _get_default_labels(self, ksize, width, height):
        labels = []
        mid_line = height // 2
        mid_col = width // 2
        for line in range(height):
            for col in range(width):
                aux_line = int(abs(mid_line - line) / mid_line * ksize)
                if aux_line == ksize:
                    aux_line -= 1

                aux_col = int(abs(mid_col - col) / mid_col * ksize)
                if aux_col == ksize:
                    aux_col -= 1

                labels.append([int((aux_col+aux_line) / 2)])

        return labels

    def _shrink_image(self, frame):
        # Target size should be 240p
        new_h = 120
        new_w = int(self._video.frame_width // self._video.frame_height * new_h)

        # Area for shrinking
        # https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA), new_h, new_w

    def _get_shot_batch(self, estimated=estimated_shot_length):
        # Estimated shot length is 5 seconds
        shot_frames = int(estimated * self._video.fps)
        batch = []
        for idx in range(shot_frames):
            self._video.step()
            # print(len(batch))
            if self._video.is_over():
                break

            # Stochastic approach
            if np.random.random() > self.stochastic_constant:
                continue
            frame = self._video.get_frame()

            shrinked_frame, shrinked_w, shrinked_h = self._shrink_image(frame)

            # Now we need to do Color Quantization
            # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html

            Z = shrinked_frame.reshape(-1, 3)
            Z = np.float32(Z)

            # print(Z)

            # Criteria for k-means:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 15, 1.0)

            # Number of clusters:
            K = self.colors_per_cluster

            # Likely location of cluster centers in a real-life frame
            if not self._default_on:
                self._default_labels = self._get_default_labels(K, shrinked_w, shrinked_h)
                self._default_labels = np.array(self._default_labels)
                self._default_labels = self._default_labels.ravel()
                self._default_on = True

            # Only need the centers - which are in fact the colors
            # _, _, centers = cv2.kmeans(Z, K, self._default_labels, criteria, 10, cv2.KMEANS_USE_INITIAL_LABELS)
            _, _, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

            center = np.uint8(centers)

            batch.append(center)

        return batch

    def get_part_colors(self, estimated=estimated_shot_length, verbose=False):
        start = time.time()
        number_of_batches = int(self.part_seconds // estimated)

        for idx in range(self.number_clusters):
            # Get number_of_batches batches
            reds = []
            greens = []
            blues = []

            for _ in range(number_of_batches):
                batch = self._get_shot_batch()
                reds += [color[0] for color in batch]
                greens += [color[1] for color in batch]
                blues += [color[2] for color in batch]

            # Now another clustering so we get only the relevant colors from the batches

            stacked = np.vstack((reds, greens, blues))

            stacked = np.float32(stacked)

            # Another criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, center = cv2.kmeans(stacked, self.colors_per_cluster,
                                           None, criteria, 15, cv2.KMEANS_PP_CENTERS)

            top_labels = [label[0] for label in labels]
            label_count = Counter(top_labels)

            center = np.int32(center)

            if verbose:
                print("At part number {}:".format(idx))
                print(center)

            self.colors.append(tuple(center))
            self.color_freq.append(list(label_count.items()))

        stop = time.time()
        if verbose:
            print("ELAPSED: {} seconds".format(stop - start))

        return self.colors, self.color_freq
