# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023-11-24 09:02:38
# @Copyright:  www.shujiajia.com  Inc. All rights reserved.
# Description: 注意：本内容仅限于数据堂公司内部传阅，禁止外泄以及用于其他的商业目的
# -------------------------------------------------------------------------------
import numpy as np


def xyxy2xywh(x: list):
    """_summary_

    Args:
        x: [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right

    Returns:
       [x, y, w, h]
    """
    y = np.copy(x)
    y[..., 0] = (x[..., 0] + x[..., 2]) / 2  # x center
    y[..., 1] = (x[..., 1] + x[..., 3]) / 2  # y center
    y[..., 2] = x[..., 2] - x[..., 0]  # width
    y[..., 3] = x[..., 3] - x[..., 1]  # height
    return y


def xywh2xyxy(x: list):
    """_summary_

    Args:
        x: [x, y, w, h]

    Returns:
        [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    """
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2  # top left x
    y[..., 1] = x[..., 1] - x[..., 3] / 2  # top left y
    y[..., 2] = x[..., 0] + x[..., 2] / 2  # bottom right x
    y[..., 3] = x[..., 1] + x[..., 3] / 2  # bottom right y
    return y


def xyxy2coordinates(top_left: list, bottom_right: list):
    """_summary_

    Args:
        top_left: [x1,y1]
        bottom_right: [x2,y2]

    Returns:
        [top_left, top_right, bottom_right, bottom_left, top_left]
    """
    x1, y1 = top_left
    x2, y2 = bottom_right

    top_right = (x2, y1)
    bottom_left = (x1, y2)

    return [top_left, top_right, bottom_right, bottom_left, top_left]


def coordinates2xyxy(coordinates: list):
    """_summary_

    Args:
        coordinates: [[x1,y1],[x2,y2]..]

    Returns:
       [top_left, bottom_right]
    """
    x_coordinates = [point[0] for point in coordinates]
    y_coordinates = [point[1] for point in coordinates]

    top_left = [min(x_coordinates), min(y_coordinates)]
    bottom_right = [max(x_coordinates), max(y_coordinates)]

    return [top_left, bottom_right]
