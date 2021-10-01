from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [393, 333, 180]
drawBotTask = [150, 333, 180]

moveBotStart = [263, 420, 90]
moveBotTask = [263, 145, 90]

flipBotStart = [166, 203, 0]
flipBotTask = [203, 115, 270]

dealBotPlayer = [354, 133, 180]
dealBotDealer = [139, 140, 180]

# initialize all robots to starting posistions on board
drawBot.moveTo(drawBotStart)
sleep(2)

moveBot.moveTo(moveBotStart)
sleep(2)

flipBot.moveTo(flipBotStart)
sleep(2)

dealBot.moveTo(dealBotPlayer)
sleep(2)

# movements for dealing card

#drawBot Movement
for i in range(2):
	drawBot.moveTo(drawBotTask)
	sleep(3)
	drawBot.moveTo(drawBotStart, "01", 40)
	sleep(5)

	#moveBot and flipBot Movement
	moveBot.moveTo(moveBotTask)
	sleep(4)

	flipBot.moveTo(flipBotTask)
	sleep(2)
	flipBot.moveTo(flipBotStart)
	sleep(2)

	moveBot.moveTo(moveBotStart)
	sleep(4)

	#dealCard to dealer
	dealBot.moveTo(dealBotDealer)
	sleep(2)
	dealBot.moveTo(dealBotPlayer)
	sleep(2)

releaseCubes(cubes)