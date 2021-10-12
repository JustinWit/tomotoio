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
import pdb

WEIGHTS = 'yolov3.weights'
FILENAME = 'data/zebra.jpg'
LABELS = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]


def main():
    # Make YOLOv3 model, load weights, and save
    model = make_yolov3_model()
    weight_reader = WeightReader(WEIGHTS)
    weight_reader.load_weights(model)
    model.save('model.h5')

    # Load and use model on test image
    model = load_model('model.h5')
    wid, hei = 416, 416  # define expected input shape of the model
    img, w, h = load_image_pixels(FILENAME, (wid, hei))
    pred = model.predict(img)
    print([a.shape for a in pred])

    # Interpret results
    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    thold = 0.6  # confidence of class in the range [0,1]
    boxes = []
    for i in range(len(pred)):
        boxes += decode_netout(pred[i][0], anchors[i], thold, hei, wid)
    correct_yolo_boxes(boxes, h, w, hei, wid)
    do_nms(boxes, 0.5)
    v_boxes, v_labels, v_scores = getboxes(boxes, LABELS, thold)
    for i in range(len(v_boxes)):
        print(v_labels[i], v_scores[i])

    # Draw bounding box on image
    drawboxes(FILENAME, v_boxes, v_labels, v_scores)
    # plt.waitforbuttonpress()


def load_image_pixels(filename, shape):
    '''Load and prepare an image for YOLOv3.'''
    img = load_img(filename)
    width, height = img.size  # get actual size of image
    img = load_img(filename, target_size=shape)  # load image with target size
    img = img_to_array(img)  # convert to numpy array
    img = img.astype('float32')  # scale pixel values to [0, 1]
    img /= 255.0
    img = np.expand_dims(img, 0)  # add a dimension so that we have one sample

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