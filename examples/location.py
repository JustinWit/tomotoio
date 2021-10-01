from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

cubes[0].moveTo(320, 80, 90)
sleep(5)