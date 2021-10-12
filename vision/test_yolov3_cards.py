# test_yolov3.py 
# Basic script to test YOLOv3 model.
#
# Reference: https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/

from yolo3_one_file_to_detect_them_all import *
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import pdb
from time import time

WEIGHTS = 'yolov3_cards_2900.weights'
FILENAME = 'data/842763.jpg'
LABELFILE = 'data/cardnames.txt'
THOLD = 0.3

def main():
    # Make YOLOv3 model, load weights, and save
    model = make_yolov3_model()
    weight_reader = WeightReader(os.path.expanduser(WEIGHTS))
    weight_reader.load_weights(model)
    # model.save('model.h5')

    # Load and use model on test image
    t0 = time()
    # model = load_model('model.h5')
    print("TIME TO LOAD MODEL:", time() - t0)
    t0 = time()
    wid, hei = 416, 416  # define expected input shape of the model
    img, w, h = load_image_pixels(FILENAME, (wid, hei))
    pred = model.predict(img)
    print([a.shape for a in pred])
    print("TIME TO PREDICT:", time() - t0)

    # Interpret results
    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    boxes = []
    for i in range(len(pred)):
        boxes += decode_netout(pred[i][0], anchors[i], THOLD, hei, wid)
    correct_yolo_boxes(boxes, h, w, hei, wid)
    do_nms(boxes, 0.5)
    v_boxes, v_labels, v_scores = getboxes(boxes, list(np.loadtxt(LABELFILE, dtype='str')), THOLD)
    for i in range(len(v_boxes)):
        print(v_labels[i], v_scores[i])

    # Draw bounding box on image
    print("TIME TO PROCESS IMAGE:", time() - t0)
    # print(v_boxes, v_labels, v_scores)
    drawboxes(FILENAME, v_boxes, v_labels, v_scores)
    # plt.waitforbuttonpress()

def crop(img, wid, hei):
    '''Crop image to desired wid and hei.'''
    cx, cy = (img.shape[1] - wid) // 2, (img.shape[0] - hei) // 2
    img = img[cy:cy + hei, cx:cx + wid]
    # print(img.shape)
    return img


def load_image_pixels(filename, shape):
    '''Load and prepare an image for YOLOv3.'''
    img = load_img(filename)
    img = img_to_array(img)  # convert to numpy array
    width, height = 832, 832
    img = crop(img, width, height)
    # width, height = img.size  # get actual size of image
    # w, h = shape
    # cornerx, cornery = (width - w * 2) // 2, (height - h * 2) // 2
    # print(f'width {width}, height {height}')
    # img = load_img(filename, target_size=shape)  # load image with target size
    # img = img[cornery:cornery + h * 2, cornerx:cornerx + w * 2]
    # width, height = 2 * w, 2 * h
    img = img.astype('float32')  # scale pixel values to [0, 1]
    img /= 255.0
    img = np.expand_dims(img, 0)  # add a dimension so that we have one sample
    # pdb.set_trace()
    return img, width, height


def getboxes(boxes, labels, thresh):
    '''Get all of the bounding boxes above a threshold.'''
    v_boxes, v_labels, v_scores = [], [], []
	# enumerate all boxes
    for box in boxes:
        # enumerate all possible labels
        for i in range(len(labels)):
            # check if the threshold for this label is high enough
            if box.classes[i] > thresh:
                v_boxes.append(box)
                v_labels.append(labels[i])
                v_scores.append(box.classes[i]*100)
                # don't break, many labels may trigger for one box
    
    return v_boxes, v_labels, v_scores


def drawboxes(filename, v_boxes, v_labels, v_scores):
    '''Draw boxes with labels and scores on image from file.'''
    img = plt.imread(filename)
    img = crop(img, 832, 832)
    plt.imshow(img)
    ax = plt.gca()
    for i in range(len(v_boxes)):
        box = v_boxes[i]
        y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
        width, height = x2 - x1, y2 - y1
        rect = Rectangle((x1, y1), width, height, fill=False, color='white')
        ax.add_patch(rect)
        label = "%s (%.3f)" % (v_labels[i], v_scores[i])
        plt.text(x1, y1, label, color='white')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()