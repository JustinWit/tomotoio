# run_yolov3.py 
# Try to run YOLOv3 on streaming video. <crosses fingers>

import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import os
import random
import pdb

DATADIR = 'data'  # directory in which to store any images
EXT = 'jpg'  # filename extension
CAMERA = 'Logitech C920x'  # name of the camera (and subsequently, the cv2 window)
MIRROR = False  # mirror image or not?
CLASSFILE = 'card.names'  # file containing class names
MODELCONFIG = 'yolov3_cards.cfg'
MODELWEIGHTS = 'yolov3_cards_2900.weights'
MODELSIZE = 416  # width and height of the model input, in pixels
THOLD = 0.6  # confidence threshold
NMS = 0.5  # threshold for non-maxima suppression
DETECT = True

def main():
    # Get class labels
    labels = []
    with open(CLASSFILE, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')
    print('LABELS:', *labels)

    # Load neural network
    net = cv2.dnn.readNetFromDarknet(MODELCONFIG, MODELWEIGHTS)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    layers = net.getLayerNames()
    outputlayers = [layers[i[0]-1] for i in net.getUnconnectedOutLayers()]

    # Start video stream
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # camera indexing starts at 0, but that is typically the integrated webcam
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cv2.namedWindow(CAMERA)
    while cv2.getWindowProperty(CAMERA, cv2.WND_PROP_VISIBLE) > 0:
        success, img = cam.read()
        if MIRROR: 
            img = cv2.flip(img, 1)
        cv2.imshow(CAMERA, img)
        # cv2.imshow(CAMERA, cv2.resize(img, (1280, 720)))

        if DETECT:
            blob = cv2.dnn.blobFromImage(img, 1/255, (MODELSIZE, MODELSIZE), [0, 0, 0], 1, crop=True)
            net.setInput(blob)
            outputs = net.forward(outputlayers)
            # findobjects(outputs, img, labels)
        
        # Monitor user key presses
        key = cv2.waitKey(1)
        if key == 27:  # Esc to exit
            break
        if key == ord('s'): # save
            filename = randomfilename(DATADIR, "jpg", prefix="")
            print(f"saving image to file: {filename}")
            cv2.imwrite(filename, img)
        if key == ord('d'):  # debug
            print(img.shape)
            # print(layers)
            print(outputs)
            print(len(outputs))
            print(outputs[0].shape)
            print(outputs[1].shape)
            print(outputs[2].shape)
        if key == ord('f') and DETECT:  # find objects in image
            value = mostlikelycard(outputs, labels)
            print(value)

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()

def randomfilename(dirname, ext, prefix=""):
    """ Return a new filename or a list of new filenames in directory 'dirname'
        If 'ext' is a list, one filename per extension in 'ext':
        filename = dirname + "/" + prefix + random number + "." + suffix
        (same random number for all the file extensions)

        Example: 
        >>> randomfilename("data", "jpg", prefix="prefix")
        'data/prefix408290.jpg'
        >>> randomfilename("data", ["jpg", "xml"])
        ['data/877739.jpg', 'data/877739.xml']        
    """
    if not isinstance(ext, list):
        ext = [ext]
    ext = [p if p[0] == '.' else '.' + p for p in ext]  # add the '.' if needed
    
    while True:
        id = "%06d" % random.randint(0, 999999)
        filenames = []
        for suffix in ext:
            fname = os.path.join(dirname, prefix + id + suffix)
            if not os.path.isfile(fname):
                filenames.append(fname)
        if len(filenames) == len(ext): break
    
    if len(filenames) == 1:
        return filenames[0]
    else:
        return filenames

def findobjects(outputs, img, labelnames):
    # img = cv2.resize(img, (1280, 720))
    hei, wid, clr = img.shape
    print(img.shape)
    bbox = []
    labels = []
    confidences = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            label = np.argmax(scores)
            confidence = scores[label]
            if confidence > THOLD:
                print(detection[:4])
                w = int(detection[2] * MODELSIZE)
                h = int(detection[3] * MODELSIZE)
                x = int((detection[0] * MODELSIZE) + (wid - MODELSIZE)/2 - w/2)
                y = int((detection[1] * MODELSIZE) + (hei - MODELSIZE)/2 - h/2)
                # x = int((detection[0] * MODELSIZE) + (wid - MODELSIZE)/2 - w/2)
                # y = int((detection[1] * MODELSIZE) + (hei - MODELSIZE)/2 - h/2)
                bbox.append([x, y, w, h])
                labels.append(label)
                confidences.append(float(confidence))

    print(f'How many objects were found? {len(bbox)}')

    # Apply non-maxima suppression
    indices = cv2.dnn.NMSBoxes(bbox, confidences, THOLD, NMS)
    for i in indices:
        i = i[0]  # because i is a list of lists
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        print(f'{labelnames[labels[i]]} (conf={confidences[i]:0.3f}) at [{x}, {y}, {w}, {h}]')
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    
    cv2.imshow(CAMERA, img)

def mostlikelycard(outputs, labelnames):
    cards = np.zeros(len(labelnames))
    for output in outputs:
        cards += np.sum(output[:, 5:], axis=0)
    
    if max(cards) < 0.5:
        print("NO CARD FOUND")
        return -1

    whichcard = labelnames[np.argmax(cards)][0]
    if whichcard in 'TJQK':
        return 10
    elif whichcard == 'A':
        return 11
    else:
        return int(whichcard)


if __name__ == "__main__":
    main()
