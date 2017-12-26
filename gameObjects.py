import pygame
import math
import os


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 90

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth=800, screenHeight=600):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth or self.rect.right < 0 or self.rect.top > screenHeight or self.rect.bottom < 0:
            self.kill()

class Scottie(GameObject):

    ScottieImages = []
    images = ['assets/doggy1.png', 'assets/doggy2.png', 'assets/doggy3.png', 'assets/doggy4.png']
    for i in range(len(images)):
        ScottieImages.append(pygame.image.load(images[i]))

    def __init__(self, cx=300, cy=300, img=0):
        super(Scottie, self).__init__(cx, cy, Scottie.ScottieImages[img], 50)
        w, h = self.image.get_size()
        self.x, self.y = cx, cy
        self.rect = pygame.Rect(self.x - w/2, self.y - h/2,w, h)
        self.power = (1, 100) # Popping power and Velocity
        self.range = 125


class DartScottie(Scottie):
    def __init__(self, cx, cy):
        super(DartScottie, self).__init__(cx, cy)
        self.value = 200

class BoomerangScottie(Scottie):
    def __init__(self, cx, cy):
        super(BoomerangScottie, self).__init__(cx, cy, img=1)
        self.power = (1, 160)
        self.range = 150
        self.value = 400

class NinjaScottie(Scottie):
    def __init__(self, cx, cy):
        super(NinjaScottie, self).__init__(cx, cy, img=2)
        self.power = (2,160) # Popping power and Velocity of projectile
        self.range = 175
        self.value = 500

class SuperScottie(Scottie):
    def __init__(self, cx, cy):
        super(SuperScottie,self).__init__(cx, cy, img=3)
        self.power = (1, 220)
        self.range = 250
        self.value = 2500

class Bloons(GameObject):

    layers = [ # Name| Health | Speed | Cash Prize
        ('assets/CaseWestern.png', 1, 2.5, 1),
        ('assets/Princeton.png', 2, 2.5, 2),
        ('assets/Harvard.png', 3, 4, 3),
        ('assets/MIT.png',   4, 5, 4),
        ('assets/Stanford.png', 5, 7, 5),]

    # @staticmethod
    # def init():
    #     Bloons.bloonImage = pygame.image.load('sample.jpg')

    def __init__(self, target=None, cx=0, cy=0, layer=4):
      pygame.sprite.Sprite.__init__(self)
      self.layer = layer
      self.setLayer()
      w, h = self.image.get_size()
      self.x, self.y = cx, cy
      self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
      self.speed = 2
      self.baseImage = self.image.copy()
      self.angle = 0
      self.RBE = 1
      self.radius = 15
      self.velocity = (self.speed, 0)
      self.targets = target

    def setLayer(self):
        self.name, self.health, self.speed, self.Value = Bloons.layers[self.layer]
        self.loadImage()

    def nextlayer(self):
        self.layer -= 1
        self.setLayer()

    def loadImage(self):
        self.image = pygame.image.load(self.name)
        self.baseImage = pygame.image.load(self.name)

    def hit(self,damage):
        self.health -= damage
        if self.health<=0:
            self.nextlayer() if self.layer>0 else self.kill()


'''class CWBloon(Bloons):
    # equivalent of a red bloon
    def __init__(self):
        super(CWBloon, self).__init__()

class PrincetonBloon(Bloons):
    # equivalent of a blue bloon
    def __init__(self):
        super(PrincetonBloon, self).__init__()
        self.speed = 14
        self.RBE = 2

    def spawn(self):
        if self.RBE == 1:
            pass  # remove prince bloon; add case

class HarvardBloon(Bloons):
    # equivalent of a green bloon
    def __init__(self):
        super(HarvardBloon, self).__init__()
        self.speed = 18
        self.RBE = 3

    def spawn(self):
        if self.RBE == 2:
            pass  # remove harvard bloon; add prince
        elif self.RBE == 1:
            pass # remove harvard bloon; add case

class MITBloon(Bloons):
    # equivalent of a yellow bloon
    def __init__(self):
        super(MITBloon, self).__init__()
        self.speed = 22
        self.RBE = 4

    def spawn(self):
        if self.RBE == 3:
            pass # remove MIT bloon; add harvard
        elif self.RBE == 2:
            pass  # remove harvard bloon; add prince
        elif self.RBE == 1:
            pass # remove harvard bloon; add case

class StanfordBloon(Bloons):
    # equivalent of a pink bloon
    def __init__(self):
        super(StanfordBloon, self).__init__()
        self.speed = 26
        self.RBE = 5

    def spawn(self):
        if self.RBE == 4:
            pass # remove Stanford bloon; add MIT
        if self.RBE == 3:
            pass # remove Stanford bloon; add harvard
        elif self.RBE == 2:
            pass  # remove Stanford bloon; add prince
        elif self.RBE == 1:
            pass # remove Stanford bloon; add case

'''

class Pop(GameObject):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/BloonPop.png')

class Bullet(GameObject):
    time = 5 # lasts 1 second
    size = 10

    def __init__(self, x, y, angle, speed):
        size = Bullet.size
        self.health = 1
        self.speed = speed
        image = pygame.Surface((Bullet.size, Bullet.size), pygame.SRCALPHA)
        image = pygame.image.load("assets/dart.png")
        # pygame.draw.circle(image, (255, 0, 255), (size // 2, size // 2), size // 2)
        super(Bullet, self).__init__(x, y, image, size // 2)
        vx = self.speed * math.cos(math.radians(angle))
        vy = -self.speed * math.sin(math.radians(angle))
        self.radius = 10
        self.velocity = vx, vy
        self.timeOnScreen = 0

    def update(self, screenWidth=800, screenHeight=600):
        super(Bullet, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1
        if self.timeOnScreen > Bullet.time:
            self.kill()
        if not 0 < self. x < screenWidth:
            self.kill()
        if not 0 < self. y < screenHeight:
            self.kill()

    def hit(self,damage):
        self.health -= damage
        if self.health<=0:
            self.kill()
