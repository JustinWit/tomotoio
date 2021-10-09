from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()
robot = cubes[0]


while True:
	sleep(5)
	print(robot.getMotion())
	robot.motionRest()

releaseCubes(cubes)