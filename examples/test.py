from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()
robot = cubes[0]

def MoveRobot(location):
	finish = False
	while(finish == False):
		robot.moveTo(location)

		while robot.getMotorStatus()[0] != 131:
			print(robot.getMotorStatus())
			pass
		
		exitCode = robot.getMotorStatus()[2]
		print(exitCode)

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			robot.setMotor(-20, -20, 1)
			sleep(1)
		else:
			print(exitCode)
			break

MoveRobot([250, 250, 90])

releaseCubes(cubes)