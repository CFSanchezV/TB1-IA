from gameClasses import Bus, BackGround, Kid, DNA
import random as rnd
import time
import sys

pg.font.init()  # init font

WIN_WIDTH, WIN_HEIGHT = 750, 552                          # Setting up
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Crazy AI Bus")                      # screen
clock = pg.time.Clock()     # Clock object to control
FPS = 30                 # the Fps
defaultFont = pg.font.SysFont(None, 40)     # Default font of the program
rnd.seed(rnd.randrange(50000000))     # Setting the random seed to a random value
moveLimit = 300         # Frame limit for free movement of smart boxes
boxCount = 200          # Amount of smart boxes for each generation
generationCount = 0
frameCount = 0          # To count the frames until the moveLimit
levelCount = 1
successCount = 0        # Counting the successful smart boxes
avgFitness = 0          # Average fitness ( score from 0 to 1 ) of-
avgFitnessD = 0         # -the last generation, and the difference-
lowestTime = 0          # -between the last and current generation-
lowestTimeD = 0         # -same with lowest time. Record holder (fastest smart box) form the last gen
aliveBoxCount = boxCount    # Currently alive boxes
successCountD = 0           # Difference of this gen's successful boxes and the last one.
levelColor = [rnd.randrange(150) + 100, rnd.randrange(150) + 100, rnd.randrange(150) + 100]    # Randomly
finished = False       # Boolean for deciding when the generation is finished                           # Generated
walls = []             # List for obstacles                                                             # Level color

genePool = []          # Necessary for genetic algorithm, best boxes have more place in this gene pool. (mating pool)


# Running game
running = True
def main():  
    while(running):
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:       # close the screen and exit the program.
                pg.quit()
                sys.exit()