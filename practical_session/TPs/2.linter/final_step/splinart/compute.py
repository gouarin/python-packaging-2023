# Author:
#     Loic Gouarin <loic.gouarin@gmail.com>
#
# License: BSD 3 clause
"""
Compute module
"""
import numpy as np

from .spline import spline, splint
from .draw import draw_pixel
from .color import DEFAULT_COLOR


def update_path(path, periodic=False, scale_value=0.00001):
    """
    update the path
    """
    n = path.shape[0]
    scale = np.arange(n) * scale_value
    radius = 1.0 - 2.0 * np.random.random(n)
    noise = radius * scale
    phi = np.random.random(n) * 2 * np.pi
    rnd = np.c_[np.cos(phi), np.sin(phi)]
    path += rnd * noise[:, np.newaxis]
    if periodic:
        path[-1] = path[0]


# pylint: disable=too-many-arguments
def update_img(
    img,
    path,
    xs_func,
    x=None,
    nrep=300,
    periodic=True,
    scale_color=0.005,
    color=DEFAULT_COLOR,
    scale_value=0.00001,
):
    """
    update image
    """
    xspline = xs_func()

    if x is not None:
        yspline = np.zeros((xspline.size, 2))
    else:
        yspline = np.zeros(xspline.size)

    for i in range(nrep):  # pylint: disable=unused-variable
        if x is not None:
            yder2 = spline(x, path)
            xspline = xs_func()
            splint(x, path, yder2, xspline, yspline)
            draw_pixel(img, yspline[:, 0], yspline[:, 1], scale_color, color)
        else:
            yder2 = spline(path[:, 0], path[:, 1])
            xspline = xs_func()
            splint(path[:, 0], path[:, 1], yder2, xspline, yspline)
            draw_pixel(img, yspline, xspline, scale_color, color)
        update_path(path, scale_value=scale_value, periodic=periodic)
