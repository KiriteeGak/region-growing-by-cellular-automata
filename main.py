import sys, argparse, ast
import numpy as np
from scipy import misc, ndimage
from utilities import preprocessingImage as ppi
from methods import RegionGrowing as RG
(image_file_path, seeds) = (sys.argv[1],sys.argv[2])
seeds = ast.literal_eval(seeds)
image_array = ndimage.imread(image_file_path)
if len(np.shape(image_array)) > 2:
	image_array = ppi().rgbToGrayscaleConversion(image_array)
RG().regionGrowing(image_array,seeds)