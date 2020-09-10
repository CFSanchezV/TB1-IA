import pygame as pg
import os
import random as rnd
import math
import time

#---------------INIT--------------------...#
pg.init()
WIN_WIDTH, WIN_HEIGHT = 750, 552
win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.font.init()
segoeFONT = pg.font.SysFont("segoeui", 25, True)

#--------------IMAGES---------------------# 

bus_images = [pg.transform.scale(pg.image.load(os.path.join("images", "bus" + str(x) + ".png")).convert_alpha(), (118, 126)) for x in range(1, 4)]
bg_images = [pg.transform.scale(pg.image.load(os.path.join("images", "Aroad" + str(i) + ".png")).convert_alpha(), (750, 552)) for i in range(1, 11)]

#imgs from spritesheets
adult_images = []
adults_sheet = pg.image.load("images/adults73x145.png").convert_alpha()
for i in range(0, 435, 145):
    for j in range(0, 438, 73):
        adult_img = adults_sheet.subsurface((j, i, 73, 145))
        adult_images.append(adult_img)

kid_images = []
kids_sheet = pg.image.load("images/kids245x250.png").convert_alpha()
for i in range(0, 750, 250):
    for j in range(0, 735, 245):
        kid_img = kids_sheet.subsurface((j, i, 245, 250))
        kid_img = pg.transform.scale(kid_img, (kid_img.get_width()-90, kid_img.get_height()-90))
        kid_images.append(kid_img)

'''
pygame.transform.scale() || syntax: scale(Surface, (width, height), DestSurface = None) -> Surface
'''

def Remap(aliveTime, frameLimit):  # Return 1 if best, returns 0 if worst
    return 1 + (aliveTime - 0) * (0 - 1) / frameLimit

#-------------------GA VARIABLES-----------------------
busCount = 50         # Amount of buses for each generation
aliveBusCount = busCount  # Currently alive buses
frameLimit = 1000       # Max frames to play


#-------------------CLASSES-----------------------
class DNA:                               # DNA for GA
    def __init__(self, genes=None):      
        self.array = []                  # generate random movement or copy genes
        self.chain = pg.math.Vector2()   # DNA "chain", a 2d vector // xy as tuple () for random movement )
        if genes:
            self.array = genes
        else:
            for _ in range(frameLimit):  # Generate random sideway movement until the limit frame. rnd.random()*2-1 floats entre 0 y 1
                self.chain.xy = rnd.random()*2-1, 0
                self.array.append(self.chain.xy)

    def CrossOver(self, partner):                               # Select a partner from the gene pool,
        newGenes = []                                           # Choose a random point in the DNA chain,
        division = math.floor(rnd.randrange(len(self.array)))  # Mix two genes and create a new array of motion.
        for i in range(len(self.array)):                        # Create a new DNA, with the gene created.
            if i < division:
                newGenes.append(partner.array[i])
            else:
                newGenes.append(self.array[i])

        return DNA(newGenes)

