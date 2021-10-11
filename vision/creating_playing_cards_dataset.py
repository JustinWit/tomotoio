# creating_playing_cards_dataset
# Script to generate a training dataset of playing cards. For training YOLO neural network.

import numpy as np
import cv2
import os
from tqdm import tqdm
import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import pickle
from glob import glob 
import imgaug as ia
from imgaug import augmenters as iaa
from shapely.geometry import Polygon
from params import *
import pdb

DATADIR = "data"  # directory that will contain all kinds of data (the data we download and the data we generate)
SUITS = ['C', 'D', 'S', 'H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DEBUG = False

# Pickle files
backgrounds_pck_fn = os.path.join(DATADIR, "backgrounds.pck")  # background images from the DTD
cards_pck_fn = os.path.join(DATADIR, "cards.pck")  # card images

# Dimensions of the generated dataset images (in pixels)
imgW = 720
imgH = 720


def main():
    # Make data directory, if needed
    if not os.path.isdir(DATADIR):
        os.makedirs(DATADIR)

    plt.figure(figsize=(10, 10))
    plt.imshow(alphamask)
    plt.pause(1)



def display(img, polygons=[], channels="bgr", size=9):
    """ Display an inline image, and draw optional polygons (bounding boxes, convex hulls) on it.
        Use the param 'channels' to specify the order of the channels ("bgr" for an image coming from OpenCV world)
    """  
    # Show image
    if channels == "bgr":
        numchannels = img.shape[2]
        if numchannels == 4:
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    _, ax = plt.subplots(figsize=(size, size))
    ax.set_facecolor((0, 0, 0))
    ax.imshow(img)

    # Add polygons to image, if requested
    if not isinstance(polygons, list):
        polygons = [polygons]  
    for polygon in polygons:
        # A polygon has either shape (n,2) or (n,1,2) if it is a cv2 contour (like convex hull). In the latter case, reshape to (n,2)
        if len(polygon.shape) == 3:
            polygon = polygon.reshape(-1, 2)
        patch = patches.Polygon(polygon, linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(patch)

def give_me_filename(dirname, suffixes, prefix=""):
    """ Return a new filename or a list of new filenames in directory 'dirname'
        If 'suffixes' is a list, one filename per suffix in 'suffixes':
        filename = dirname + "/" + prefix + random number + "." + suffix
        Same random number for all the file name
        Ex: 
        > give_me_filename("dir", "jpg", prefix="prefix")
        'dir/prefix408290659.jpg'
        > give_me_filename("dir", ["jpg", "xml"])
        ['dir/877739594.jpg', 'dir/877739594.xml']        
    """
    if not isinstance(suffixes, list):
        suffixes = [suffixes]
    suffixes = [p if p[0] == '.' else '.' + p for p in suffixes]
          
    while True:
        bname = "%09d"%random.randint(0, 999999999)
        fnames = []
        for suffix in suffixes:
            fname = os.path.join(dirname, prefix + bname + suffix)
            if not os.path.isfile(fname):
                fnames.append(fname)                
        if len(fnames) == len(suffixes): break
    
    if len(fnames) == 1:
        return fnames[0]
    else:
        return fnames

def varianceOfLaplacian(img):
    """ Compute the Laplacian of the image and then return the focus measure, 
        which is simply the variance of the Laplacian.
        Source: A.Rosebrock, https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
    """
    return cv2.Laplacian(img, cv2.CV_64F).var()

def extract(img, output_fn=None, min_focus=120, debug=False):
    """Extract a playing card from an image."""
    imgwarp = None
    
    # Check the image is not too blurry
    focus = varianceOfLaplacian(img)
    if debug: print(f'Focus: {focus} (threshold is {min_focus})')
    # if focus < min_focus:
    #     if debug: print("Focus too low :", focus)
    #     return False, None
    
    # Convert in gray color
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise-reducing and edge-preserving filter
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    
    # Edge extraction
    edge = cv2.Canny(gray, 30, 200)

    # Find the contours in the edged image
    cnts, hierarchy = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # We suppose that the contour with largest area corresponds to the contour delimiting the card
    cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    # Show largest contour
    # cv2.namedWindow("contours")
    # contours = img.copy()
    # cv2.drawContours(contours, [cnt], 0, (0, 0, 255), 2, cv2.LINE_8, hierarchy, 0)
    # cv2.imshow("contours", contours)
    # cv2.imshow("new", img)
    
    # We want to check that the contour is a rectangular shape
    # First, determine 'box', the minimum area bounding rectangle of 'cnt'
    # Then compare area of 'cnt' and area of 'box'
    # Both areas sould be very close
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    areaCnt = cv2.contourArea(cnt)
    areaBox = cv2.contourArea(box)
    valid = areaCnt / areaBox > 0.9
    
    if valid:
        # We want transform the zone inside the contour into the reference rectangle of dimensions (cardW,cardH)
        ((xr, yr), (wr, hr), thetar) = rect
        # Determine 'Mp' the transformation that transforms 'box' into the reference rectangle
        if wr > hr:
            Mp = cv2.getPerspectiveTransform(np.float32(box), refCard)
        else:
            Mp = cv2.getPerspectiveTransform(np.float32(box), refCardRot)
        # Determine the warped image by applying the transformation to the image
        imgwarp = cv2.warpPerspective(img, Mp, (cardW, cardH))
        # Add alpha layer
        imgwarp = cv2.cvtColor(imgwarp, cv2.COLOR_BGR2BGRA)
        
        # Shape of 'cnt' is (n,1,2), type=int with n = number of points
        # We reshape into (1,n,2), type=float32, before feeding to perspectiveTransform
        cnta = cnt.reshape(1, -1, 2).astype(np.float32)
        # Apply the transformation 'Mp' to the contour
        cntwarp = cv2.perspectiveTransform(cnta, Mp)
        cntwarp = cntwarp.astype(np.int32)
        
        # We build the alpha channel so that we have transparency on the
        # external border of the card
        # First, initialize alpha channel fully transparent
        alphachannel = np.zeros(imgwarp.shape[:2], dtype=np.uint8)
        # Then fill in the contour to make opaque this zone of the card 
        cv2.drawContours(alphachannel, cntwarp, 0, 255, -1)
        
        # Apply the alphamask onto the alpha channel to clean it
        alphachannel = cv2.bitwise_and(alphachannel, alphamask)
        
        # Add the alphachannel to the warped image
        imgwarp[:,:,3] = alphachannel
        
        # Save the image to file
        if output_fn is not None:
            cv2.imwrite(output_fn, imgwarp)
        
    if debug:
        cv2.imshow("Gray",gray)
        cv2.imshow("Canny",edge)
        edge_bgr = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(edge_bgr, [box], 0, (0, 0, 255), 3)
        cv2.drawContours(edge_bgr, [cnt], 0, (0, 255, 0), -1)
        cv2.imshow("Contour with biggest area", edge_bgr)
        if valid:
            cv2.imshow("Alphachannel", alphachannel)
            cv2.imshow("Extracted card", imgwarp)

    return valid, imgwarp

if __name__ == "__main__":
    main()
