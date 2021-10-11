from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()


flipBotStart = [166, 203, 0]
flipBotTask = [210, 115, 270]
while True:
	cubes[2].moveToMulti(2, [flipBotTask, flipBotStart])
	while(cubes[2].getMotorStatus()[0] != 132):
		pass

	exitCode = cubes[2].getMotorStatus()[2]

	print(exitCode)
	sleep(.5)

releaseCubes(cubes)