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

    #start game state
    game_state = "START"  # Can be "START", "PLAYING", or "GAME_OVER"

    #start screen
    # Create fonts
    game_title_font = pygame.font.Font(None, 100)
    game_font = pygame.font.Font(None, 32)
    game_title_text = game_title_font.render("ASTEROIDS", True, (255, 255, 255))
    move_instructions = game_font.render("WASD: Movement", True, (255, 255, 255))
    shoot_instructions = game_font.render("SPACE: Shoot", True, (255, 255, 255))
    start_text = game_font.render("Press Enter to start!", True, (255, 255, 255))
    #position elements
    game_title_rect = game_title_text.get_rect(centerx=SCREEN_WIDTH / 2, top=50)
    move_instructions_rect = move_instructions.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2 - 20)
    shoot_instructions_rect = shoot_instructions.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2 + 20)
    start_text_rect = start_text.get_rect(centerx=SCREEN_WIDTH / 2, bottom=SCREEN_HEIGHT - 50)

    
    # create variable initialising game clock
    clock = pygame.time.Clock()
    dt = 0
    # start score counter
    start_time = pygame.time.get_ticks()
    last_point_time = start_time  # Track when we last awarded a point
    score = 0
    # Load background image
    background = pygame.image.load("assets/game-background.jpeg").convert()
    # Scale it to fit screen if needed
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
    Particle.containers = (updatable, drawable)

    # instantiate Player object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # create asteroid field
    asteroidfield = AsteroidField()

    # particle explosion
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
                
    #draw the black screen
        screen.blit(background, (0, 0))

    
        if game_state == "START":
    # Draw start screen
            screen.blit(game_title_text, game_title_rect)
            screen.blit(move_instructions, move_instructions_rect)
            screen.blit(shoot_instructions, shoot_instructions_rect)
            screen.blit(start_text, start_text_rect)
        
    # Check for Enter key to start game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                game_state = "PLAYING"
    
    
    # Startup gameplay
        elif game_state == "PLAYING":
    #game fonts
            game_font = pygame.font.Font(None, 36)  # You already have this
            game_over_font = pygame.font.Font(None, 72)  # Bigger font for GAME OVER
    #screen fill and updateables
            screen.fill(color=(0, 0, 0))
            updatable.update(dt)

    # Collision checks
            for roid in asteroids:
                if roid.collides_with(player):
                    game_state = "GAME_OVER"
                    break
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


        elif game_state == "GAME_OVER":
            # Game Over screen
            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            final_score_text = game_font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = game_font.render("Press Enter to restart", True, (255, 255, 255))

            # Position the text in the center
            game_over_rect = game_over_text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2 - 50)
            score_rect = final_score_text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2 + 10)
            restart_rect = restart_text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2 + 50)

            # Draw the game over screen
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, score_rect)
            screen.blit(restart_text, restart_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # Reset game elements
                score = 0
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                updatable.empty()
                drawable.empty()
                asteroids.empty()
                shots.empty()
                player.add(updatable, drawable)
                asteroidfield = AsteroidField()
                game_state = "PLAYING"  # Back to playing state

        pygame.display.flip()
        dt = clock.tick(60) / 1000


# End of main
if __name__ == "__main__":
    asyncio.run(main())
