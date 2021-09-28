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

	drawBot.setMotor(65, 65, 2.2)
	sleep(3)
	drawBot.setMotor(-45, -45, 2.2)
	sleep(3)


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