# Cards.py
# Class to store card information, loaded from pickle file.

import os
import pickle
import random
import matplotlib.pyplot as plt
from display import display
# import pdb


class Cards():
    def __init__(self, filename=os.path.join("data", "cards.pck")):
        self._cards = pickle.load(open(filename, 'rb'))
        # self._cards is a dictionary where keys are name names (ex:'KC') and values are lists of (img, hullHL, hullLR) 
        self._num_cards_by_value = {k: len(self._cards[k]) for k in self._cards}
        print("Number of cards loaded per name:", self._num_cards_by_value)
        
    def getrandom(self, name=None, show=False):
        if name is None:
            name = random.choice(list(self._cards.keys()))
        card, hull1, hull2 = self._cards[name][random.randint(0, self._num_cards_by_value[name]-1)]
        if show:
            display(card, [hull1, hull2], "rgb")
        return card, name, hull1, hull2


if __name__ == "__main__":
    cards = Cards()
    _ = cards.getrandom(show=True)
    # _ = cards.getrandom('7H', show=True)
    plt.waitforbuttonpress()