from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()


for x in range(50):
	cubes[0].setMotor(x, x, 0)
	sleep(0.1)
cubes[0].setMotor(0, 0, 1)
sleep(2)
for x in range(30):
	cubes[0].setMotor(-x, -x, 0)
	sleep(0.1)
sleep(2)
cubes[0].setMotor(0, 0, 1)

sleep(1)

for x in range(50):
	cubes[1].setMotor(-x, -x, 0)
	sleep(0.05)
sleep(1.8)
cubes[1].setMotor(0, 0, 1)
sleep(3)
for x in range(50):
	cubes[1].setMotor(x, x, 0)
	sleep(0.1)
sleep(.2)
cubes[1].setMotor(0, 0, 1)
sleep(5)


	

releaseCubes(cubes)