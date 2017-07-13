import argparse
import numpy as np
from scipy import ndimage
from utilities import PreprocessingImage
from methods import RegionGrowing

parser = argparse.ArgumentParser(prog='rgca', description='Arguments for Region growing based segmentation')
parser.add_argument('pathToImageFile', metavar='ImagePath', type=str, help='Path for the image file')
parser.add_argument('pathToSeeds', metavar='SeedsList', type=str, help='File with seeds')
parser.add_argument('-t', '--cutoffThreshold', metavar='th', nargs='?', type=float, default=0.5,
                    help='Cutoff strength at which growing stops')
parser.add_argument('-i', '--iterations', metavar='i', nargs='?', type=int, default=50,
                    help='Number of iterations used for growing')
args = parser.parse_args()

image_array = ndimage.imread(args.pathToImageFile)
if len(np.shape(image_array)) > 2:
    image_array = PreprocessingImage().rgbToGrayscaleConversion(image_array)

RegionGrowing().regionGrowing(image_array, args.pathToSeeds, args.cutoffThreshold, args.iterations)
