from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()
navs = createNavigators(cubes)

testCube1 = navs[3]

try:
	while True:
		c = testCube1.mat.center
		print("before: ", testCube1.lastPosition)

		print()
		sleep(1)


finally: 
	releaseCubes(cubes)