# convert_voc_yolo.py
# Convert dataset annotations from VOC format to YOLO format.
#
# YOLO cannot directly exploit the Pascal VOC annotations files.
# You need to convert the xml files in txt files accordingly to the syntax explained here: 
# https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
# This script makes this conversion and also generates the txt file that contains all the
# images of the dataset.

import xml.etree.ElementTree as ET
import os
import sys
from glob import glob


def main():
    # Parse inputs
    if len(sys.argv) !=  4:
        print("ERROR: This script requires 3 inputs to run.")
        print(f"\tUsage: {sys.argv[0]} datadir classnames.txt list.txt")
        print(f"\tEx: {sys.argv[0]} data/scenes/train data/cardnames.txt data/train.txt")
        print("\tFrom xml files in datadir, convert to txt files with annotation information and build list.txt file")
        sys.exit(1)
    datadir = sys.argv[1]  # directory containing all images and corresponding XML files
    classfile = sys.argv[2]  # file containing class name (e.g. 2C, 3C, ..., AH)
    listfile = sys.argv[3]  # output file containing the list of all image files

    # Check that input files and directories exist
    if not os.path.isdir(datadir):
        print(f"ERROR: {datadir} is not a directory")
        sys.exit(1)
    if not os.path.isfile(classfile):
        print(f"ERROR: {classfile} file does not exist")
        sys.exit(1)

    # Read classes from file
    with open(classfile,"r") as f:
        classes = f.read().split("\n")
    classes = [c for c in classes if c != '']
    print(len(classes), "classes:", *classes)

    # Start compiling list of all image filenames, while simultaneously converting XML files to TXT format
    f = open(listfile, "w")
    for i, xml in enumerate(glob(os.path.join(datadir, "*.xml"))):
        jpg = xml.replace(".xml", ".jpg")
        xml2txt(xml, classes)
        f.write(f"{jpg}\n")
        if (i + 1) % 100 == 0:
            print(i + 1)
    f.close()


def xml2txt(xml, classes):
    '''Convert XML file to TXT file required for YOLO.'''
    infile = open(xml)
    txt = xml.replace(".xml", ".txt")  # create new filename with txt extension
    outfile = open(txt, 'w')
    tree = ET.parse(infile)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), 
            float(xmlbox.find('xmax').text),
            float(xmlbox.find('ymin').text),
            float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        #outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        outfile.write(f"{cls_id} {bb[0]:0.6f} {bb[1]:0.6f} {bb[2]:0.6f} {bb[3]:0.6f}\n")
        #print(f"{txt} created")

    # Close file objects
    infile.close()
    outfile.close()


def convert(size, box):
    '''Make bounding box tuple from input parameters.'''
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


if __name__ == "__main__":
    main()
