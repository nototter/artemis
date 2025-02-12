import random
from core.plugin import BasePwnhyvePlugin
from core.pil_simplify import tinyPillow

class Plugin(BasePwnhyvePlugin):
    def snake(tpil:tinyPillow):
        global dirChange

        def drawPixel2(xy):
            # draw pixels in a 64x32 grid instead of 128x64
            xAxis, yAxis = xy[0]*2, xy[1]*2
            tpil.rect((xAxis, yAxis), (xAxis+1, yAxis+1))

        def moveSnake(snakePos):
            global dirChange

            newSnakePos = []

            for coordPlane in snakePos:
                for dirChange in dirChanges.copy():
                    if [coordPlane[0], coordPlane[1]] == dirChange[0]: # if snake body pixel reaches a direction change
                        coordPlane[2] = dirChange[1] # then change that pixel's direction

                match coordPlane[2]: # coordPlane[2] is the direction of the pixel
                    case "up":
                        coordPlane[1] -= 1 # move Y-1
                    case "down":
                        coordPlane[1] += 1 # move Y+1
                    case "right":
                        coordPlane[0] += 1 # move X+1
                    case "left":
                        coordPlane[0] -= 1 # move X-1

                newSnakePos.append(coordPlane) # append new, changed coordinate to the new snake body

            return newSnakePos

        def snakeDirection(dir):
            global dirChange
            dirChanges.append([snakePos[-1][:2], dir]) # add turn pixel and direction


        def died():
            pass

        dirChanges = [] # when snake body pixel reaches a pixel in here, the body will turn to the alotted direction
        snakePos = [[x, 16, "right"] for x in range(36, 42)]
        applePos = [48, 16]
        popNext = False
        applesAte = 0
        speed = 0.25

        def checkDir(dir):
            # make sure snake doesn't do a 180 into itself
            head = snakePos[-1]

            if head[2] == "right":
                return dir != "left"
            elif head[2] == "left":
                return dir != "right"
            elif head[2] == "up":
                return dir != "down"
            elif head[2] == "down":
                return dir != "up"

        while True:
            # drawing
            tpil.clear()

            drawPixel2(applePos)

            for XYCoord in snakePos:
                drawPixel2(XYCoord)

            tpil.text([4, 52], "Score: {}".format(applesAte),fontSize=16)
            tpil.show()

            # user key management
            key = tpil.waitWhileChkKey(speed)

            if key == "up":
                if checkDir("up"): snakeDirection("up")
            elif key == "right":
                if checkDir("right"): snakeDirection("right")
            elif key == "left":
                if checkDir("left"): snakeDirection("left")
            elif key == "down":
                if checkDir("down"):snakeDirection("down")

            # handle snake tail movement
            snakeTail = snakePos[0]
            print('Tail: {}'.format([snakeTail[0], snakeTail[1]]))
            try:
                if [snakeTail[0], snakeTail[1]] == dirChanges[0][0]:
                    # if the last direction change is not applicable to the snake anymore (e.g snake body finished the turn)
                    # then remove that direction change to prevent random movements on that same pixel
                    popNext = True
            except:
                pass

            headCoordinate = [snakePos[-1][0], snakePos[-1][1]]

            # if head is on an apple, the snake ate it - increase score by 1
            if headCoordinate == applePos:
                applesAte += 1
                speed -= 0.005 if speed >= 0.01 else 0.001
                applePos = [random.randint(2,62), random.randint(2,24)]

            # make snake die when crashed into wall
            if (headCoordinate[0] >= 64 or headCoordinate[0] == -1) or (headCoordinate[1] >= 32 or headCoordinate[1] == -1):
                died()
                return

            # make snake die when crashed into itself
            if headCoordinate in [[x[0], x[1]] for x in snakePos][:-1]:
                died()
                return

            snakePos = moveSnake(snakePos)
            
            if popNext: # if we need to pop the last direction change
                popNext = not popNext
                dirChanges.pop(0) # then do so