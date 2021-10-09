from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()


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

target1 = [250, 250, 90]
target2 = [350, 350, 90]
target3 = [150, 250, 90]
target4 = [350, 150, 90]


# send total number of cubes, array of cubes position in cubes array, array of target location for respective cube
moveSim(4, [0, 1, 2, 3], [target1, target2, target3, target4])

cube0Response = cubes[0].getMotorStatus()[2]
cube1Response = cubes[1].getMotorStatus()[2]
cube2Response = cubes[2].getMotorStatus()[2]
cube3Response = cubes[3].getMotorStatus()[2]

print("cube0", cube0Response)
print("sube1", cube1Response)
print("cube2", cube2Response)
print("sube3", cube3Response)




releaseCubes(cubes)