####################################
# HACK112
# CMU TD 112
# test
#################################### 

from subprocess import Popen
import pygame
import map
import os
from soundFiles import *
from gameObjects import *
from main import *
import copy
import round

# centers the game window on your computer screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# pygamegame.py created by Lukas Peraza
class newGame(object):
    
    def __init__(self):
        pass
    
    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_SPACE:
            pass


    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        pass
        
    def __init__(self, width=1000, height=600, fps=50, title="TPBA"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def redrawAll(self, screen):
        pass

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        #self.init()
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
    newGame().run()
    PygameGame().run()
    
if __name__ == '__main__':
    main()