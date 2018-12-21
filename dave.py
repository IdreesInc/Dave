#!/usr/bin/python

import time
import threading

import logger
from kinematics import Arm
from vision import Eye

logger.log_level = logger.Level.NORMAL

class Thready (threading.Thread):
    def __init__(self, function = None):
        threading.Thread.__init__(self)
        self.running = True
        self.function = function

    def set_function(self, function):
        self.function = function

    def run(self):
        while self.running:
            self.function()

    def stop(self):
        self.running = False

arm = Arm()
eye = Eye()
input_thread = Thready()

def start():
    input_thread.set_function(get_input)
    input_thread.run()
    arm.reset_servos()
    arm.open_claw()
    arm.close_claw()

def shutdown():
    input_thread.stop()
    arm.reset_servos()
    time.sleep(0.75)
    arm.rest_servos()
    logger.log("Goodbye!")

def get_input():
    input = logger.prompt("Command?")
    command = input.split(" ")
    if len(command) == 2:
        if command[0] == "r" or command[0] == "rot" or command[0] == "rotation":
            arm.rot_servo.set_angle(float(command[1]))
        elif command[0] == "b":
            arm.b_servo.set_angle(float(command[1]))
        elif command[0] == "a":
            arm.a_servo.set_angle(float(command[1]))
        elif command[0] == "c" or command[0] == "claw":
            arm.claw_servo.set_angle(float(command[1]))
    elif len(command) == 3:
        if command[0] == "go" or command[0] == "move":
            arm.move(float(command[1]), float(command[2]))
    else:
        if command[0] == "q" or command[0] == "quit":
            shutdown()
        elif command[0] == "r" or command[0] == "reset":
            arm.reset_servos()
            logger.log("Servos reset")
        elif command[0] == "rest" or command[0] == "d" or command[0] == "disable":
            arm.rest_servos()
            logger.log("Servos set to rest")
        elif command[0] == "open":
            arm.open_claw()
            logger.log("Opening claw")
        elif command[0] == "close":
            arm.close_claw()
            logger.log("Closing claw")
        elif command[0] == "up":
            arm.b_servo.set_angle(80, arm.b_servo.rest)
        elif command[0] == "down":
            arm.b_servo.set_angle(0, arm.b_servo.rest)
        elif command[0] == "left":
            arm.rot_servo.set_angle(-80, arm.b_servo.rest)
        elif command[0] == "right":
            arm.rot_servo.set_angle(80, arm.b_servo.rest)
        elif command[0] == "back":
            arm.a_servo.set_angle(-70, arm.b_servo.rest)
        elif command[0] == "forward":
            arm.a_servo.set_angle(0, arm.b_servo.rest)
        elif command[0] == "hi" or command[0] == "hello" or command[0] == "greet":
            logger.log("Hello!")
            arm.open_claw(arm.close_claw)
        else:
            logger.log("Command '%s' not recognized" % (input), logger.Level.ERROR)

start()