
# Dave, the Playful Robotic Arm
The goal of this project is to create a robotic arm that can play games, whether locally or against a remote opponent. You can either play against Dave or against a remote player, whose movements will then be applied to your board. This way, you and your friend can play a physical game like chess anywhere across the world!
This project is a work in progress, meaning that I am updating this repo as I go. If you have any questions or comments, feel free to contact me from my [website](http://idreesinc.com)!

## Hardware
- daGHIZmo's wonderful  [EEZYbotARM MK2](https://www.thingiverse.com/thing:1454048)
	- 3D printed in Hatchbox PLA using a modified ANET A8 printer
- [Raspberry Pi 3](https://www.raspberrypi.org) for processing
- [Adafruit Servo Hat](https://www.adafruit.com/product/2327) for easy servo controls

## Current Features
- Implemented ability to set servo angles via Raspberry Pi and Adafruit Servo Hat
- As of July 1st, implemented cartesian coordinate system which allows me to use standard x and y coordinates to accurately move the arm to within 1 mm accuracy

### Next Goal
- Implement game piece detection using OpenCV in a lightweight manner
	- Most likely going to be based off of color detection and simple outline detection rather than complex image recognition, as the goal is to be as lightweight as possible

## Longterm Goals
- To play chess using a custom built curved vertical chess board
- Ability to play against the computer or against a remote opponent who also has a Dave robot, allowing each player's move to be physically synced on their respective board

## FAQ
### Why?
Because I can! And because the idea of playing a physical game with my friend from Purdue all the way here at UNC is pretty cool in my opinion. Plus this project allows me to get involved in Python, robotics, and computer vision, which is always a plus!
### Why use the [EEZYbotARM MK2](https://www.thingiverse.com/thing:1454048) for this project?
Mostly because it is a popular, open source design for a 3D printable robot. The benefits of 3D printing the robot as opposed to just getting a kit is that I can customize the bot however I wish, including changing the claw to better grip the game pieces and adding a mount for the sensors.
Plus it is cheap, and I needed a justification for spending all that time and money making my 3D printer.
### Why is it named Dave?
Well it was either that or Steve

<br/>
<p align="center"><a href="http://idreesinc.com"><img src="http://idreesinc.com/images/logo_transparent.png" width=200 height=200></a></p>
