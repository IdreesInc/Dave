#!/usr/bin/python

class CColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Level:
    DEBUG = 0
    NORMAL = 1
    WARNING = 2
    ERROR = 3
    NONE = 4

log_level = Level.NORMAL

def log(message, type=Level.NORMAL):
    if type >= log_level:
        if type == Level.NORMAL:
            print(message)
        elif type == Level.DEBUG:
            print("DEBUG: " + message)
        elif type == Level.WARNING:
            print(CColors.WARNING + "WARNING: " + message + CColors.ENDC)
        elif type == Level.ERROR:
            print(CColors.ERROR + "ERROR: " + message + CColors.ENDC)

def warn(message):
    log(message, Level.WARNING)

def error(message):
    log(message, Level.ERROR)

def prompt(message):
    print(CColors.GREEN + message + CColors.ENDC)
    return input()