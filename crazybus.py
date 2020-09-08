#imports
import time
import sys
from gameClasses import *

pg.display.set_caption("AI Bus")

clock = pg.time.Clock()     # Clock object to control
FPS = 30                 # the Fps
defaultFont = pg.font.SysFont(None, 40)     # Default font of the program




def draw_window(win, kid, bg):
    # win.fill(pg.Color("blue"))
    bg.draw(win)
    kid.draw(win)    
    pg.display.update()


# Running game
playing = True

def main():
    bg = BackGround()
    akid = Kid(300, 400)

    while playing:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:       # close the screen and exit the program.
                pg.quit()
                sys.exit()
        akid.move()
        draw_window(win, akid, bg)

    pg.quit()
    quit()

main()


    


# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     main()