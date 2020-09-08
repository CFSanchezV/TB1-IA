import pygame as pg
import os
import random as rnd
import math
import time

pg.init()

WIN_WIDTH, WIN_HEIGHT = 750, 552
win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pg.font.init()
segoeFONT = pg.font.SysFont("segoeui", 30, True)

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
pygame.transform.scale() documentation
syntax: scale(Surface, (width, height), DestSurface = None) -> Surface
An optional destination surface can be used. Quicker to repeatedly scale something.
'''



#-------------------CLASSES-----------------------
class Bus:
    """
    Bus class
    """
    ANIMATION_TIME = 5

    def __init__(self, x, y):
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
        self.Vvel = 0
        self.jumping = False
        self.height = self.y
        self.img_count = 0
        self.img = bus_images[0]

    def jump(self):
        """
        make the bus jump
        return: None
        """
        if not self.jumping:
            self.jumping = True
            self.Vvel = -8.9
            self.tick_count = 0
            self.height = self.y

    def moveDown(self):
        self.tick_count += 1
        s = self.Vvel*self.tick_count + 1.2*self.tick_count**2

        if s >= 10:
            s = 10
        if s < 0:
            s -= 0.2
        
        #displacement s
        self.y = self.y + s

        #jumpipng
        if s < 0 or self.y < self.height - (self.img.get_height()//2):
            self.y = self.y + s
        else:
            self.y = self.firstY
            self.jumping = False


    def move(self, direction):
        """
        make the bus move left or right
        return: None
        """
        self.tick_count += 1

        if direction == "right" and self.x + self.Hvel < 600 and not self.jumping:                           
            self.x = self.x + self.Hvel
        elif direction == "left" and self.x - self.Hvel > 200 and not self.jumping:
            self.x = self.x - self.Hvel

        
    def draw(self, win):
        """
        param win: pg surface
        return: None
        """
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

        # draw bus
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        """
        gets the mask of current bus image
        return: None
        """
        return pg.mask.from_surface(self.img)


class Kid:
    """
    Kid class
    """
    ANIMATION_TIME = 10

    def __init__(self, x, y):
        """
        param x: starting x pos (int)
        param y: starting y pos (int)
        return: None
        """
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = -3
        self.width = 245 - 90
        self.height = 250 - 90
        self.alive = True
        self.img_count = 0        
        # random img for Kid        
        self.img = rnd.choice(kid_images)
        self.substitute_img = self.img


    def move(self):
        self.tick_count += 1
        # d = self.vel*self.tick_count + 1.5*self.tick_count**2
        # if d >= 16:
        #     d = 16
        
        # if d < 0:
        #     d = 0

        self.y = self.y + self.vel
        if self.y == 300:
            self.vel = 0
            self.alive = False

    def draw(self, win):
        if self.alive:
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
        
        # win.blit(self.img, (self.x + inc, self.y))
        if self.y != 300 and self.alive == True:
            win.blit(self.img, (self.x + inc, self.y))
        

class Adult:
    """
    Adult class
    """
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        param x: starting x pos (int)
        param y: starting y pos (int)
        return: None
        """
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        # random img for Adult        
        self.img = rnd.choice(adult_images)


class BackGround:
    """
    background class
    """    
    IMGS = bg_images
    ANIMATION_TIME = 7

    def __init__(self):
        """        
        return: None
        """
        self.x = 0
        self.y = 0
        self.tick_count = 0
        self.img_count = 0
        self.img = self.IMGS[9]

    def draw(self, win):
        """
        draw the bg scrolling
        param win: pg window or surface
        return: None
        """
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

class DNA:                             # DNA for genetic algorithm
    def __init__(self, genes=None):      # If initialized with a gene already, don't
        self.array = []                  # generate random movement. Else, do.
        self.chain = pg.math.Vector2()   # DNA chain = 2d vector // xy as tuple ( for random acceleration )
        if genes:
            self.array = genes
        else:
            for i in range(moveLimit=20):              # Till the limit frame, generate random movements. rnd.random()*2-1 floats entre 0 y 1
                self.chain.xy = rnd.random()*2-1, rnd.random()*2-1
                self.array.append(self.chain.xy)

    def CrossOver(self, partner):                               # Select a partner from the gene pool,
        newGenes = []                                           # Choose a random point in the DNA chain,
        middle = math.floor(rnd.randrange(len(self.array)))  # Mix two genes and create a new array of motion.
        for i in range(len(self.array)):                        # Create a new DNA, with the gene created.
            if i < middle:
                newGenes.append(partner.array[i])
            else:
                newGenes.append(self.array[i])

        return DNA(newGenes)