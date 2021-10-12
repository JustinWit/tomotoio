# generate_train_colab.py
# Generate train.txt file for Google Colab

import os
from glob import glob

DATADIR = "data/scenes/val"
FILENAME = "test.txt"  # output file


def main():
    filenames = glob(os.path.join(DATADIR, '*.jpg'))
    newfilenames = ['data/cards/' + f.split('\\')[-1] for f in filenames]
    print(*newfilenames, sep='\n')
    with open(FILENAME, "w") as outfile:
        for f in newfilenames:
            outfile.write(f)
            outfile.write("\n")
        outfile.close()


if __name__ == "__main__":
    main()