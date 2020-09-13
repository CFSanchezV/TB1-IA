#imports
from gameClasses import *

pg.display.set_caption("AI Bus")
clock = pg.time.Clock()
FPS = 60

#----------------GEN ALG COUNTERS---------------------#
rnd.seed(rnd.randrange(65432121))
genCount = 0
# Fitness (between 0 to 1) longestTime (bus.timeAlive) completeCount (No. of buses alive at time limit)
frameCount = 0
avgFit = 0
avgFitD = 0
longestTime = 0
longestTimeD = 0
completeCount = 0
completeCountD = 0
finishGame = False

matingPool = []

#------------------AUX functions--------------------#

def validvicX():
    validX = [350-100, 350, 350+90, 350+180]
    return rnd.choice(validX)

def validbusX(): # Random valid x for bus spawn
    validX = [255, 255+90, 255+180, 255+270]
    return rnd.choice(validX)

def randVictim(x, y):   # random Victim
    num = rnd.random()
    if num >= 0.5:
        return Adult(x+30, y)
    else:
        return Kid(x, y)

def drawText(string, x, y, size = 20, color=(255, 255, 255)):   # show text on screen
    segoe = pg.font.SysFont("segoeui", size, True)
    win.blit(segoe.render(string, True, color), (x, y))

def draw_window(win, bg, buses, victims, score):  # 'draw it all' method, order matters    
    the_score = segoeFONT.render("Score:" + str(score), True, WHITE)
    win.blit(the_score, (WIN_WIDTH - 10 - the_score.get_width(), 0))
    
    for bus in buses:
        bus.draw(win)

    for vic in victims:
        vic.draw(win)
        
    pg.display.update()
    bg.draw(win)

# test
def FinishGeneration():

    global finishGame, avgFit, frameLimit, completeCount
    global genCount, frameCount, longestTime, avgFitD
    global longestTimeD, completeCountD, aliveBusCount, buses

    tmpLongestTime = longestTime
    tmpAvgFit = avgFit
    tmpCompleteCount = completeCount
    
    maxFit = 0
    longestTime = 0

    maxFitIndex = 0
    longestIndex = 0
    completeCount = 0
    avgFitSum = 0
    matingPool.clear()

    for bus in buses:
        bus.CalculateFitness()
        avgFitSum += bus.fitness
        if bus.fitness >= 1.0 or bus.aliveTime == frameLimit:
            completeCount += 1        
        if bus.fitness > maxFit:
            maxFit = bus.fitness
            maxFitIndex = buses.index(bus)
        
        # if bus.fitness != 1.0:
        #     print("fit:", end=" "); print(bus.fitness)
            
    completeCountD = completeCount - tmpCompleteCount
    avgFit = avgFitSum / len(buses)
    avgFitD = avgFit - tmpAvgFit

    for i, bus in enumerate(buses):
        if not bus.won:
            if bus.aliveTime > longestTime:
                longestTime = bus.aliveTime
                longestIndex = i
    longestTimeD = longestTime - tmpLongestTime

    for i, bus in enumerate(buses):
        n = int((bus.fitness ** 2) * 100)
        if i == maxFitIndex:
            # check
            print(bus.fitness)

            if completeCount < 2:
                n = int((bus.fitness ** 2) * 150)

        if i == longestIndex and completeCount > 1:
            n = int((bus.fitness ** 2) * 500)           

        for _ in range(n):
            matingPool.append(buses[i])
    
    # check
    print(len(matingPool))
                
    # Reset all if they all win
    if completeCount >= len(buses):
        print("All of the buses cleared the game")
        buses.clear()
        genCount = 0
        maxFit = 0
        longestTime = 0
        maxFitIndex = 0
        longestIndex = 0
        completeCount = 0
        avgFitSum = 0
        
        for _ in range(busCount):            
            buses.append(Bus(validbusX(), 290))

    # Crossover bus children
    else:
        for i, bus in enumerate(buses):  
            index = rnd.randrange(0, len(matingPool) )
            mother = matingPool[index].genes            
            index = rnd.randrange(0, len(matingPool) )
            father = matingPool[index].genes       
            child = mother.CrossOver(father)
            buses[i] = Bus(validbusX(), 290, child.genoma)
        genCount += 1
    frameCount = 0
    aliveBusCount = busCount
    finishGame = False


# Bus List.
buses = []
for _ in range(busCount):            
    buses.append(Bus(validbusX(), 290))

#-----------------------Running game------------------------#
playing = True
def main():
    global frameCount, finishGame, frameLimit, aliveBusCount, buses
    bg = BackGround()
    # debuggin.. Kid(350, 480)
    victims = [Adult(350+30, 480)]
    # win display, clock must be init
    score = 0

    # x += 90 to switch lane -> bus = Bus(255+90, 290)    
    while playing:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    pass
                if event.key == pg.K_RIGHT:
                    pass
                if event.key == pg.K_UP:
                    pass
        # Display timers
        frame_counter = "Frame: " + str(frameCount)
        counter_limit = "  / " + str(frameLimit)
        
        add_vic = False
        collided = False
        rem = []        
        for vic in victims:
            for i, bus in enumerate(buses):
                if bus.canMove:
                    bus.move(vic, frameCount)

                if vic.collide(buses[i]):
                    bus.crashed = True
                    aliveBusCount -= 1
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
            victims.append(randVictim(validvicX(), 480))
        
        for r in rem:
            victims.remove(r)
        
        for i, bus in enumerate(buses):
            #also ticks aliveTime in MoveDown
            if bus.alive:
                bus.testMoveAbility(frameCount)
                bus.moveDown()
            if bus.crashed:
                bus.alive = False                 
        
        drawText(frame_counter, 10, 0)        
        drawText(counter_limit, 120, 0)
        drawText("Generación: " + str(genCount), 10, 20)
        drawText("Buses vivos: " + str(aliveBusCount), 10, 40)

        drawText("Generación previa:", 10, 420, 30)
        drawText("No. de Buses:            " + str(len(buses)), 30, 460)
        drawText("Buses que ganaron:   " + str(completeCount), 30, 480)
        if completeCountD > 0:
            drawText("+" + str(completeCountD), 300, 480, 20, GREEN)
        else:
            drawText("-" + str(-completeCountD), 300, 480, 20, RED)

        drawText("Fitness promedio:      " + str(round(avgFit, 3)), 30, 500)
        if avgFitD > 0:
            drawText("+" + str(round(avgFitD, 3)), 300, 500, 20, GREEN)
        else:
            drawText("-" + str(round(-avgFitD, 3)), 300, 500, 20, RED)

        drawText("Tiempo record:          " + str(longestTime), 30, 520)
        if longestTimeD < 0:
            drawText("-" + str(-longestTimeD), 300, 520, 20, RED)
        else:
            drawText("+" + str(longestTimeD), 300, 520, 20, GREEN)
        
        draw_window(win, bg, buses, victims, score)
        
        # If frameCount > limit, or no buses left -> generation is done. Terminate
        if (frameCount >= frameLimit-1) or aliveBusCount <= 0:
            frameCount = frameLimit-1
            finishGame = True
        else:                                  
            frameCount += 1

        if finishGame:
            FinishGeneration()

    pg.quit()
    quit()


if __name__ == '__main__':
    main()