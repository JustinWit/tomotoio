from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

drawBot = cubes[0]

drawBotStart = [379, 328, 182]
drawBotMid = [308, 329, 180]
drawBotTask = [205, 320, 180]

forward = [drawBotMid, drawBotTask]
backward = [drawBotMid, drawBotStart]

def Move_DrawBot(locations, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		drawBot.moveToMulti(len(locations), locations, motorType, maxSpeed, movementType)

		while(len(drawBot.getMotorStatus()) != 3):
			pass

		exitCode = drawBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		# did not reach high enough on card
		elif exitCode == 1:
			drawBot.setMotor(-20, -20, .2)
			sleep(.2)
			drawBot.setMotor(150, 150, 1)
			sleep(1)
			break

		elif exitCode == 2:
			drawBot.setMotor(-20, -20, .5)
			sleep(.5)
			break
		else:
			print("Error: ", exitCode)
			break

while True:
	Move_DrawBot(forward, "01", 100, "00")
	Move_DrawBot(backward, "00", 60, "00")
	input()


releaseCubes(cubes)