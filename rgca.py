import argparse, os
from scipy import ndimage
from src.utilities import *
from src.methods import RegionGrowing

parser = argparse.ArgumentParser(prog='rgca', description='Arguments for Region growing based segmentation')
parser.add_argument('pathToImageFile', metavar='ImagePath', type=str, help='Path for the image file')
parser.add_argument('pathToSeeds', metavar='SeedsList', type=str, help='File with seeds')
parser.add_argument('-t', '--cutoffThreshold', metavar='th', nargs='?', type=float, default=0.5,
                    help='Cutoff strength at which growing stops')
parser.add_argument('-i', '--iterations', metavar='i', nargs='?', type=int, default=50,
                    help='Number of iterations used for growing')
args = parser.parse_args()

if os.path.isfile(args.pathToImageFile):
    image_array = ndimage.imread(args.pathToImageFile)
    if len(np.shape(image_array)) > 2:
        image_array = rgb_to_gray_scale_conversion(image_array)
    RegionGrowing().region_growing(image_array, args.pathToSeeds, args.cutoffThreshold, args.iterations)
else:
    raise Exception("File not found in the path provided.")
