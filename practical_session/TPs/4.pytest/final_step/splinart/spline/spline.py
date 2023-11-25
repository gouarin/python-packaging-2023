# Author:
#     Loic Gouarin <loic.gouarin@gmail.com>
#
# License: BSD 3 clause
"""
spline module
"""
import numpy as np


def spline(xs, ys):
    """
    return spline
    """
    n = xs.shape[0]
    u_i = np.zeros_like(ys)
    y2s = np.zeros_like(ys)

    dif = np.diff(xs)
    sig = dif[:-1] / (xs[2:] - xs[:-2])

    if ys.ndim == 2:
        dif = dif[:, np.newaxis]

    u_i[1:-1] = (ys[2:] - ys[1:-1]) / dif[1:] - (ys[1:-1] - ys[:-2]) / dif[:-1]

    for i in range(1, n - 1):
        p_i = sig[i - 1] * y2s[i - 1] + 2.0
        y2s[i] = (sig[i - 1] - 1) / p_i
        u_i[i] = (6 * u_i[i] / (xs[i + 1] - xs[i - 1]) - sig[i - 1] * u_i[i - 1]) / p_i

    for i in range(n - 2, -1, -1):
        y2s[i] = y2s[i] * y2s[i + 1] + u_i[i]

    return y2s
