from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

drawBot = cubes[0]

drawBotStart = [379, 333, 180]
drawBotMid = [[323, 330, 180], [308, 329, 180], [247, 329, 180]]
drawBotTask = [205, 333, 180]

forward = [drawBotMid[0], drawBotMid[1], drawBotMid[2], drawBotTask]
backward = [drawBotMid[2], drawBotMid[1], drawBotMid[0], drawBotStart]

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
			sleep(.5)
			drawBot.setMotor(150, 150, 1)
			sleep(1.3)
			break

		elif exitCode == 2:
			drawBot.setMotor(-20, -20, .5)
			sleep(.5)
			break
		else:
			print("Error: ", exitCode)
			break

# while True:
# 	Move_DrawBot([drawBotTask], "01", 100, "00")
# 	sleep(.8)
# 	Move_DrawBot([drawBotStart], "00", 60, "00")
# 	input()

drawBot.setSoundEffect(7)


releaseCubes(cubes)