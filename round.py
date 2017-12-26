####################################
# HACK112
# CMU TD 112
# round
#################################### 

import gameObjects
import string

round = open('Assets/round1.txt', 'r')
lines = round.readline().split(';')
layer = int(lines[0])
count = int(lines[1])

bloonRounds = []
for i in range (count):
    bloon = gameObjects.Bloons(cx=0, cy=225)
    bloonRounds.append(bloon)

def getBloonsList(round):
    count, layer = 0, 0
    bloonRounds = []
    path = 'Assets/round%d.txt' % (round)
    input = open(path , 'r')
    lines = input.read()
    for line in lines.splitlines():
        data = line.split(';')
        layer = int(data[0])
        count = int(data[1])
        for i in range(count):
            bloon = gameObjects.Bloons(layer=layer, cx=0, cy=225)
            bloonRounds.append(bloon)
    return bloonRounds