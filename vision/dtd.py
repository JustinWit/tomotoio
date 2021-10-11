# dtd.py
# Helper class for background images from the Describable Textures Dataset (DTD).
# https://www.robots.ox.ac.uk/~vgg/data/dtd/

import pickle
import random
import matplotlib.pyplot as plt


class Backgrounds():
    def __init__(self, filename="data/backgrounds.pck"):
        self._images = pickle.load(open(filename,'rb'))
        self._numimages = len(self._images)
        print(f"Number of images loaded: {self._numimages}")

    def getrandom(self, display=False):
        '''Get a random image from the list of images.'''
        bg = self._images[random.randint(0, self._numimages - 1)]
        if display:
            plt.imshow(bg)
            plt.pause(1)
        return bg

def main():
    backgrounds = Backgrounds()
    _ = backgrounds.getrandom(display=True)

if __name__ == "__main__":
    main()