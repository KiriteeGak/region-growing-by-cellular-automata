import numpy as np
import datetime
from scipy.misc import *
import time

class RegionGrowing():
    def regionGrowing(self,image_array,seeds,cutoff_threshold,iterations):
        print __name__
        size = np.shape(image_array)
        image_array_map = {str(r)+"_"+str(c):pixel for r,each_row in enumerate(image_array) for c,pixel in enumerate(each_row)}
        seeds_map = {str(r)+"_"+str(c):1 for (r,c) in seeds}
        for it in range(0,iterations):
            _update_seeds_map = seeds_map.copy()
            for pixel_coord,strength in seeds_map.iteritems():
                [r,c] = map(lambda a:int(a),pixel_coord.split('_'))
                _temp_weights_neighbors_pixel = self.neighborhoodWeighting([r,c],image_array_map,
                    seeds_map,cutoff_threshold, size)
                _update_seeds_map = self._updateWeights(_temp_weights_neighbors_pixel, _update_seeds_map)
            seeds_map = _update_seeds_map
        self.saveImage(self.makeBinaryImage(np.shape(image_array), seeds_map))

    @staticmethod
    def seedPoints(filepath):
        fid = open(filepath, 'rb')
        return [list(map(lambda x: int(x.replace(' ', '')), line.strip().split(','))) for line in fid]

    def _updateWeights(self, _temp_weights_neighbors_pixel, _update_seeds_map):
        for pixel_address, strength in _temp_weights_neighbors_pixel.iteritems():
            if pixel_address not in _update_seeds_map:
                _update_seeds_map[pixel_address] = strength
            elif pixel_address in _update_seeds_map and _update_seeds_map[pixel_address] < strength:
                _update_seeds_map[pixel_address] = strength
            else:
                pass
        return _update_seeds_map

    def neighborhoodWeighting(self,coord,image_map,seeds_map,threshold,canvas_size):
        [[r,c],[max_r,max_c]] = [coord,canvas_size]
        _temp_weights = {}
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                pixel_key = str(r)+"_"+str(c)
                if [i,j] != [1,1] and 0<=r+i<max_r and 0<=c+j<max_c:
                    if pixel_key in seeds_map:
                        trans_strength = self.strengthCal(image_map[pixel_key],image_map[str(r+i)+"_"+str(c+j)],seeds_map[pixel_key],threshold)
                    else:
                        trans_strength = self.strengthCal(image_map[pixel_key],image_map[str(r+i)+"_"+str(c+j)],0,threshold)
                    if trans_strength != 0:
                        _temp_weights[str(r+i)+"_"+str(c+j)] = trans_strength
        return _temp_weights

    @staticmethod
    def strengthCal(dat1,dat2,strength,threshold):
        strength_trans = strength * (1-(abs(dat1-dat2) / max(dat1,dat2)))
        if strength_trans >= threshold:
            return strength_trans
        return 0

    @staticmethod
    def makeBinaryImage(size,image_map):
        grown_image = np.zeros(size)
        for i in range(0,size[0]):
            for j in range(0,size[1]):
                image_add = str(i)+"_"+str(j)
                if image_add in image_map and image_map[image_add] > 0:
                    grown_image[i,j] = 255
                else:
                    grown_image[i,j] = 0
        return grown_image

    @staticmethod
    def saveImage(image_array):
        name = str(datetime.datetime.now()).replace(" ","_")
        imsave("output/"+name+".jpg",image_array)

if __name__ == '__main__':
    image_array = np.random.rand(100,100)
    seeds = [[30,30],[90,90]]
    RegionGrowing().regionGrowing(image_array,seeds,0.5,50)