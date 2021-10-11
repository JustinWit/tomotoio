# pickle_dtd.py 
# Load JPGs from Describable Textures Dataset (DTD) subdirectories and save them in a pickle file.
# https://www.robots.ox.ac.uk/~vgg/data/dtd/
#
# Download and extract DTD first:
# $ wget https://www.robots.ox.ac.uk/~vgg/data/dtd/download/dtd-r1.0.1.tar.gz
# $ tar xf dtd-r1.0.1.tar.gz
#
# After running this script, you can remove the DTD directory if desired
# $ rm -r dtd
# $ rm dtd-r1.0.1.tar.gz

from glob import glob
import matplotlib.image as mpimg
import pickle

DATADIR = "data"  # directory that will contain all kinds of data (the data we download and the data we generate)
DTDDIR = "C:/Users/meicholtz/Downloads/dtd/images/"
FILENAME = DATADIR + "/backgrounds.pck"  # pickle FILENAME for DTD background images


def main():
    # Extract images
    imgs = []  # list of background images
    for subdir in glob(DTDDIR + "/*"):
        for f in glob(subdir + "/*.jpg"):
            imgs.append(mpimg.imread(f))

    # Dump via pickle
    pickle.dump(imgs, open(FILENAME, 'wb'))

    # Display results
    print(f"Number of images loaded: {len(imgs)}")
    print(f"Saved in: {FILENAME}")

if __name__ == "__main__":
    main()