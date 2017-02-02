import numpy as np
import datetime
from scipy.misc import *
from utilities import preprocessingImage as ppi

class RegionGrowing(object):
	def regionGrowing(self, image_array, seed_point, threshold = 0.5, iterations = 120):
		'''
			Description : Main function caller
			image_array : type : nd-array of an image
			seed_point : type : list, List of coordinates
			threshold : type : float, the threshold for stopping iterations
			iterations : type: int, number of iterations for region growing
		'''
		image_array_padded = self.padImages(image_array)
		size = np.shape(image_array)
		actual_weights_image = np.zeros(size)
		temp_actual_weights_image = np.zeros((size[0]+2,size[1]+2))
		for seed in seed_point:
			actual_weights_image[seed[0], seed[1]] = 1
			temp_actual_weights_image[size[0]+1,size[1]+1] = 1
		actual_weights_image = np.array(actual_weights_image)
		for it in range(0,iterations):
			for r in range(0,size[0]):
				for c in range(0,size[1]):
					if actual_weights_image[r,c] > 0:
						temp_actual_weights_image = self.neighborhoodWeighting([r,c], image_array_padded, actual_weights_image, temp_actual_weights_image)
			actual_weights_image = temp_actual_weights_image[1:size[0]+1,1:size[1]+1]
		self.saveImage(self.makeBinaryImage(actual_weights_image))			

	def strengthCal(self, dat1, dat2, stre, threshold=0.5):
		'''
			Calculates strength of a pixel from the parent pixel based on grayscale difference
		'''
		if stre > threshold:
			return stre*(1-(abs(dat1-dat2)/max(dat1,dat2)))
		return 0

	def neighborhoodWeighting(self, coord, real_image_padded, dummy_image, temp_dummy_image):
		'''
			Function for calculating weights for whole neighborhood 3x3
			coord : type : array, parent coordinate
			real_image_padded : Zero padded grayscale image  
			dummy_image : Image with size of image_array with default values as zeros except at parent coordinates
			temp_dummy_image : temporary weight storage for substitution after iterations
		'''
		[c_1,c_2] = coord
		for i in range(-1,2,1):
			for j in range(-1,2,1):
				if [i,j] != [1,1]:
					str_ob = self.strengthCal(real_image_padded[c_1+1,c_2+1],real_image_padded[c_1+1+i,c_2+1+j],dummy_image[c_1,c_2])
					temp_dummy_image[c_1+i+1,c_2+j+1] = max(dummy_image[c_1+i,c_2+j],str_ob)
		return temp_dummy_image

	def padImages(self, image_array):
		'''
			Function for padding images
			image_array : Grayscaled_image numpy array
		'''
		size = np.shape(image_array)
		padded_matrix = np.zeros((size[0]+2,size[1]+2))
		padded_matrix[1:size[0]+1,1:size[1]+1] = np.array(image_array)
		return padded_matrix

	def makeBinaryImage(self, actual_weights_image):
		'''
			Produces output binary image from the final weighted image
		'''
		size = np.shape(actual_weights_image)
		grown_image = np.zeros(size)
		for i in range(0,size[0]):
			for j in range(0,size[1]):
				if actual_weights_image[i,j] > 0:
					grown_image[i,j] = 255
				else:
					grown_image[i,j] = 0
		return grown_image

	def saveImage(self, image_array):
		name = str(datetime.datetime.now()).replace(" ","_")
		imsave("output/"+ name+".jpg", image_array)