class Bus:
    """ Bus class """
    ANIMATION_TIME = 5

    def __init__(self, x, y, dna=None):
        """
        param x: starting x pos (int)
        param y: starting y pos (int)
        return: None
        """
        self.x = x        
        self.y = y
        self.firstY = y
        self.tick_count = 0
        self.Hvel = 90
        self.img_count = 0
        self.img = bus_images[0]
        #jump
        self.Vvel = 0
        self.jumping = False
        self.height = self.y        
        #collision
        self.hitbox = (self.x, self.y, self.img.get_width(), self.img.get_height()-6)

        #GA
        self.alive = True
        self.crashed = False
        self.won = False
        self.fitness = 0        
        self.aliveTime = 0
        if dna:
            self.gene = DNA(dna)
        else:
            self.gene = DNA()

    def jump(self):
        """ make the bus jump """
        if not self.jumping:
            self.jumping = True
            self.Vvel = -4.7
            self.tick_count = 0
            self.height = self.y

    def moveDown(self):
        self.tick_count += 1
        s = self.Vvel*self.tick_count + 0.5*self.tick_count**2

        if s >= 6:
            s = 6
        if s < 0:
            s -= 1.5
        
        #displacement s
        self.y = self.y + s

        #jumpipng
        if s < 0 or self.y < self.height - (self.img.get_height()//2):
            self.y = self.y + s
        else:
            self.y = self.firstY
            self.jumping = False

        #tick time
        if self.alive:
            self.aliveTime += 1

    def move(self, direction):
        """ move bus left or right """
        self.tick_count += 1

        if direction == "right" and self.x + self.Hvel < 600 and not self.jumping:                           
            self.x = self.x + self.Hvel
        elif direction == "left" and self.x - self.Hvel > 200 and not self.jumping:
            self.x = self.x - self.Hvel
        
    def draw(self, win):
        """ param win: pg surface """
        self.img_count += 1

        # Loop through three images to 'animate'
        if self.img_count <= self.ANIMATION_TIME:
            self.img = bus_images[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = bus_images[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = bus_images[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = bus_images[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = bus_images[0]
            self.img_count = 0

        # collision
        self.hitbox = (self.x, self.y, self.img.get_width(), self.img.get_height()-6)
        # pg.draw.rect(win, pg.Color("red"), self.hitbox, 2)
        
        win.blit(self.img, (self.x, self.y))

    def checkCollision(self, collided):
        global aliveBusCount
        
        if collided:
            self.crashed = True

        if self.crashed:
            self.alive = False
            aliveBusCount -= 1

    def CalculateFitness(self):  # The longer it lives, the better its fitness is.
        global frameLimit
        # Fitness set between 0 and 1
        self.fitness = Remap(self.aliveTime, frameLimit)

    def Update(self, frameCount):   # Update / move the object every other frame.
        global frameLimit
        x_disp = self.gene.array[frameCount].x
        
        if self.alive and (frameCount%20 == 0):
            if x_disp > 0:
                self.move("right")
            elif x_disp < 0:
                self.move("right")
            

class Kid:
    """ Kid class  """
    ANIMATION_TIME = 10

    def __init__(self, x, y):
        """
        param x: starting x pos (int)
        param y: starting y pos (int)
        """
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = -3
        self.width = 245 - 110
        self.height = 250 - 110
        self.alive = True
        self.img_count = 0        
        # random img for Kid        
        self.img = rnd.choice(kid_images)
        self.substitute_img = self.img

        #collision        
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.passed = False

    def move(self):
        self.tick_count += 1

        self.y = self.y + self.vel
        if self.y == 300 and self.alive:
            self.vel = 0
            self.passed = True

    def draw(self, win):
        if self.alive and self.passed == False:
            self.img_count += 1
            inc = 0            
            
            if self.img_count < self.ANIMATION_TIME*2:
                self.img = pg.transform.scale(self.substitute_img, (self.width-20, self.height-20))
                inc += 20//2
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = pg.transform.scale(self.substitute_img, (self.width-30, self.height-30))
                inc += 30//2
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = pg.transform.scale(self.substitute_img, (self.width-40, self.height-40))
                inc += 40//2
            elif self.img_count < self.ANIMATION_TIME*5:
                self.img = pg.transform.scale(self.substitute_img, (self.width-50, self.height-50))
                inc += 50//2
            elif self.img_count < self.ANIMATION_TIME*6:
                self.img = pg.transform.scale(self.substitute_img, (self.width-60, self.height-60))
                inc += 60//2
            elif self.img_count < self.ANIMATION_TIME*7:
                self.img = pg.transform.scale(self.substitute_img, (self.width-70, self.height-70))
                inc += 70//2
            elif self.img_count < self.ANIMATION_TIME*8:
                self.img = pg.transform.scale(self.substitute_img, (self.width-80, self.height-80))
                inc += 80//2
            elif self.img_count < self.ANIMATION_TIME*9 + 1:
                self.img_count = 0                
                inc += 90//2
        
            # collision
            self.hitbox = (self.x + inc, self.y, self.img.get_width(), self.img.get_height())
            # pg.draw.rect(win, pg.Color("blue"), self.hitbox, 2)

        # win.blit(self.img, (self.x + inc, self.y))
        if self.y != 300 and self.alive == True:
            win.blit(self.img, (self.x + inc, self.y))

    def collide(self, bus):
        ''' hitbox collisions w/ "centers"+a bit, and bus bottom '''
        if self.alive and not self.passed:
            if ((self.hitbox[0] + self.hitbox[2]//2) > bus.hitbox[0]) and (self.hitbox[0] + self.hitbox[2]//2) < (bus.hitbox[0] + bus.hitbox[2]):
                if (self.hitbox[1] + self.hitbox[3]//1.4) < bus.hitbox[1] + bus.hitbox[3] and (self.hitbox[1] + self.hitbox[3]//1.4) >= (bus.hitbox[1] + bus.hitbox[3]) - 6:
                    return True

        return False

class Adult:
    """ Adult class  """
    ANIMATION_TIME = 10

    def __init__(self, x, y):
        """ param x: starting x pos (int) ||  param y: starting y pos (int) """
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = -3
        self.width = 73
        self.height = 145
        self.alive = True
        self.img_count = 0        
        # random img for Kid        
        self.img = rnd.choice(adult_images)
        self.substitute_img = self.img

        #collision
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.passed = False

    def move(self):
        self.tick_count += 1

        self.y = self.y + self.vel
        if self.y == 300 and self.alive:
            self.vel = 0
            self.passed = True

    def draw(self, win):
        if self.alive and self.passed == False:
            self.img_count += 1
            inc = 0            
            
            if self.img_count < self.ANIMATION_TIME*2:
                self.img = pg.transform.scale(self.substitute_img, (self.width-5, self.height-10))
                inc += 5//2
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = pg.transform.scale(self.substitute_img, (self.width-10, self.height-20))
                inc += 10//2
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = pg.transform.scale(self.substitute_img, (self.width-15, self.height-30))
                inc += 15//2
            elif self.img_count < self.ANIMATION_TIME*5:
                self.img = pg.transform.scale(self.substitute_img, (self.width-20, self.height-40))
                inc += 20//2
            elif self.img_count < self.ANIMATION_TIME*6:
                self.img = pg.transform.scale(self.substitute_img, (self.width-25, self.height-50))
                inc += 25//2
            elif self.img_count < self.ANIMATION_TIME*7:
                self.img = pg.transform.scale(self.substitute_img, (self.width-30, self.height-60))
                inc += 30//2
            elif self.img_count < self.ANIMATION_TIME*8:
                self.img = pg.transform.scale(self.substitute_img, (self.width-35, self.height-70))
                inc += 35//2
            elif self.img_count < self.ANIMATION_TIME*9 + 1:
                self.img_count = 0                
                inc += 40//2
        
            # collision
            self.hitbox = (self.x + inc, self.y, self.img.get_width(), self.img.get_height())
            # pg.draw.rect(win, pg.Color("yellow"), self.hitbox, 2)

        # win.blit(self.img, (self.x + inc, self.y))
        if self.y != 300 and self.alive == True:
            win.blit(self.img, (self.x + inc, self.y))

    def collide(self, bus):
        ''' hitbox collisions w/ "centers"+a bit, and bus bottom '''
        if self.alive and not self.passed:
            if ((self.hitbox[0] + self.hitbox[2]//2) > bus.hitbox[0]) and (self.hitbox[0] + self.hitbox[2]//2) < (bus.hitbox[0] + bus.hitbox[2]):
                if (self.hitbox[1] + self.hitbox[3]//1.5) <= bus.hitbox[1] + bus.hitbox[3] and (self.hitbox[1] + self.hitbox[3]//1.5) >= (bus.hitbox[1] + bus.hitbox[3]) - 6:
                    return True
        
        return False

class BackGround:
    """ background class """
    IMGS = bg_images
    ANIMATION_TIME = 7

    def __init__(self):        
        self.x = 0
        self.y = 0
        self.tick_count = 0
        self.img_count = 0
        self.img = self.IMGS[9]

    def draw(self, win):
        """ draw the bg scrolling """
        self.img_count += 1

        # Loop through 10 images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[9]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[8]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[7]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[6]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[5]
        elif self.img_count <= self.ANIMATION_TIME*5:
            self.img = self.IMGS[4]
        elif self.img_count <= self.ANIMATION_TIME*6:
            self.img = self.IMGS[3]
        elif self.img_count <= self.ANIMATION_TIME*7:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*8:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*9:
            self.img = self.IMGS[0]
        elif self.img_count == self.ANIMATION_TIME*9 + 1:
            self.img = self.IMGS[9]
            self.img_count = 0

        win.blit(self.img, (self.x, self.y))







