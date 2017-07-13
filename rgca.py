import argparse
import numpy as np
from scipy import ndimage
from utilities import preprocessingImage as ppi
from methods import RegionGrowing as rg

parser = argparse.ArgumentParser(prog='regiongrowingca', description='Arguments for region growing')
parser.add_argument('imagepath', metavar='ImagePath', type=str, help='Image path for segmentation')
parser.add_argument('seedlistpath', metavar='SeedsList', type=str, help='File with seeds')
parser.add_argument('-t', '--cutoffThreshold', metavar='th', nargs='?', type=float, default=0.5, help='Strength cutoff')
parser.add_argument('-i', '--iterations', metavar='i', nargs='?', type=int, default=50, help='No.of iterations')
args = parser.parse_args()

image_array = ndimage.imread(args.imagepath)
if len(np.shape(image_array)) > 2:
    image_array = ppi().rgbToGrayscaleConversion(image_array)

rg.regionGrowing(image_array, args.seedlistpath, args.cutoffThreshold, args.iterations)
