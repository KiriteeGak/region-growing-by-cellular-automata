import numpy as np
class preprocessingImage(object):
	def rgbToGrayscaleConversion(self, image_array):
		grayscaled_image = []
		for col in image_array:
			grayscaled_image.append([self.weightedAverageGrayscaleConv(row) for row in col])
		return grayscaled_image

	def weightedAverageGrayscaleConv(self, pixel):
		return np.mean(np.array(pixel))