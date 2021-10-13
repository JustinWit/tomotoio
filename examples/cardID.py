from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

cubes[0].moveTo([243, 281, 270])

sleep(2)

cubes[0].moveTo([243, 304, 270], "00", 20, "00")
while True:
	print("StandardID ", cubes[0].getStandardID())
	print("Motor Status ", cubes[0].getMotorStatus())
	if(cubes[0].getStandardID()[1] == "2"):
		card = cubes[0].getStandardID()
		while cubes[0].getStandardID()[1] != "1":
			cubes[0].setMotor(10, 10, .5)
			sleep(.5)
		cubes[0].moveTo([166, 203, 0])
		sleep(2)
		break

print("card value: ", card[3])

