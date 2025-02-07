#imports
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


#main function
def main():

#initialise pygame, sets screen, and prints startup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

#create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
#add to groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

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

#asteroid/player collision check
        for roid in asteroids:
            if roid.collides_with(player):
                print("Game over!")
                sys.exit()
#asteroid/shot collision check
            for bullet in shots:
                if bullet.collides_with(roid):
                    bullet.kill()
                    roid.split()

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