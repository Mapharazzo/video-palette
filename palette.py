import knn_cluster
import cv2
import numpy as np
import video
import matplotlib.pyplot as plt
import plotting
import sys
import argparse

# Adding arguments
parser = argparse.ArgumentParser()
choice = parser.add_mutually_exclusive_group(required=True)
choice.add_argument('--video', type=str,
                   help='Select the video path')
choice.add_argument('--load', type=str,
                   help='Select a previous configuration')

video_group = parser.add_argument_group()
video_group.add_argument('-k', type=int,
                         help='Number of colors per each part')
video_group.add_argument('-p', type=int,
                         help='Number of parts')
video_group.add_argument('--verbose', type=str,
                         help='See the progress verbosely')

# Number of colors per part
K = 8
# Number of parts
P = 12


if __name__ == '__main__':

    args = parser.parse_args()

    print(args.video)
    print(args.load)
    print(args.k)
    print(args.p)
    pass

    # using a new file
    if args.video:
        file = sys.argv[2]
        vid = video.Video(file)
        filename = file.split(sep='.')[0]
        model_path = "palettes\\" + filename
        if args.k:
            # Get the K value
            K = args.k

        if args.p:
            # Get the P value
            P = args.p

        verbose = True if args.verbose else False

        cluster = knn_cluster.Cluster(vid, K, P)
        colors, color_freq = cluster.get_part_colors(verbose=verbose)

        plotting.plot_colors(colors, color_freq)

        np.save(model_path+"cols", colors)
        np.save(model_path+"freqs", color_freq)

    if args.load:
        file = args.load
        vid = video.Video(file)
        filename = file.split(sep='.')[0]
        colors, color_freq = plotting.load_data(filename)

        plotting.plot_colors(colors, color_freq)
