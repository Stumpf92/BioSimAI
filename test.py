import numpy as np

matrix = np.zeros((10*2+1,10*2+1))

print(matrix.shape)

pos = (2,5)
vision_range = 10

for y in range(pos[0]-vision_range,pos[0]+vision_range+1):
    print(y)