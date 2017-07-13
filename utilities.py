import numpy as np


class PreprocessingImage:
    def rgbToGrayscaleConversion(self, image_array):
        grayscaled_image = []
        for col in image_array:
            grayscaled_image.append([self.weightedAverageGrayscaleConv(row) for row in col])
        return grayscaled_image

    @staticmethod
    def weightedAverageGrayscaleConv(pixel):
        return np.mean(np.array(pixel))
