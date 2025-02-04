#imports
import pygame
from constants import *
from player import *
from circleshape import *

#set the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#main function
def main():

#initialise pygame
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

#create variable initialising game clock
    clock = pygame.time.Clock()
    dt = 0

#instantiate Player object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
#start infinite loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
#colour the screen
        screen.fill(color=(0,0,0))
#draw the player each frame
        player.draw(screen)
#player update method hook
        player.update(dt)
#Update the full display surface to the screen
        pygame.display.flip()
#set the frame rate to 60 fps
        dt = (clock.tick(60) / 1000)
    
#End of main

if __name__ == "__main__":
    main()