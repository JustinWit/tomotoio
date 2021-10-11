# pickle_convexhulls.py
# Compute the convex hulls for a directory of images, and save the corresponding information
# via pickle.

import cv2
import os
from glob import glob
import pickle
from params import *
from convexhull import convexhull

DATADIR = "data/extracted"
SUITS = ['C', 'D', 'S', 'H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
OUTFILE = os.path.join("data", "cards.pck")  # output pickle file

def main():
    cards = {}  # initialize dictionary to store card information
    for suit in SUITS:
        for value in VALUES:
            card = value + suit
            print(f'Processing card {card}')

            cards[card] = []
            filename = os.path.join(DATADIR, card + ".jpg")
            img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

            # Find convexhull in upper-left corner
            hullHL = convexhull(img, refCornerHL, debug=False) 
            if hullHL is None: 
                print(f"File {filename} not used.")
                continue

            # Find convex hull in lower-right corner
            hullLR = convexhull(img, refCornerLR, debug=False) 
            if hullLR is None: 
                print(f"File {filename} not used.")
                continue

            # Store image in "rgb" format (we don't need opencv anymore)
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGBA)
            cards[card].append((img, hullHL, hullLR))

    print(f"Saving data to file:", OUTFILE)
    pickle.dump(cards, open(OUTFILE,'wb'))

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()