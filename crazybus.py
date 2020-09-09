#imports
import sys
from gameClasses import pg, Kid, Adult, Bus, BackGround, DNA, win, segoeFONT, WIN_HEIGHT, WIN_WIDTH, rnd

pg.display.set_caption("AI Bus")

clock = pg.time.Clock()     # Clock object to control time
FPS = 30                 # the Fps
defaultFont = pg.font.SysFont(None, 40)     # Default font of the program


def draw_window(win, bg, bus, victims, score):
    # win.fill(pg.Color("blue"))
    bg.draw(win)            
    the_score = segoeFONT.render("Score:" + str(score), 1, pg.Color("white"))
    win.blit(the_score, (WIN_WIDTH - 10 - the_score.get_width(), 10))

    bus.draw(win)
    for vic in victims:
        vic.draw(win)
    
    pg.display.update()


# random Victim
def randVictim(x, y):
    num = rnd.random()
    if num >= 0.5:
        return Adult(x+30, y)
    else:
        return Kid(x, y)




# Running game
playing = True

def main():
    bg = BackGround()
    score = 0
    # Kid(350, 480)
    victims = [Adult(350+30, 480)]    
    
    # x += 90 to switch lane ->
    bus = Bus(255+90, 290)

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
            if vic.collide(bus):
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

        bus.moveDown()
        draw_window(win, bg, bus, victims, score)

    pg.quit()
    quit()

main()


    


# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     main()