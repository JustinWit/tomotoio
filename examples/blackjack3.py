from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [393, 328, 180]
drawBotTask = [154, 328, 180]

moveBotStart = [263, 420, 90]
moveBotTask = [263, 145, 90]
moveBotClearDraw = [263, 193, 90]

flipBotStart = [166, 203, 0]
flipBotTask = [210, 115, 270]

dealBotPlayer = [354, 133, 180]
dealBotDealer = [139, 140, 360]

# initail configuration for cubes
dealBot.configHorizontal(10)

# methods for moving each robot and handling errors

# motorType: 00 - constant, 01 - accelerate, 02 de accelerate, 03 accelerate then de accelerate
# movementType: 00 - move and rotate, 01 - not backwards, 02 - rotate after

def Move_DrawBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		drawBot.moveTo(location, motorType, maxSpeed, movementType)

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

def Move_MoveBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		moveBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(moveBot.getMotorStatus()) != 3):
			pass

		exitCode = moveBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			moveBot.setMotor(40, 40, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break

def Move_FlipBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		flipBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(flipBot.getMotorStatus()) != 3):
			pass

		exitCode = flipBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			flipBot.setMotor(20, 20, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break

def Move_DealBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		dealBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(dealBot.getMotorStatus()) != 3):
			pass

		exitCode = dealBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			dealBot.setMotor(20, 20, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break


def moveSim(numCubes: int, cubeArr, cubesTarget):
	for i in range(numCubes):
		cubes[cubeArr[i]].moveTo(cubesTarget[i])

	while True:
		finish = True

		for i in range(numCubes):
			if(cubes[cubeArr[i]].getMotorStatus()[0] != 131):
				finish = False
			if(cubes[cubeArr[i]].getMotorStatus()[0] == 131 and cubes[cubeArr[i]].getMotorStatus()[2] != 0):
				print("error cube", i)
				cubes[cubeArr[i]].setMotor(-20, -20, 1)
				sleep(1)
				cubes[cubeArr[i]].moveTo(cubesTarget[i])
				finish = False


		if finish == True:
			break

# initialize all robots to starting posistions on board
Move_DrawBot(drawBotStart)

Move_MoveBot(moveBotStart)

Move_FlipBot(flipBotStart)

Move_DealBot(dealBotDealer)

# movements for dealing card, initial deal of 3 cards, 2 to player one to dealer
Move_DrawBot(drawBotTask, "01", 80, "00")
for i in range(3):


	Move_DrawBot(drawBotStart, "00", 40, "00")
	#moveBot and flipBot Movement
	Move_MoveBot(moveBotClearDraw, "03", 100)

	# here start simultanious movement of draw and move and flip
	drawBot.moveTo(drawBotTask, "01", 80, "00")
	moveBot.moveTo(moveBotTask)
	flipBot.moveTo(flipBotTask)

	sleep(3)

	flipBot.moveTo(flipBotStart)
	sleep(.2)
	moveBot.moveTo(moveBotClearDraw)
	sleep(1)

	#dealCard every other
	dealBot.moveTo(dealBotPlayer if (i%2 == 0) else dealBotDealer, "03", 80, "02")
	Move_MoveBot(moveBotStart)

releaseCubes(cubes)