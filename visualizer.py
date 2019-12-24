#!/usr/bin/env python3
# pylint: disable=import-error

import matplotlib.pyplot as plt
import numpy as np
import logger
from kinematics import Arm
import math

logger.log_level = logger.Level.NONE
arm = Arm()

x_values = []
y_values = []

for x in range(0, 300):
    if not x % 2 == 0:
        continue
    for y in range(-100, 200):
        if not y % 2 == 0:
            continue
        if arm.move_to(x, y, testing=True):
            x_values.append(x)
            y_values.append(y)
        if x % 50 == 0 and y % 50 == 0:
            print("x: %s, y: %s" % (x, y))
  
print("Done testing")

fig, ax = plt.subplots()

# Plot range of motion
ax.plot(x_values, y_values, marker=".")

target, = ax.plot(0, 0, marker="o")
low_bar, = ax.plot([0, 0], [0, 0])
back_bar, = ax.plot([0, 0], [0, 0])

logger.log_level = logger.Level.DEBUG

def show_move(x, y, testing=True):
    logger.log("Moving to x: %s, y: %s" % (int(x), int(y)))
    arm.move_to(x, y, testing=testing)

    target.set_xdata(x)
    target.set_ydata(y)


    a_real = math.radians(90 - (arm.a_servo.current_angle - arm.A_VERTICAL))
    low_bar.set_xdata([0, math.cos(a_real) * arm.INNER_ARM_LENGTH])
    low_bar.set_ydata([0, math.sin(a_real) * arm.INNER_ARM_LENGTH])

    b_real = math.radians(90 - (arm.B_VERTICAL - arm.b_servo.current_angle))
    back_bar.set_xdata([0, math.cos(b_real) * arm.BACK_BAR_LENGTH])
    back_bar.set_ydata([0, math.sin(b_real) * arm.BACK_BAR_LENGTH])

    plt.draw()

show_move(240, 0)

def onclick(event):
    show_move(event.xdata, event.ydata, testing=(event.button == 1))

cid = fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('pick_event', onclick)

plt.xlabel('X') 
plt.ylabel('Y') 
plt.title('Range of Motion') 
plt.xlim([-100, 300])
plt.ylim([-100, 200])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()