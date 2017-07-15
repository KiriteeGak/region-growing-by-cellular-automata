import numpy as np
import datetime
from scipy.misc import *
import time

class RegionGrowing(object):
    def regionGrowing(self, image_array, seed_point_path, cutoff_threshold, iterations):
        times = []
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
            st = time.time()
            for r in range(0, size[0]):
                for c in range(0, size[1]):
                    if actual_weights_image[r, c] > 0:
                        temp_actual_weights_image = self.neighborhoodWeighting([r, c], image_array_padded,
                                                                               actual_weights_image,
                                                                               temp_actual_weights_image,
                                                                               cutoff_threshold)
            actual_weights_image = temp_actual_weights_image[1:size[0] + 1, 1:size[1] + 1]
            times.append(time.time()-st)
        print times, np.mean(timesn)
        self.saveImage(self.makeBinaryImage(actual_weights_image))

    def regionGrowingUpdated(self, image_array, seed_point, cutoff_threshold, iterations):
        coordinate_strength_array = {}
        for seed in seed_point:
            coordinate_strength_array[str(seed[0])+"_"+str(seed[1])] = 1
        image_dict = {str(i)+"_"+str(j):pixel_val for i,each_row in enumerate(image_array) for j,pixel_val in enumerate(each_row)}
        for it in range(0, iterations):
            temp_coordinate_strength_array = coordinate_strength_array.copy()
            for seed, strength in temp_coordinate_strength_array.iteritems():
                coordinate_strength_array = self.neighborhoodWeightingUpdated(map(lambda a: int(a), seed.split('_')),
                 coordinate_strength_array, 0.5, (5,5))
            print coordinate_strength_array

    def neighborhoodWeightingUpdated(self, coord, coordinate_strength_array, threshold, canvas_size):
        [c_1, c_2] = coord
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if [i, j] != [1, 1] and 0<=c_1+i<canvas_size[0] and 0<=c_2+j<canvas_size[1]:
                    if str(c_1)+"_"+str(c_2) in coordinate_strength_array:
                        curr_cell_strength = coordinate_strength_array[str(c_1)+"_"+str(c_2)]
                    else:
                        curr_cell_strength = 0
                    neighboring_cell_strength = coordinate_strength_array[str(c_1+i)+"_"+str(c_2+j)]
                    str_ob = self.strengthCal(curr_cell_strength,neighboring_cell_strength,threshold)
                    coordinate_strength_array[str(c_1+i)+"_"+str(c_2+j)] = max(neighboring_cell_strength, str_ob)
        return coordinate_strength_array


    @staticmethod
    def seedPoints(filepath):
        fid = open(filepath, 'rb')
        return [list(map(lambda x: int(x.replace(' ', '')), line.strip().split(','))) for line in fid]

    @staticmethod
    def strengthCal(dat1, dat2, strength, threshold=0.5):
        print strength, threshold
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


if __name__ == '__main__':
    image_array = np.random.rand(5,5)
    RegionGrowing().regionGrowingUpdated(image_array, [[1,0],[3,3]], 0.5, 10)