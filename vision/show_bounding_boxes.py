# show_bounding_boxes.py 
# Look at current bounding boxes for training data.

import cv2
import matplotlib.pyplot as plt
import os
import random
from glob import glob
from params import *
from display import display

DATADIR = "data/extracted"


def main():
    '''Test the hardcoded bounding box on a randomly chosen image.'''
    filenames = glob(os.path.join(DATADIR, '*.jpg'))
    filename = random.choice(filenames)
    filename = os.path.join(DATADIR, '4D.jpg')
    display(cv2.imread(filename, cv2.IMREAD_UNCHANGED), polygons = [refCornerHL, refCornerLR])
    plt.waitforbuttonpress()


if __name__ == "__main__":
    main()