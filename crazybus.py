#imports
import sys
from gameClasses import *

pg.display.set_caption("AI Bus")

clock = pg.time.Clock()     # Clock object to control
FPS = 30                 # the Fps
defaultFont = pg.font.SysFont(None, 40)     # Default font of the program




def draw_window(win, kid, bg, bus):
    # win.fill(pg.Color("blue"))
    bg.draw(win)
    kid.draw(win)   
    bus.draw(win) 
    pg.display.update()


# Running game
playing = True

def main():
    bg = BackGround()
    kid = Kid(300, 480)
    # x += 90 to switch lane ->
    bus = Bus(255+90+90, 290)

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
                if event.key == pg.K_SPACE:
                    bus.jump()


        kid.move()
        bus.moveDown()
        draw_window(win, kid, bg, bus)

    pg.quit()
    quit()

main()


    


# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     main()