from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(flipBot, moveBot, drawBot, dealBot) = (cubes[0], cubes[2], cubes[3], cubes[1])

def drawCard():
	# drawBot pulls card from shoe
	# moveBot pushes card to brick wall
	# flipBot filps card and pulls back
	# moveBot pulls back

	for x in range(50):
		drawBot.setMotor(x, x, 0)
		sleep(0.1)
	drawBot.setMotor(0, 0, 1)
	sleep(3)

	for x in range(30):
		drawBot.setMotor(-x, -x, 0)
		sleep(0.1)
	sleep(2)
	drawBot.setMotor(0, 0, 1)
	sleep(5)


	moveBot.setMotor(-65, -65, 0)
	sleep(3)
	moveBot.setMotor(-10, -10, 1)

	flipBot.setMotor(45, 45, 1)
	sleep(1.2)
	flipBot.setMotor(-45, -45, 1)
	sleep(1.2)

	moveBot.setMotor(45, 45, 0)
	sleep(3)
	moveBot.setMotor(10, 10, 1)

try:
	drawCard();

finally:
	releaseCubes(cubes)