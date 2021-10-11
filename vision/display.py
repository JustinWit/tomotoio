# display.py
# Helper function to display images.

import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def display(img, polygons=[], channels="bgr", size=9):
    """Display an image with optional polygons (e.g. bounding boxes, convex hulls) overlayed."""  
    # Show image
    if channels == "bgr":  # cv2 images are 'bgr'
        numchannels = img.shape[2]
        if numchannels == 4:
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    _, ax = plt.subplots(figsize=(size, size))
    ax.set_facecolor((0, 0, 0))
    ax.imshow(img)

    # Add polygons to image, if requested
    if not isinstance(polygons, list):
        polygons = [polygons]  
    for polygon in polygons:
        # A polygon has either shape (n,2) or (n,1,2) if it is a cv2 contour (like convex hull). In the latter case, reshape to (n,2)
        if len(polygon.shape) == 3:
            polygon = polygon.reshape(-1, 2)
        patch = patches.Polygon(polygon, linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(patch)