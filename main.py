# imports
import sys
import pygame
import asyncio
import random
from constants import *
from particle import Particle
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

# main function
async def main():
    # initialise pygame, sets screen, and prints startup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #start score counter
    start_time = pygame.time.get_ticks()
    last_point_time = start_time  # Track when we last awarded a point
    score = 0
    game_font = pygame.font.Font(None, 36)  # You already have this
    game_over_font = pygame.font.Font(None, 72)  # Bigger font for GAME OVER
    game_active = True  # New flag to track game state

    # create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # add to groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # create asteroid field
    asteroidfield = AsteroidField()
    # create variable initialising game clock
    clock = pygame.time.Clock()
    dt = 0
    # instantiate Player object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    #particle explosion
    def create_explosion(position, num_particles=10):
        for _ in range(num_particles):
            particle = Particle(position.x, position.y)
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            particle.velocity = pygame.Vector2(speed, 0).rotate(angle)
            particle.add(updatable, drawable)  # Add to your sprite groups

    # start infinite loop
    while True:
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if not game_active and event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
    # Reset game here
                    score = 0
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Clear all sprite groups
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
    # Add player back to groups
                    player.add(updatable, drawable)
    # Reset asteroid field
                    asteroidfield = AsteroidField()
                    game_active = True
                    continue

        screen.fill(color=(0, 0, 0))

        if game_active:
    # Your existing game logic here
            updatable.update(dt)

    # Collision checks
            for roid in asteroids:
                if roid.collides_with(player):
                    game_active = False 
                    continue
                for bullet in shots:
                    if bullet.collides_with(roid):
                        create_explosion(roid.position)
    # Award points based on asteroid size
                        if roid.radius <= ASTEROID_MIN_RADIUS * 2:  # Smallest asteroids
                            score += 3
                        elif roid.radius <= ASTEROID_MIN_RADIUS * 3:  # Medium asteroids
                            score += 2
                        else:  # Largest asteroids
                            score += 1
                        bullet.kill()
                        roid.split()

    # Drawing
            for item in drawable:
                item.draw(screen)

    # Score updates
            current_time = pygame.time.get_ticks()
            if (current_time - last_point_time) >= 1000:
                score += 1
                last_point_time = current_time

    # Draw score (your existing code)
            score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect()
            score_rect.topright = (SCREEN_WIDTH - 10, 10)
            screen.blit(score_text, score_rect)
        else:
    # Game Over screen
            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            final_score_text = game_font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = game_font.render("Press Enter to restart", True, (255, 255, 255))
            
            # Position the text in the center
            game_over_rect = game_over_text.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2 - 50)
            score_rect = final_score_text.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2 + 10)
            restart_rect = restart_text.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2 + 50)
            
            # Draw the game over screen
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, score_rect)
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


# End of main

if __name__ == "__main__":
    asyncio.run(main())
