from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [379, 333, 180]
drawBotMid = [308, 329, 180]
drawBotTask = [205, 333, 180]

drawForward = [drawBotTask]
drawBackward = [drawBotStart]


moveBotStart = [263, 420, 90]
moveBotTask = [263, 145, 90]
moveBotDropCard = [263, 202, 90]

flipBotStart = [166, 203, 0]
flipBotTask = [210, 115, 270]

dealBotPlayer = [354, 133, 180]
dealBotDealer = [139, 140, 360]

clearDealer = [67, 135, 180]
clearPlayer = [429, 135, 360]

# initail configuration for cubes
dealBot.configHorizontal(10)

# methods for moving each robot and handling errors

# motorType: 00 - constant, 01 - accelerate, 02 de accelerate, 03 accelerate then de accelerate
# movementType: 00 - move and rotate, 01 - not backwards, 02 - rotate after

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

def dealCard(numCubes: int, cubeArr, cubesTarget):
	for i in range(numCubes):
		cubes[cubeArr[i]].moveTo(cubesTarget[i])
		sleep(1)

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

def flipCard(cubeArr, cubesTarget):
	cubes[cubeArr[0]].moveToMulti(1, cubesTarget[0], "01", 100, "00")
	cubes[cubeArr[1]].moveToMulti(2, [cubesTarget[1], cubesTarget[2]])

	while True:
		finish = True

		for i in range(2):
			if(cubes[cubeArr[i]].getMotorStatus()[0] != 132):
				finish = False
			if(cubes[cubeArr[i]].getMotorStatus()[0] == 132 and cubes[cubeArr[i]].getMotorStatus()[2] != 0):
				print("error cube", i)
				cubes[cubeArr[i]].setMotor(-20, -20, 1)
				sleep(1)
				if i == 0:
					cubes[cubeArr[i]].moveToMulti(1, [cubesTarget[0][0]], "00", 120, "00")
				else:
					cubes[cubeArr[i]].moveToMulti(1, [cubesTarget[0][0]])
				finish = False


		if finish == True:
			break





####################################################################
########                    Start of Game                   ########
####################################################################

# initialize all robots to starting posistions on board
drawBot.moveTo(drawBotStart)

Move_MoveBot(moveBotStart)

Move_FlipBot(flipBotStart)

Move_DealBot(dealBotDealer)


gamePlay = True

# first draw
Move_DrawBot(drawForward, "01", 100, "00")
sleep(.5)

while gamePlay:
	# initialize player and dealer totals
	playerTotal = 0
	dealerTotal = 0

	# initialize bust to false and playerBlackJack to false
	bust = False
	blackjack = False

	# initialize numAces for both dealer and player
	numAcePlayer = 0
	numAceDealer = 0

	# movements for dealing card, initial deal of 3 cards, 2 to player one to dealer
	
	# move dealBot to correct position
	dealBot.moveTo(dealBotDealer)
	for i in range(3):

		Move_DrawBot(drawBackward, "00", 60, "00")
		Move_MoveBot(moveBotTask, "03", 100)

		# here start simultanious move of flipBot and drawBot
		flipCard([0, 2], [drawForward, flipBotTask, flipBotStart])


		# start movebot return and deal at same time
		dealCard(2, [1, 3], [moveBotStart, dealBotPlayer if (i%2 == 0) else dealBotDealer])


		#########################################################################
		###    Get card value here from camera and add to respective total    ###
		cardValue = int(input("Enter Card Value: "))
		if i%2 == 0:
			playerTotal += cardValue
			if cardValue == 11:
				numAcePlayer += 1
			if playerTotal > 21 and numAcePlayer > 0:
				playerTotal -= 10
				numAcePlayer -= 1
			print(playerTotal)
		else:
			dealerTotal += cardValue
			if cardValue == 11:
				numAceDealer += 1
			print(dealerTotal)


	#########################################################################
	###   if player total == 21, deal to dealer check values for winner   ###
	if playerTotal == 21:
		blackjack = True

	# get player input from robot for hit and stand
	else:
		dealBot.setSoundEffect(0)
		while True:
			response = dealBot.getMotion()

			# if tapped hit and recheck playerTotal
			if response[3] == 1:
				dealBot.motionReset()
				dealBot.setSoundEffect(1)

				dealBot.moveTo(dealBotDealer)
				Move_DrawBot(drawBackward, "00", 60, "00")


				Move_MoveBot(moveBotTask, "03", 100)

				# here start simultanious move of flipBot and drawBot
				flipCard([0, 2], [drawForward, flipBotTask, flipBotStart])

				
				# start movebot return and deal at same time
				dealCard(2, [1, 3], [moveBotStart, dealBotPlayer])


				#########################################################################
				###    Get card value here from camera and add to player total       ###
				cardValue = int(input("Enter Card Value: "))
				playerTotal += cardValue
				if cardValue == 11:
					numAcePlayer += 1
				if playerTotal > 21 and numAcePlayer > 0:
					playerTotal -= 10
					numAcePlayer -= 1

					
				print(playerTotal)


				############################################################
				###   if player total > 21, bust and end game            ###

				if playerTotal > 21:
					bust = True
					break
				dealBot.setSoundEffect(0)

			# if tilted stand
			elif response[1] == 0:
				dealBot.motionReset()
				dealBot.setSoundEffect(2)
				sleep(1)
				break

	if bust == False:
		while dealerTotal < 17:
			dealBot.moveTo(dealBotPlayer)
			Move_DrawBot(drawBackward, "00", 60, "00")


			Move_MoveBot(moveBotTask, "03", 100)

			# here start simultanious move of flipBot and drawBot
			flipCard([0, 2], [drawForward, flipBotTask, flipBotStart])

			# start movebot return and deal at same time
			dealCard(2, [1, 3], [moveBotStart, dealBotDealer])


			#########################################################################
			###    Get card value here from camera and add to dealer total        ###
			###    if dealer busts, player win
			cardValue = int(input("Enter Card Value: "))
			dealerTotal += cardValue
			if cardValue == 11:
				numAceDealer += 1
			if dealerTotal > 21 and numAceDealer > 0:
				dealerTotal -= 10
				numAceDealer -= 1
			print(dealerTotal)

			if dealerTotal > 21:
				print("Dealer Busts")

			if blackjack:
				break
	# player busted, dealer win, end game
	else:
		print("player busted")
		playerTotal = 0

	###################################################
	### compare player and dealer totals for winner ###

	if playerTotal > dealerTotal or dealerTotal > 21:
		print("Player Wins")
		dealBot.setSoundEffect(6)

	elif dealerTotal > playerTotal:
		print("Dealer Wins")
		dealBot.setSoundEffect(5)

	else:
		print("It's a Tie")
		dealBot.setSoundEffect(10)


	###########################################################
	### Get user input from a robot to quit or play again   ###
	### hit to play again stand to quit                     ###
	Move_DealBot(dealBotPlayer)
	dealBot.setSoundEffect(0)
	while True:
		response = dealBot.getMotion()

		if response[3] == 1:
			# clear board with dealbot and reset game
			Move_DealBot(clearPlayer)
			Move_DealBot(clearDealer)
			dealBot.motionReset()
			break
		if response[1] == 0:
			gamePlay = False
			dealBot.setSoundEffect(5)
			break





	

releaseCubes(cubes)