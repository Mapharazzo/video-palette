import matplotlib.pyplot as plt
import numpy as np

# Recommended parameters for (K, P)
# Outputs variance, mean, x_axis
gaussian_dict = {
    (4, 4): (0.02, 0.5, 200),
    (4, 6): (0, 0, 200),
    (4, 8): (0, 0, 200),
    (8, 4): (0, 0, 200),
    (8, 6): (0, 0, 200),
    (8, 8): (0, 0, 200),
    (12, 4): (0, 0, 200),
    (12, 6): (0, 0, 200),
    (12, 8): (0, 0, 200),
}


def load_data(name, explicit=False, explicit_col=None, explicit_freq=None):
    filepath = "palettes\\" + name
    colors = np.load(file=filepath+"cols.npy")
    frequencies = np.load(file=filepath + "freqs.npy")
    if explicit:
        colors = np.load(file=explicit_col)
        frequencies = np.load(file=explicit_freq)
    return colors, frequencies


def normalize_colors(color, max_channel_value=255):
    red = color[0] / max_channel_value
    green = color[1] / max_channel_value
    blue = color[2] / max_channel_value
    return red, green, blue


def normalize_freqs(freqs):
    new_freq = [frq[1] for frq in freqs]

    total_freq = sum(new_freq)

    new_freq = [frq / total_freq for frq in new_freq]

    return new_freq


def sort_before_plot(lst1, lst2):
    to_sort = list(zip(lst1, lst2))
    to_sort.sort(key=lambda x: -x[1])

    return map(lambda x: x[0], to_sort), map(lambda x: x[1], to_sort)


def plot_colors(color_pack, color_freqs_pack, plot=True):
    idx = 0
    final_freqs = []
    final_cols = []
    final_x = []
    for cols, col_freq in zip(color_pack, color_freqs_pack):
        num_cols = len(col_freq)
        freqs = normalize_freqs(col_freq)
        x_axis = [idx, idx+1, idx+2, idx+3]

        to_sort = list(zip(cols, freqs))
        to_sort.sort(key=lambda x: -x[1])

        cols = map(lambda x: x[0], to_sort)
        freqs = map(lambda x: x[1], to_sort)

        # cols, freqs = sort_before_plot(cols, freqs)

        normalized_cols = [normalize_colors(colour) for colour in cols]

        final_freqs.append(freqs)
        final_cols.append(normalized_cols)
        final_x.append(x_axis)

        plt.stackplot(x_axis, *freqs, colors=normalized_cols)

        idx += 5

    if plot:
        plt.show()
    else:
        return x_axis, final_freqs, final_cols


# NOT YET FUNCTIONAL
def gaussian_plot(color_pack, color_freqs_pack, K, P):
    idx = 0
    variance, mean, x_axis_len = gaussian_dict[(K, P)]
    for cols, color_freq in zip(color_pack, color_freqs_pack):
        freqs = normalize_freqs(color_freq)
        cols, freqs = sort_before_plot(cols, freqs)
        x_axis = [idx * x_axis_len + k for k in range(x_axis_len)]

        normalized_cols = [normalize_colors(colour) for colour in cols]

        def gaussian_array(quot):
            aux_pi = np.sqrt(np.pi * 2)
            gauss = []
            for index in range(x_axis_len):
                x_approx = index / x_axis_len
                g = 1 / aux_pi / np.sqrt(variance) * \
                    np.exp(-((x_approx - mean) * 3)**2 / 2 / variance / 10) * quot
                gauss.append(g)

            return np.float32(gauss)

        gaussian = []
        negative_gaussian = []
        for quotient, color in zip(freqs, normalized_cols):
            arr = gaussian_array(quotient)
            gaussian.append(arr)
            negative_gaussian.append(map(lambda x: -x, arr))
        # gaussian = gaussian + negative_gaussian
        # normalized_cols = normalized_cols * 2
        plt.stackplot(x_axis, *gaussian, colors=normalized_cols)

        idx += 2

    plt.show()
