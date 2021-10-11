# Backgrounds.py
# Class to store information related to random background images.

import os
import pickle
import random
import matplotlib.pyplot as plt
# import pdb


class Backgrounds():
    def __init__(self, filename=os.path.join("data", "backgrounds.pck")):
        self._images = pickle.load(open(filename, 'rb'))
        self._numimages = len(self._images)
        print("Number of images loaded :", self._numimages)

    def getrandom(self, show=False):
        bg = self._images[random.randint(0, self._numimages-1)]
        if show: plt.imshow(bg)
        return bg


if __name__ == "__main__":
    backgrounds = Backgrounds()
    _ = backgrounds.getrandom(show=True)
    plt.waitforbuttonpress()