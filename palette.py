import knn_cluster
import cv2
import numpy as np
import video
import matplotlib.pyplot as plt
import plotting
import sys

# Number of colors per part
K = 8
# Number of parts
P = 12


if __name__ == '__main__':
    # using a new file
    if sys.argv[1] == '--video' or sys.argv[1] == '-v':
        file = sys.argv[2]
        vid = video.Video(file)
        filename = file.split(sep='.')[0]
        model_path = "palettes\\" + filename
        if '-k' in sys.argv:
            # Get the K value
            K = int(sys.argv[sys.argv.index('-k') + 1])

        if '-p' in sys.argv:
            # Get the P value
            P = int(sys.argv[sys.argv.index('-p') + 1])

        verbose = True if '--verbose' in sys.argv else False

        cluster = knn_cluster.Cluster(vid, K, P)
        colors, color_freq = cluster.get_part_colors(verbose=verbose)

        plotting.plot_colors(colors, color_freq)

        np.save(model_path+"cols", colors)
        np.save(model_path+"freqs", color_freq)

    if sys.argv[1] == '--load' or sys.argv[1] == '-l':
        file = sys.argv[2]
        vid = video.Video(file)
        filename = file.split(sep='.')[0]
        colors, color_freq = plotting.load_data(filename)

        plotting.plot_colors(colors, color_freq)
