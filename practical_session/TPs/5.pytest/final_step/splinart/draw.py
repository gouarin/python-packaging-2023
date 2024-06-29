# Author:
#     Loic Gouarin <loic.gouarin@gmail.com>
#
# License: BSD 3 clause
"""
draw module
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from .color import DEFAULT_COLOR


def draw_pixel(img, xs, ys, scale_color=0.0005, color=DEFAULT_COLOR):
    """
    draw pixel
    """
    size = img.shape[0]
    newxs = np.floor(xs * size)
    xs_mask = np.logical_and(newxs >= 0, newxs < size)
    newys = np.floor(ys * size)
    ys_mask = np.logical_and(newys >= 0, newys < size)
    mask = np.logical_and(xs_mask, ys_mask)
    coords = np.asarray([newxs[mask], newys[mask]], dtype="i8")
    img_color = np.asarray(color) * scale_color
    pixels = img[coords[0, :], coords[1, :], :]
    alpha = 1.0 - img_color[3]
    img[coords[0, :], coords[1, :], :] = img_color + pixels * alpha


def save_img(img, path, filename):
    """
    save image
    """
    plt.imshow(img)
    plt.axes().set_aspect("equal")
    plt.axis("off")

    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + filename, dpi=300, bbox_inches="tight")


def show_img(img):
    """
    show image
    """
    plt.imshow(img)
    plt.axes().set_aspect("equal")
    plt.axis("off")
    plt.show()
