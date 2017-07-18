import numpy as np
import datetime
from scipy.misc import *


class RegionGrowing:
    def region_growing(self, image_array, file_path, cutoff_threshold, iterations):
        """
        :param image_array:
        :param file_path:
        :param cutoff_threshold:
        :param iterations:
        :return:
        """
        size = np.shape(image_array)
        image_array_map = {str(r) + "_" + str(c): pixel for r, each_row in enumerate(image_array) for c, pixel in
                           enumerate(each_row)}
        seeds_map = {str(r) + "_" + str(c): 1 for (r, c) in self._seed_points(file_path)}
        for it in range(0, iterations):
            _update_seeds_map = seeds_map.copy()
            for pixel_coord, strength in seeds_map.iteritems():
                [r, c] = map(lambda a: int(a), pixel_coord.split('_'))
                _temp_weights_neighbors_pixel = self._neighborhood_weighting([r, c], image_array_map,
                                                                             seeds_map, cutoff_threshold, size)
                _update_seeds_map = self._update_weights(_temp_weights_neighbors_pixel, _update_seeds_map)
            seeds_map = _update_seeds_map
        self._save_image(self._make_binary_image(np.shape(image_array), seeds_map))

    @staticmethod
    def _seed_points(file_path):
        """
        :param file_path:
        :return:
        """
        fid = open(file_path, 'rb')
        return [list(map(lambda x: int(x.replace(' ', '')), line.strip().split(','))) for line in fid]

    @staticmethod
    def _update_weights(_temp_weights_neighbors_pixel, _update_seeds_map):
        """
        :param _temp_weights_neighbors_pixel:
        :param _update_seeds_map:
        :return:
        """
        for pixel_address, strength in _temp_weights_neighbors_pixel.iteritems():
            if pixel_address not in _update_seeds_map:
                _update_seeds_map[pixel_address] = strength
            elif pixel_address in _update_seeds_map and _update_seeds_map[pixel_address] < strength:
                _update_seeds_map[pixel_address] = strength
            else:
                pass
        return _update_seeds_map

    def _neighborhood_weighting(self, coord, image_map, seeds_map, threshold, canvas_size):
        """
        :param coord:
        :param image_map:
        :param seeds_map:
        :param threshold:
        :param canvas_size:
        :return:
        """
        [[r, c], [max_r, max_c]] = [coord, canvas_size]
        _temp_weights = {}
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                pixel_key = str(r) + "_" + str(c)
                if [i, j] != [0, 0] and 0 <= r + i < max_r and 0 <= c + j < max_c:
                    if pixel_key in seeds_map:
                        trans_strength = self._calculate_strength(image_map[pixel_key],
                                                                  image_map[str(r + i) + "_" + str(c + j)],
                                                                  seeds_map[pixel_key], threshold)
                    else:
                        trans_strength = self._calculate_strength(image_map[pixel_key],
                                                                  image_map[str(r + i) + "_" + str(c + j)], 0,
                                                                  threshold)
                    if trans_strength != 0:
                        _temp_weights[str(r + i) + "_" + str(c + j)] = trans_strength
        return _temp_weights

    @staticmethod
    def _calculate_strength(dat1, dat2, strength, threshold):
        """
        :param dat1:
        :param dat2:
        :param strength:
        :param threshold:
        :return:
        """
        if dat1 != 0 or dat2 != 0:
            strength_trans = strength * (1 - (abs(dat1 - dat2) / max(dat1, dat2)))
            if strength_trans >= threshold:
                return strength_trans
        return 0

    @staticmethod
    def _make_binary_image(size, image_map):
        """
        :param size:
        :param image_map:
        :return:
        """
        grown_image = np.zeros(size)
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                image_add = str(i) + "_" + str(j)
                if image_add in image_map and image_map[image_add] > 0:
                    grown_image[i, j] = 255
                else:
                    grown_image[i, j] = 0
        return grown_image

    @staticmethod
    def _save_image(image_array):
        """
        :param image_array:
        :return:
        """
        name = str(datetime.datetime.now()).replace(" ", "_")
        imsave("examples/output/" + name + ".jpg", image_array)
