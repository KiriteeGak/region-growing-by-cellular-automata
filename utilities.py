class preprocessingImage(object):
	def rgbToGrayscaleConversion(self, image_array):
		grayscaled_image = []
		for col in image_array:
			grayscaled_image.append([self.weightedAverageGrayscaleConv(row) for row in col])
		return grayscaled_image

	def weightedAverageGrayscaleConv(self, pixel):
		return int(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])