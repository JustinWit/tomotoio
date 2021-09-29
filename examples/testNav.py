from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()
navs = createNavigators(cubes)

testCube1, testCube2 = navs[0], navs[1]

try:
	
	cubes[0].setMotor(10, -10, 1)
	# x pos(actual), y pos(actual), angle
	target = (500, 500, 270)
	sleep(1)
	cubeX, cubeY, cubeZ = testCube1.lastPosition.x, testCube1.lastPosition.y, testCube1.lastPosition.angle
	targetX, targetY, targetZ = testCube2.lastPosition.x, testCube2.lastPosition.y, testCube2.lastPosition.angle

	target = (targetX, targetY, targetZ)

	print(cubeX)
	print(cubeY)
	print(cubeZ)



	# a positive height means the target is below the robot, negative the target is above the robot
	# a negative lenght means the target is to the left of the robot, positve the target is to the right
	height = target[1] - cubeY 
	length = target[0] - cubeX

	# calculates robots angle to target relative to its x-axis
	targetAngle = round(math.degrees(math.atan(abs(length)/abs(height))))

	print("height: ", height)
	print("length: ", length)

	print("targetAngle", targetAngle)

	degreesToAdjust = 0

	# when target is up and left of robot
	if (height < 0 and length < 0):
		if(cubeZ < 180):
			degreesToAdjust = (180 - cubeZ + targetAngle)
		else: 
			degreesToAdjust = (cubeZ - 180 - targetAngle)

	# when target is up and right of robot
	elif (height < 0 and length > 0):
		if(cubeZ < 180):
			degreesToAdjust = cubeZ + targetAngle
		else: 
			degreesToAdjust = (360 - cubeZ - targetAngle)

	# when target is down and left of robot
	elif (height > 0 and length < 0):
		if(cubeZ < 180):
			degreesToAdjust = 180 - targetAngle - cubeZ
		else: 
			degreesToAdjust = -1 * (cubeZ - 180 + targetAngle)

	# when target is down and right of robot
	else:
		if(cubeZ < 180):
			degreesToAdjust = cubeZ - targetAngle
		else: 
			degreesToAdjust = -1 * (cubeZ - targetAngle)

	print("adjust by :", degreesToAdjust)

	cubes[0].setMotor(10, -10, abs((.75/90)*degreesToAdjust))

	# while True:
	# 	c = testCube1.mat.center
	# 	print("before: ", testCube1.lastPosition)
	# #	testCube1.move(c.x, c.y, 80)
	# #	print("after: ", testCube1.lastPosition)

	# 	print()
	# 	sleep(1)


finally: 
	releaseCubes(cubes)