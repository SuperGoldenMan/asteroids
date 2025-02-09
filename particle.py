import pygame
from circleshape import *


class Particle(CircleShape):
    def __init__(self, x, y, color=(255, 100, 0)):  # Orange-ish by default
        super().__init__(x, y, 2)  # Small radius for particles
        self.color = color
        self.lifetime = 1.0  # Particle lives for 1 second
        self.alpha = 255  # For fade out effect

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        self.alpha = max(0, int(255 * (self.lifetime)))
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        color_with_alpha = (*self.color, self.alpha)
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color_with_alpha, (self.radius, self.radius), self.radius)
        screen.blit(surface, (self.position.x - self.radius, self.position.y - self.radius))
