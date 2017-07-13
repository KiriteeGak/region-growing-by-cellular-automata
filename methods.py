import numpy as np
import datetime
from scipy.misc import *


class RegionGrowing(object):
    def regionGrowing(self, image_array, seed_point_path, cutOffThreshold, iterations):
        seed_point = self.seedPoints(seed_point_path)
        image_array_padded = self.padImages(image_array)
        size = np.shape(image_array)
        actual_weights_image = np.zeros(size)
        temp_actual_weights_image = np.zeros((size[0] + 2, size[1] + 2))
        for seed in seed_point:
            actual_weights_image[seed[0], seed[1]] = 1
            temp_actual_weights_image[size[0] + 1, size[1] + 1] = 1
        actual_weights_image = np.array(actual_weights_image)
        for it in range(0, iterations):
            for r in range(0, size[0]):
                for c in range(0, size[1]):
                    if actual_weights_image[r, c] > 0:
                        temp_actual_weights_image = self.neighborhoodWeighting([r, c], image_array_padded,
                                                                               actual_weights_image,
                                                                               temp_actual_weights_image,
                                                                               cutOffThreshold)
            actual_weights_image = temp_actual_weights_image[1:size[0] + 1, 1:size[1] + 1]
        self.saveImage(self.makeBinaryImage(actual_weights_image))

    @staticmethod
    def seedPoints(filepath):
        fid = open(filepath, 'rb')
        return [list(map(lambda x: int(x.replace(' ', '')), line.strip().split(','))) for line in fid]

    @staticmethod
    def strengthCal(dat1, dat2, strength, threshold=0.5):
        if strength > threshold:
            return strength * (1 - (abs(dat1 - dat2) / max(dat1, dat2)))
        return 0

    def neighborhoodWeighting(self, coord, real_image_padded, dummy_image, temp_dummy_image, threshold):
        [c_1, c_2] = coord
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if [i, j] != [1, 1]:
                    str_ob = self.strengthCal(real_image_padded[c_1 + 1, c_2 + 1],
                                              real_image_padded[c_1 + 1 + i, c_2 + 1 + j], dummy_image[c_1, c_2],
                                              threshold)
                    temp_dummy_image[c_1 + i + 1, c_2 + j + 1] = max(dummy_image[c_1 + i, c_2 + j], str_ob)
        return temp_dummy_image

    @staticmethod
    def padImages(image_array):
        size = np.shape(image_array)
        padded_matrix = np.zeros((size[0] + 2, size[1] + 2))
        padded_matrix[1:size[0] + 1, 1:size[1] + 1] = np.array(image_array)
        return padded_matrix

    @staticmethod
    def makeBinaryImage(actual_weights_image):
        size = np.shape(actual_weights_image)
        grown_image = np.zeros(size)
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                if actual_weights_image[i, j] > 0:
                    grown_image[i, j] = 255
                else:
                    grown_image[i, j] = 0
        return grown_image

    @staticmethod
    def saveImage(image_array):
        name = str(datetime.datetime.now()).replace(" ", "_")
        imsave("output/" + name + ".jpg", image_array)
