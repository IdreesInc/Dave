#!/usr/bin/python
# pylint: disable=import-error
import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
import threading
import time
from pyzbar import pyzbar

import logger

debug = True

class Eye:
    def start(self):
        logger.log("Starting eye")
        self.cam = cv2.VideoCapture(0)

    def look(self):
        ret_val, img = self.cam.read()
        self.frame = img
        return img

    def show_image(self, image):
        cv2.imshow('Dave', image)
        if cv2.waitKey(1) == 27: 
            return  # esc to quit

    def detect_qr_codes(self, image):
        frame = imutils.resize(image, width = 400)
        barcodes = pyzbar.decode(frame)

        # https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
        for barcode in barcodes:
            points = barcode.polygon
            # https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/
            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else: 
                hull = points
            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[ (j + 1) % n], (0, 0, 255), 1)

            (x, y, w, h) = barcode.rect
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return frame
        
    def find_card(self, image):
        lower = np.array([155, 90, 75])
        upper = np.array([179, 255, 255])

        copy = imutils.resize(image, width=1000)
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


class EyeThread (threading.Thread):
   def __init__(self, eye):
        threading.Thread.__init__(self)
        self.eye = eye

   def run(self):
        self.eye.look()
        logger.log