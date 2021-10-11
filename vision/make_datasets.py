# make_datasets.py 
# Generate datasets for training and validation using randomly generated scenes of cards.

import os
from tqdm import tqdm
from Backgrounds import Backgrounds
from Cards import Cards
from generate_scene import *

DATADIR = "data/scenes/val"  # where to save the files
NUMBER = 500  # number of images to generate
CARDS = 3  # 2 or 3 cards in each image

def main():
    # Make output directory, if needed
    if not os.path.isdir(DATADIR):
        os.makedirs(DATADIR)

    if CARDS not in [2, 3]:
        print(f'ERROR: Unrecognized value for CARDS ({CARDS})')
        return -1

    # Get backgrounds and cards
    backgrounds = Backgrounds()
    cards = Cards()

    # Generate and save scenes, using progress bar
    for i in tqdm(range(NUMBER)):
        bg = backgrounds.getrandom()
        
        if CARDS == 2:
            img1, card_val1, hulla1, hullb1 = cards.getrandom()
            img2, card_val2, hulla2, hullb2 = cards.getrandom()
            scene = Scene(bg,
                img1, card_val1, hulla1, hullb1,
                img2, card_val2, hulla2, hullb2)
        elif CARDS == 3:
            img1, card_val1, hulla1, hullb1 = cards.getrandom()
            img2, card_val2, hulla2, hullb2 = cards.getrandom()
            img3, card_val3, hulla3, hullb3 = cards.getrandom()
            scene = Scene(bg,
                img1, card_val1, hulla1, hullb1,
                img2, card_val2, hulla2, hullb2,
                img3, card_val3, hulla3, hullb3)

        scene.writefiles(DATADIR)

if __name__ == "__main__":
    main()