# extract_all_cards.py 
# Parse a directory of images, extracting individual cards from each image, 
# and saving the extracted version to a new directory.

import numpy as np
import cv2
import os
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from glob import glob
from params import *  # contains required params
import pdb

INPUTDIR = "data/cards"
OUTPUTDIR = "data/extracted"
FILENAME = "3D.jpg"  # sample image file from which to extract a card
DEBUG = False
REPEAT = False  # if False, do *not* process files with a corresponding file in the OUTPUTDIR

def main():
    # Check input and output directories
    if not os.path.isdir(INPUTDIR):
        print(f"ERROR: Input directory not found ({INPUTDIR})")
        return -1
    if not os.path.isdir(OUTPUTDIR):
        os.makedirs(OUTPUTDIR)

    # Extract image files from input directory
    fullfiles = glob(os.path.join(INPUTDIR, '*.jpg'))
    outfiles = glob(os.path.join(OUTPUTDIR, '*.jpg'))
    if not REPEAT:
        fullfiles = removeduplicates(fullfiles, outfiles)
    if len(fullfiles) == 0:
        print(f'ERROR: No image files found that need processing in ({INPUTDIR}). Check REPEAT parameter.')
        return -1
    # filenames = [f.split('\\')[-1] for f in fullfiles]
    # print(*fullfiles, sep='\n')
    # print(*filenames, sep='\n')

    # Process each file separately
    n = len(fullfiles)
    for i in range(n):
        file = fullfiles[i]
        print(f'Processing file {i + 1} of {n}: {file}')
        img = cv2.imread(file)
        valid, card = extract(img, debug=DEBUG)
        # print(f'Card found? {valid}')
        # print(f'Card data: {card}')
        if valid:
            plt.figure(1)
            plt.imshow(cv2.cvtColor(card,cv2.COLOR_BGR2RGB))
            plt.pause(0.5)
            cv2.imwrite(os.path.join(OUTPUTDIR, file.split('\\')[-1]), card)
        else:
            print(f'\tCard not found!!!')

        if DEBUG:
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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

def removeduplicates(infiles, outfiles):
    '''Helper function to remove files in INFILES that already exist in OUTFILES.'''
    outfiles = [f.split('\\')[-1] for f in outfiles]
    s = set(outfiles)
    newfiles = [f for f in infiles if f.split('\\')[-1] not in s]
    return newfiles

def varianceOfLaplacian(img):
    """ Compute the Laplacian of the image and then return the focus measure, 
        which is simply the variance of the Laplacian.
        Source: A.Rosebrock, https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
    """
    return cv2.Laplacian(img, cv2.CV_64F).var()

if __name__ == "__main__":
    main()
