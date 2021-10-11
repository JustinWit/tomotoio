# save_camera_images.py 
# Simple Python script to save images from a webcam.

import cv2
import os

DATADIR = 'data'  # directory in which to save images
PREFIX = 'allcards'  # prefix of image filenames
EXT = 'jpg'  # filename extension
MIRROR = False  # mirror image or not?
CAMERA = 'Logitech C920x'  # name of the camera (and subsequently, the cv2 window)


def main():
    # Make data directory, if needed
    if not os.path.isdir(DATADIR):
        os.makedirs(DATADIR)

    # Show video until Esc is pressed or window is closed
    num = 1
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # camera indexing starts at 0, but that is typically the integrated webcam
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv2.namedWindow(CAMERA)
    while cv2.getWindowProperty(CAMERA, cv2.WND_PROP_VISIBLE) > 0:
        _, img = cam.read()
        if MIRROR: 
            img = cv2.flip(img, 1)
        cv2.imshow(CAMERA, img)

        # Monitor user key presses
        key = cv2.waitKey(1)
        if key == 27:  # Esc to exit
            break
        if key == ord('s'): # S to save
            filename = '{0}{1:02d}.{2}'.format(PREFIX, num, EXT)
            num += 1
            print(f"saving image to file: {os.path.join(DATADIR, filename)}")
            cv2.imwrite(os.path.join(DATADIR, filename), img)

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()