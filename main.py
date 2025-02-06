#imports
import sys
import pygame
from constants import *
from player import *
from circleshape import *
from asteroid import *
from asteroidfield import *

#set the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#main function
def main():

#initialise pygame
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

#create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
#add to groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

#create asteroid field
    asteroidfield = AsteroidField()

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

#player update method hook
        updatable.update(dt)
#collision check
        for roid in asteroids:
            if roid.collides_with(player):
                print("Game over!")
                sys.exit()
#draw the player each frame
        for item in drawable:
            item.draw(screen)
            
#Update the full display surface to the screen
        pygame.display.flip()
#set the frame rate to 60 fps
        dt = (clock.tick(60) / 1000)
    
#End of main

if __name__ == "__main__":
    main()