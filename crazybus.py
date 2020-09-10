#imports
import sys
from gameClasses import *

pg.display.set_caption("AI Bus")
clock = pg.time.Clock()     # Clock object to control time
FPS = 30                 # the Fps
defaultFont = pg.font.SysFont(None, 40)     # Default font of the program


#----------------GEN ALG-----------------------#
rnd.seed(rnd.randrange(50302010))     # random seed set to random value
generationCount = 0
frameCount = 0        # Count the frames until the frameLimit
successCount = 0      # Counting the successful buses
avgFitness = 0        # Average fitness ( score from 0 to 1 ) of-
avgFitnessD = 0       # -the last generation, and the difference-
longestTime = 0       # -between the last and current generation-
longestTimeD = 0      # -same with longest time. Record holder (longest alive bus) form the last gen
successCountD = 0     # Difference of this gen's successful buses and the last one.
finished = False      # Boolean for deciding when the generation is finished

genePool = []          # Best buses have more place in this gene pool. (the mating pool)

#------------------AUX functions--------------------#

def validbusX(): # Random valid x for bus spawn
    validX = [255, 255+90, 255+180, 255+270]
    return rnd.choice(validX)

def randVictim(x, y):   # random Victim
    num = rnd.random()
    if num >= 0.5:
        return Adult(x+30, y)
    else:
        return Kid(x, y)

def ShowText(win, string, x, y, size = 40, color=(255, 255, 255)):   # show text on screen
    # segoeFONT = pg.font.SysFont("segoeui", size, True)
    win.blit(segoeFONT.render(string, True, color), (x, y))

def draw_window(win, bg, buses, victims, score):  # Quick 'draw it all' method, order matters
    bg.draw(win)            
    the_score = segoeFONT.render("Score:" + str(score), True, pg.Color("white"))
    win.blit(the_score, (WIN_WIDTH - 10 - the_score.get_width(), 10))
    
    for bus in buses:
        bus.draw(win)

    for vic in victims:
        vic.draw(win)
    
    pg.display.update()


# List to hold the buses.
buses = [Bus(validbusX(), 290)]
#------------------Running game-------------------#
playing = True
def main():
    global frameCount, finished    
    bg = BackGround()
    # debuggin.. Kid(350, 480)
    victims = [Adult(350+30, 480)]
    # win display, clock must be init
    score = 0        

    # x += 90 to switch lane -> bus = Bus(255+90, 290)    
    while playing:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:       # close the screen and exit the program.
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    bus.move("left")
                if event.key == pg.K_RIGHT:
                    bus.move("right")
                if event.key == pg.K_UP:
                    bus.jump()

        add_vic = False
        collided = False
        rem = []        
        for vic in victims:
            for i, bus in enumerate(buses):
                if vic.collide(buses[i]):
                    vic.alive = False                
                    collided = True
                    #trigger_next_flag
                    add_vic = True

                if vic.passed:
                    rem.append(vic)
                    add_vic = True
                    vic.passed = False

            vic.move()
            
        if add_vic:
            if not collided:
                score += 1
            victims.append(randVictim(350, 480))
        
        for r in rem:
            victims.remove(r)

        for i, bus in enumerate(buses):
            if buses[i].checkCollision(victims):
                bus.crashed = True

            bus.moveDown()
        
        draw_window(win, bg, buses, victims, score)
        
        # If frameCount > limit, or no buses left -> generation is finished.
        if (frameCount >= frameLimit-1) or aliveBusCount <= 0:        
            frameCount = frameLimit-1                                                    
            finished = True                                                             
        else:                                                                           
            frameCount += 1     # Update frameCount every frame.

        if finished:
            FinishGeneration()  # Start the resetting process.

    pg.quit()
    quit()

main()

# TODO TEST FINISH FUNCTION
def FinishGeneration():     # A function for resetting process.

    global finished, avgFitness, frameLimit, successCount             # Getting all the global variables.
    global generationCount, frameCount, longestTime, avgFitnessD
    global longestTimeD, successCountD, aliveBusCount

    tempLongestTime = longestTime         # Setting up some values.
    tempAvgFitness = avgFitness
    tempSuccessCount = successCount
    genePool.clear()
    maxFit = 0
    longestTime = 0

    longestIndex = 0
    successCount = 0
    avgFitnessSum = 0
    maxFitIndex = 0

    for bus in buses:
        bus.CalculateFitness()
        avgFitnessSum += bus.fitness
        if bus.fitness >= 1.0:
            successCount += 1
        if bus.fitness > maxFit:
            maxFit = bus.fitness
            maxFitIndex = buses.index(bus)
            
    successCountD = successCount - tempSuccessCount
    avgFitness = avgFitnessSum / len(buses)
    avgFitnessD = avgFitness - tempAvgFitness

    for i, bus in enumerate(buses):
        if not bus.won:
            if bus.aliveTime > longestTime:
                longestTime = bus.aliveTime
                longestIndex = i
    longestTimeD = longestTime - tempLongestTime

    for i, bus in enumerate(buses):
        n = int((bus.fitness ** 2) * 100)
        if i == maxFitIndex:
            print(bus.fitness)
            if successCount < 2:
                n = int((bus.fitness ** 2) * 150)       # Squared the fitness value to make sure
                                                        # The furthest ones get much more place in the gene pool.
        if i == longestIndex and successCount > 1:
            n = int((bus.fitness ** 2) * 500)           # If it's the first one to finish when there are more boxes
                                                        # finishing the level, get much much more places in the pool.
        for _ in range(n):
            genePool.append(buses[i])

        # Reset
        buses.clear()
        generationCount = 0
        for i in range(busCount):
            buses.append(Bus(validbusX(), 290))

    if successCount >= len(buses)//2:
        print("More than half of the buses cleared the game")
    else:
        for i, bus in enumerate(buses):  # For every bus, create a child with crossover.
            randomIndex = rnd.randint(0, len(genePool) - 1)
            parentA = genePool[randomIndex].gene
            randomIndex = rnd.randint(0, len(genePool) - 1)
            parentB = genePool[randomIndex].gene
            child = parentA.CrossOver(parentB)
            buses[i] = Bus(validbusX(), 290, child.array)
        generationCount += 1
    frameCount = 0
    aliveBusCount = busCount
    finished = False

    


# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     main()