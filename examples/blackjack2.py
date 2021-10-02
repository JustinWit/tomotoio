from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [393, 328, 180]
drawBotTask = [175, 328, 180]

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

dealBot.moveTo(dealBotDealer)
sleep(2)

# movements for dealing card, initial deal of 3 cards, 2 to player one to dealer
for i in range(3):
	drawBot.moveTo(drawBotTask, "03", 80, "02")
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

	#dealCard every other
	dealBot.moveTo(dealBotPlayer if (i%2 == 0) else dealBotDealer)

print("Hit or Stand? (H/S)")
response = input()

while response.upper() != "S":
	# dealBot to dealer side
	dealBot.moveTo(dealBotDealer)

	drawBot.moveTo(drawBotTask, "03", 80, "02")
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

	dealBot.moveTo(dealBotPlayer)
	sleep(2)

	print("Hit or Stand? (H/S)")
	response = input()

response = ""

while response.upper() != "S":
	# dealBot to player side
	dealBot.moveTo(dealBotPlayer)

	drawBot.moveTo(drawBotTask, "03", 80, "02")
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

	dealBot.moveTo(dealBotDealer)
	sleep(2)

	print("Dealer, Hit or Stand? (H/S)")
	response = input()




releaseCubes(cubes)