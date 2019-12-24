#!/usr/bin/python
# pylint: disable=import-error

# This file only exists as a testbed for OpenCV stuff

import numpy as np
import cv2
from hush import suppress_stdout_stderr
import sys
import time

print("hi!")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
# time.sleep(5)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    print("errar", file=sys.stderr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print("bye!")
