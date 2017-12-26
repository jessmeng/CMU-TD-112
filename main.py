####################################
# HACK112
# CMU TD 112
# main
#################################### 

# MAIN DISPLAY

import pygame
import map
import os
from soundFiles import *
from gameObjects import *
from test import *
import copy
import round

# centers the game window on your computer screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# pygamegame.py created by Lukas Peraza
class PygameGame(object):
    
    def init(self):

        self.mode = "start"
        self.gameTime = 0
        self.money = 650
        self.lives = 150
        self.level = 1
        self.bloons = pygame.sprite.Group()
        self.scotties = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.pops = pygame.sprite.Group()
        self.nextEnemies = []
        self.roundActive = False
        self.spawn = 35
        self.levelUp = False

        self.font = pygame.font.SysFont("Berlin Sans FB", 20)
        
        # start screen
        startSprite = pygame.sprite.Sprite()
        startSprite.image = pygame.image.load("assets/startScreen.png")
        startSprite.rect = pygame.Rect(0, 0, self.width, 600)
        self.startScreen = pygame.sprite.Group(startSprite)

        # help screen
        helpSprite = pygame.sprite.Sprite()
        helpSprite.image = pygame.image.load("assets/helpScreen.png")
        helpSprite.rect = pygame.Rect(0, 0, 800, 600)
        self.helpScreen = pygame.sprite.Group(helpSprite)

        # sidebar menu
        sideSprite = pygame.sprite.Sprite()
        sideSprite.image = pygame.image.load("assets/side.png")
        sideSprite.rect = pygame.Rect(600, 0, 800, 600)
        self.sideMenu = pygame.sprite.Group(sideSprite)

        # 0 means none selected; 1,2,3,4 are the scotties in the order they appear
        self.towerSelected = 0
        # row and col of the space last clicked
        self.spaceClicked = (None, None)

        # end screen
        endSprite = pygame.sprite.Sprite()
        endSprite.image = pygame.image.load("assets/endScreen.png")
        endSprite.rect = pygame.Rect(0, 0, 800, 600)
        self.endScreen = pygame.sprite.Group(endSprite)
        
        # win screen
        winSprite = pygame.sprite.Sprite()
        winSprite.image = pygame.image.load("assets/winScreen.png")
        winSprite.rect = pygame.Rect(0, 0, 800, 600)
        self.winScreen = pygame.sprite.Group(winSprite)

        map.Map.init("Map1.png")

        self.board1 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'E', 'O', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'X', 'X', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'X', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'X', 'X', 'O', 'O', 'O'],
                       ['O', 'O', 'X', 'X', 'O', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'O'],
                       ['O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'O'],
                       ['S', 'X', 'X', 'O', 'O', 'X', 'X', 'O', 'O', 'X', 'X', 'X', 'X', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'X', 'X', 'X', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'X', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'X', 'X', 'O', 'O', 'O'],
                       ['O', 'O', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'X', 'X', 'O', 'O'],
                       ['O', 'O', 'X', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'X', 'O', 'O'],
                       ['O', 'O', 'X', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'O', 'O', 'O', 'O'],
                       ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]
        MAP_1 = map.Map(self.board1)
        self.targets = [(6, 2, 0, -1), (4, 2, 1, 0), (4, 3, 0, -1), (3, 3, 1, 0), (3, 5, 0, 1), (4, 5, 1, 0),
                        (4, 6, 0, 1), (6, 6, -1, 0), (6, 5, 0, 1), (10, 5, -1, 0), (10, 3, 0, 1), (11, 3, -1, 0), (11, 2, 0, 1), (13, 2, 1, 0), (13, 4, 0, 1), (14, 4, 1, 0), (14, 11, 0, -1),
                        (13, 11, 1, 0), (13, 13, 0, -1), (11, 13, -1, 0), (11, 12, 0, -1), (10, 12, -1, 0),
                        (10, 11, 0, -1), (9, 11, -1, 0), (9, 8, 0, -1), (7, 8, 1, 0), (7, 9, 0, -1), (6, 9, 1, 0),
                        (6, 12, 0, -1), (3, 12, -1, 0), (3, 11, 0, -1), (3, 10, -1, 0), (3, 10, 0, -1), (0, 10, 0, 0)]

        self.start = (0, 225, 1, 0)
        self.target = []
        for tup in self.targets:
            self.target.append((int(tup[0] * 37.5), int(tup[1] * 37.5 + 17), tup[2], tup[3]))

        self.currMap = MAP_1
        self.map = pygame.sprite.Group(self.currMap)

    def mousePressed(self, x, y):
        if (self.mode == "start"):
            if (x >= 41 and y >= 24 and x <= 171 and y <= 68):
                self.mode = "play"
                buttonPress()
            elif (x >= 41 and y >= 89 and x <= 171 and y <= 133):
                self.mode = "help"
                buttonPress()
        elif (self.mode == "play"):
            # scottie 1 clicked
            if (x >= 611 and y >= 98 and x <= 679 and y <= 169):
                if (self.towerSelected != 1):
                    self.towerSelected = 1
                else:
                    self.towerSelected = 0
                buttonPress()
            # scottie 2 clicked
            elif (x >= 611 and y >= 201 and x <= 679 and y <= 272):
                if (self.towerSelected != 2):
                    self.towerSelected = 2
                else:
                    self.towerSelected = 0
                buttonPress()
            # scottie 3 clicked
            elif (x >= 611 and y >= 302 and x <= 679 and y <= 373):
                if (self.towerSelected != 3):
                    self.towerSelected = 3
                else:
                    self.towerSelected = 0
                buttonPress()
            # scottie 4 clicked
            elif (x >= 611 and y >= 402 and x <= 679 and y <= 474):
                if (self.towerSelected != 4):
                    self.towerSelected = 4
                else:
                    self.towerSelected = 0
                buttonPress()
            elif (x >= 612 and y >= 557 and x <= 689 and y <= 589):
                self.init()
                buttonPress()
            elif (x >= 708 and y >= 557 and x <= 785 and y <= 589):
                self.init()
                self.mode = "play"
                buttonPress()
                self.level, self.money, self.lives, self.scotties = self.temp[0], self.temp[1], self.temp[2], self.temp[3]
            elif (x >= 0 and y >= 0 and x <= 600 and y <= 600):
                row, col = int(y // 37.5), int(x // 37.5)
                if (self.towerSelected != 0):
                    if (self.towerSelected == 1 and self.money >= 200):
                        x, y = pygame.mouse.get_pos()
                        scot = DartScottie(x, y)
                        self.scotties.add(scot)
                        self.money -= scot.value
                        self.towerSelected = 0
                        buttonPress()
                    elif (self.towerSelected == 2 and self.money >= 400):
                        x, y = pygame.mouse.get_pos()
                        scot = BoomerangScottie(x, y)
                        self.scotties.add(scot)
                        self.money -= scot.value
                        self.towerSelected = 0
                        buttonPress()
                    elif (self.towerSelected == 3 and self.money >= 500):
                        x, y = pygame.mouse.get_pos()
                        scot = NinjaScottie(x, y)
                        self.scotties.add(scot)
                        self.money -= scot.value
                        self.towerSelected = 0
                        buttonPress()
                    elif (self.towerSelected == 4 and self.money >= 2500):
                        x, y = pygame.mouse.get_pos()
                        scot = SuperScottie(x, y)
                        self.scotties.add(scot)
                        self.money -= scot.value
                        self.towerSelected = 0
                        buttonPress()
        elif (self.mode == "help"):
            if (x >= 37 and y >= 23 and x <= 163 and y <= 74):
                self.mode = "start"
                buttonPress()
            elif (x >= 641 and y >= 23 and x <= 767 and y <= 74):
                self.mode = "play"
                buttonPress()
        elif (self.mode == "gameOver"):
            if (x >= 22 and y >= 13 and x <= 211 and y <= 63):
                self.init()
                buttonPress()
        elif (self.mode == "woke"):
            if (x >= 19 and y >= 9 and x <= 209 and y <= 60):
                self.init()
                buttonPress()

    '''def printList(self, l):
        for row in l:
            print(row)'''

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_SPACE:
            self.nextEnemies = round.getBloonsList(self.level)
            self.roundActive = True
            self.temp = (self.level, self.money, self.lives, self.scotties)
            #print(self.nextEnemies)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        # continueMusic()
        if self.lives == 0: self.mode = 'gameOver'
        self.gameTime += 1
        self.bullets.update(self.width, self.height)
        self.dartCollision()
        self.swivel()
        self.inRange()
        self.swivel()
        self.updateProjectiles()
        self.moveBloons()
        if self.gameTime % self.spawn == 0 and self.roundActive:
            self.spawnBloons()
        if self.gameTime % 10 == 0:
           self.attack()
        if self.gameTime % 5 == 0:
            self.pops.remove(self.pops.sprites())
        if self.gameTime % 50 == 0 and self.levelUp:
            self.levelUp = False
        if self.level > 20:
            self.mode = "woke"

    def redrawAll(self, screen):
        if (self.mode == "start"):
            self.startScreen.draw(screen)
        elif (self.mode == "play"):
            self.map.draw(screen)
            self.sideMenu.draw(screen)
            moneyLabel = self.font.render(str(self.money), 1, (0, 0, 0))
            screen.blit(moneyLabel, (670, 13))
            livesLabel = self.font.render(str(self.lives), 1, (0, 0, 0))
            screen.blit(livesLabel, (654, 30))
            levelLabel = self.font.render(str(self.level), 1, (0, 0, 0))
            screen.blit(levelLabel, (654, 46))
            # for row in range(len(self.currMap.board)):
            #     for col in range(len(self.currMap.board[row])):
            #         if (self.currMap.board[row][col] not in 'XSEO'):
            #             dogSprite = pygame.sprite.Sprite()
            #             if (self.currMap.board[row][col] == '1'):
            #                 dogSprite.image = pygame.image.load(os.path.join("Assets", "doggy1.png"))
            #             elif (self.currMap.board[row][col] == '2'):
            #                 dogSprite.image = pygame.image.load(os.path.join("Assets", "doggy2.png"))
            #             elif (self.currMap.board[row][col] == '3'):
            #                 dogSprite.image = pygame.image.load(os.path.join("Assets", "doggy3.png"))
            #             elif (self.currMap.board[row][col] == '4'):
            #                 dogSprite.image = pygame.image.load(os.path.join("Assets", "doggy4.png"))
            #             dogSprite.rect = pygame.Rect(int(col * 37.5), int(row * 37.5) + 2, int(col * 37.5 + 37.5),
            #                                          int(row * 37.5 + 37.5))
            #             doggy = pygame.sprite.Group(dogSprite)
            #             doggy.draw(screen)
            self.bullets.draw(screen)
            self.scotties.draw(screen)
            self.bloons.draw(screen)
            self.pops.draw(screen)
            if not self.roundActive and self.level > 1 and len(self.bloons) == 0 and self.levelUp:
                roundSprite = pygame.sprite.Sprite()
                roundSprite.image = pygame.image.load("assets/levelUp.png")
                roundSprite.rect = pygame.Rect(150, 175, 450, 225)
                roundScreen = pygame.sprite.Group(roundSprite)
                roundScreen.draw(screen)
        elif (self.mode == "help"):
            self.helpScreen.draw(screen)
        elif (self.mode == "gameOver"):
            self.endScreen.draw(screen)
        elif (self.mode == "woke"):
            self.winScreen.draw(screen)

    def isKeyPressed(self, key):
        #return whether a specific key is being held
        return self._keys.get(key, False)

    def moveBloons(self):
        for bloon in self.bloons:
            x, y = bloon.x, bloon.y
            dx, dy = bloon.velocity
            if len(bloon.targets) == 0:
                self.lives -= bloon.health
                bloon.kill()
                return

            y1, x1, deltaX, deltaY = bloon.targets[0]
            if x1 - 10 < x < x1 + 10 and dy == 0:
                bloon.x = x1
                bloon.velocity = (deltaX*bloon.speed, deltaY*bloon.speed)
                bloon.targets.pop(0)
            elif y1 -10 < y < y1 + 10 and dx == 0:
                bloon.y = y1
                bloon.velocity = (deltaX*bloon.speed, deltaY*bloon.speed)
                bloon.targets.pop(0)
            bloon.update()

    def spawnBloons(self):
        if len(self.nextEnemies) != 0:
            bloon = self.nextEnemies.pop(0)
            bloon.targets = copy.deepcopy(self.target)
            self.bloons.add(bloon)
        if len(self.bloons) == 0:
            self.money += 100
            self.roundActive = False
            self.level += 1
            self.levelUp = True

    def dartCollision(self):
        for dart in self.bullets:
            for bloon in self.bloons:
                if pygame.sprite.collide_circle(dart,bloon):
                    dart.hit(1)
                    pop = Pop(bloon.x, bloon.y)
                    pop.updateRect()
                    self.pops.add(pop)
                    bloon.hit(1)
                    balloonPop()
                    self.money += 1

    def getClosestBloon(self, scottie):
        x, y = scottie.x, scottie.y
        smallestDistance = 600
        targetBloon = None
        bloons = self.bloons.sprites()
        if bloons == []: return None
        for bloon in bloons:
            x2, y2 = bloon.x, bloon.y
            dist = self.getDistance(x,y,x2,y2)
            if dist == None or dist < smallestDistance and dist < scottie.range:
                smallestDistance = dist
                targetBloon = bloon
        return targetBloon

    def updateProjectiles(self):
        for dart in self.bullets:
            dart.update()
            if not 0 < dart.x < 800:
                dart.kill()
            if not 0 < dart.y < 600:
                dart.kill()

    def inRange(self):
        for scottie in self.scotties:
            x, y = scottie.x, scottie.y
            curBloon = self.getClosestBloon(scottie)
            if curBloon == None: break
            x2, y2 = curBloon.x, curBloon.y
            dist = self.getDistance(x,y,x2,y2)
            # print(dist)
            if self.getDistance(x,y,x2,y2) < scottie.range:
                scottie.angle = self.get_angle(x, y, scottie)

    def swivel(self):
        for scot in self.scotties:
            scot.update()

    def get_angle(self, x, y, scottie):
        x1, y1 = x, y
        bloon = self.getClosestBloon(scottie)
        x2, y2 = bloon.x, bloon.y
        return  - (math.atan2(y2 - y1, x2 - x1)) / (math.pi / 180)

    def attack(self):
        for scottie in self.scotties:
            if not self.getClosestBloon(scottie) == None:
                self.bullets.add(Bullet(scottie.x, scottie.y, scottie.angle, scottie.power[1]))
                #print(len(self.bloons.sprites()))

    def getDistance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
    def __init__(self, width=800, height=600, fps=60, title="CMU TD 112"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        playMusic()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()

def main():
    game = PygameGame()
    game.run()


if __name__ == '__main__':
    main()