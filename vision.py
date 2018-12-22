#!/usr/bin/python

import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
import threading
import time

import logger

class Eye:
    def start(self):
        self.cam = VideoStream(src=0).start()

    def look(self):
        self.frame = self.cam.read()
        return self.frame

    def find_card(self):
        lower = np.array([155, 90, 75])
        upper = np.array([179, 255, 255])

        copy = imutils.resize(self.frame, width=1000)
        blurred = cv2.GaussianBlur(copy, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        height, width, _ = copy.shape

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        if len(contours) > 0:
            max_area = 0
            biggest_contour = contours[0]
            for contour in contours:
                area = cv2.contourArea(contour)
                if (area > max_area):
                    max_area = area
                    biggest_contour = contour

            if max_area > 200:
                M = cv2.moments(biggest_contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                offsetX = int(cX - width / 2)
                offsetY = int(cY - height / 2)
                return offsetX, offsetY

    #         if debug:
    #             cv2.drawContours(frame, [biggest_contour], -1, (0, 255, 0), 2)
    #             cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
    #             cv2.putText(frame, str(offsetX) + " " + str(offsetY), (cX - 30, cY - 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    # if debug:
    #     cv2.imshow("Circles", frame)


# class EyeThread (threading.Thread):
#    def __init__(self, eye):
#       threading.Thread.__init__(self)
#       self.eye = eye

#    def run(self):
#       self.eye.look()