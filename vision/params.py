# params.py 
# Useful parameters for image processing of videos containing playing cards.

import numpy as np
import cv2

# Dimensions of the generated dataset images (in pixels)
imgW = 720
imgH = 720

# Card parameters (in mm)
cardW = 59
cardH = 89
cornerXmin = 1
cornerXmax = 10
cornerYmin = 2.5
cornerYmax = 26

# Convert the measures from mm to pixels: multiply by an arbitrary factor 'zoom'
zoom = 4
cardW *= zoom
cardH *= zoom
cornerXmin = int(cornerXmin * zoom)
cornerXmax = int(cornerXmax * zoom)
cornerYmin = int(cornerYmin * zoom)
cornerYmax = int(cornerYmax * zoom)

refCard = np.array([
    [0, 0], 
    [cardW, 0], 
    [cardW, cardH], 
    [0, cardH]], dtype=np.float32)
refCardRot = np.array([
    [cardW, 0], 
    [cardW, cardH], 
    [0, cardH], 
    [0, 0]], dtype=np.float32)
refCornerHL = np.array([
    [cornerXmin, cornerYmin],
    [cornerXmax, cornerYmin],
    [cornerXmax, cornerYmax],
    [cornerXmin, cornerYmax]], dtype=np.float32)
refCornerLR = np.array([
    [cardW - cornerXmax, cardH - cornerYmax],
    [cardW - cornerXmin, cardH - cornerYmax],
    [cardW - cornerXmin, cardH - cornerYmin],
    [cardW - cornerXmax, cardH - cornerYmin]], dtype=np.float32)
refCorners = np.array([refCornerHL, refCornerLR])

bord_size = 2 # border size alpha=0
alphamask = np.ones((cardH, cardW), dtype=np.uint8) * 255
cv2.rectangle(alphamask, (0, 0), (cardW - 1, cardH - 1), 0, bord_size)
cv2.line(alphamask, (bord_size * 3, 0), (0, bord_size * 3), 0, bord_size)
cv2.line(alphamask, (cardW - bord_size * 3, 0), (cardW, bord_size * 3), 0, bord_size)
cv2.line(alphamask, (0, cardH - bord_size * 3), (bord_size * 3, cardH), 0, bord_size)
cv2.line(alphamask, (cardW - bord_size * 3, cardH), (cardW, cardH - bord_size * 3), 0, bord_size)
