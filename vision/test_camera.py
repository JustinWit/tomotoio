# test_camera.py
# Python script to get images from Logitech C920x webcam.

import cv2

def main():
    # Setup camera
    name = 'Logitech C920x'  # name of the window
    mirror = True  # mirror image or not?
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # camera indexing starts at 0, but that is typically the integrated webcam

    # Show video until Esc is pressed or window is closed
    cv2.namedWindow(name)
    while cv2.waitKey(1) != 27 and cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) > 0:
        _, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow(name, img)

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()