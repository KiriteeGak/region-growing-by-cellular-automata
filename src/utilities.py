import numpy as np


def rgb_to_gray_scale_conversion(image_array):
    gray_scale_image = []
    for col in image_array:
        gray_scale_image.append([weighted_average_gray_conversion(row) for row in col])
    return gray_scale_image


def weighted_average_gray_conversion(pixel):
    return np.mean(np.array(pixel))
