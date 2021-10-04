from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [393, 328, 180]
moveBotStart = [263, 420, 90]
flipBotStart = [166, 203, 0]
dealBotDealer = [139, 140, 180]

# initialize all robots to starting posistions on board
drawBot.moveTo(drawBotStart)

moveBot.moveTo(moveBotStart)

flipBot.moveTo(flipBotStart)

dealBot.moveTo(dealBotDealer)

sleep(5)

releaseCubes(cubes)