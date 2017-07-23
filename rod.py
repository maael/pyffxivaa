import pyscreenshot as ImageGrab
try:
  import Image
except ImportError:
  from PIL import Image
import time
import ctypes
import cv2
import numpy as np

if __name__ == '__main__':
  previous_pos = None
  while True:
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    im = ImageGrab.grab(bbox=((width / 4), 0, width - (width / 4), height - (height / 4)))
    image = np.array(im.convert('RGB'))
    image = image[:, :, ::-1].copy()
    blur = cv2.blur(image, (5, 5))
    brightest = np.array([100, 255, 255], dtype='uint8')
    lowest = np.array([0, 100, 100], dtype='uint8')
    thresh = cv2.inRange(blur, lowest, brightest)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_cnt = 1
    for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > max_area:
          max_area = area
          best_cnt = cnt
    tracking_radius = (max_area / (2 * np.pi))
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    if previous_pos != None:
      change = (abs(previous_pos[0] - cx), abs(previous_pos[1] - cy))
      if (change[0] > tracking_radius or change[1] > tracking_radius):
        print('change', change)
    previous_pos = (cx, cy)
    time.sleep(0.5)
