#!/usr/bin/python

import adafruit_pca9685
from adafruit_servokit import ServoKit
from threading import Timer
import math
import time
import logger
import board
import busio

# Hardware initialization
i2c = busio.I2C(board.SCL, board.SDA)
pwm = adafruit_pca9685.PCA9685(i2c)
pwm.frequency = 60
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, channel, name, min, max):
        self.channel = channel
        self.name = name
        self.min = min
        self.max = max
        self.current_angle = -1337
        self.servoMin = 750  # Min pulse length out of 4096
        self.servoMax = 2500  # Max pulse length out of 4096
        kit.servo[self.channel].set_pulse_width_range(self.servoMin, self.servoMax)

    def set_angle(self, angle, callback=None):
        if not self.is_within_bounds(angle):
            logger.log("Angle outside of [%s]'s bounds: %s <= %s <= %s" % (self.name, self.min, angle, self.max), logger.Level.ERROR)
            return -1
        logger.log("Moving %s to angle %s" % (self.name, angle), logger.Level.DEBUG)
        kit.servo[self.channel].angle = angle
        self.current_angle = angle
        delta = 170
        if callback != None:
            Timer(1, callback).start()
        return 1

    def is_within_bounds(self, angle):
        return angle >= self.min and angle <= self.max

    def rest(self):
        kit.servo[self.channel].angle = None
        self.current_angle = -1
        logger.log("Resting %s" % (self.name), logger.Level.DEBUG) 

class Arm:
    def __init__(self):
        self.INNER_ARM_LENGTH = 134.5
        self.OUTER_ARM_LENGTH = 148
        self.ROT_CENTER = 90
        self.ROT_MIN = 0
        self.ROT_MAX = 180
        self.A_VERTICAL = 7 # a servo angle when wing is vertical
        self.B_VERTICAL = 50 # b servo angle when wing is vertical
        self.A_MIN = 10
        self.B_MIN = 70
        self.A_MAX = 100
        self.B_MAX = 180
        self.CLAW_MIN = 80
        self.CLAW_MAX = 145

        self.rot_servo = Servo(0, "rot", self.ROT_MIN, self.ROT_MAX)
        self.b_servo = Servo(1, "b", self.B_MIN, self.B_MAX)
        self.a_servo = Servo(2, "a", self.A_MIN, self.A_MAX)
        self.claw_servo = Servo(3, "claw", 80, 145)

        self.last_move = None

    def open_claw(self, callback=None):
        self.claw_servo.set_angle(145, callback)


    def close_claw(self):
        self.claw_servo.set_angle(self.claw_servo.min)


    def reset_servos(self):
        """ Reset servos to original location """
        self.rot_servo.set_angle(self.ROT_CENTER)
        self.claw_servo.set_angle(90)
        self.a_servo.set_angle(45)
        self.close_claw()


    def rest_servos(self):
        """ Temporarily disable the servos """
        self.rot_servo.rest()
        self.a_servo.rest()
        self.b_servo.rest()
        self.claw_servo.rest()

    def distance(self, start_point, end_point):
        """ Returns the distance from the first point to the second """
        return math.sqrt((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2)

    def law_of_cosines(self, a, b, c):
        """ Performs the Law of Cosines on the given side lengths """
        return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

    def move_to(self, x, y):
        """ Returns the angles necessary to reach the given coordinate point """
        distance_to_goal = self.distance((0, 0), (x, y))
        if distance_to_goal == 0:
            logger.log("Cannot move to origin", logger.Level.ERROR)
            return False
        angle_from_horizontal = math.degrees(math.asin(y / distance_to_goal))
        try:
            triangle_a = self.law_of_cosines(self.INNER_ARM_LENGTH, distance_to_goal, self.OUTER_ARM_LENGTH)
            triangle_b = self.law_of_cosines(self.INNER_ARM_LENGTH, self.OUTER_ARM_LENGTH, distance_to_goal)
            logger.log("[Triangle] a: %s, b: %s, angle from horiz: %s" % (triangle_a, triangle_b, angle_from_horizontal), logger.Level.DEBUG)
            servo_angle_a = 90 - triangle_a - angle_from_horizontal
            servo_angle_b = triangle_b - servo_angle_a + angle_from_horizontal
            if not self.a_servo.is_within_bounds(self.A_VERTICAL + servo_angle_a) or not self.b_servo.is_within_bounds(self.B_VERTICAL + servo_angle_b):
                logger.log("[Servos] a: %s, b: %s" % (self.A_VERTICAL + servo_angle_a, self.B_VERTICAL + servo_angle_b), logger.Level.ERROR)
                logger.log("Coordinates out of range due to servo constraints", logger.Level.ERROR)
                return False
            self.a_servo.set_angle(self.A_VERTICAL + servo_angle_a)
            self.b_servo.set_angle(self.B_VERTICAL + servo_angle_b)
            logger.log("[Servos] a: %s, b: %s" % (servo_angle_a, servo_angle_b), logger.Level.DEBUG)
            self.last_move = [x, y]
            return True
        except ValueError:
            logger.log("Coordinates out of range due to the physical laws of the universe", logger.Level.ERROR)
        return False