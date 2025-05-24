"""
Visual effects for the game
"""
import random
import pygame
import math

class Particle:
    """
    Simple particle effect
    """
    def __init__(self, x, y, color, size, speed, lifetime):
        """
        Initialize a particle
        
        Args:
            x (int): X position
            y (int): Y position
            color (tuple): RGB color tuple
            size (int): Particle size
            speed (float): Movement speed
            lifetime (int): Lifetime in milliseconds
        """
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.birth_time = pygame.time.get_ticks()
        self.age = 0
        
        # Random direction
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
    def update(self):
        """Update the particle"""
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Update age
        self.age = pygame.time.get_ticks() - self.birth_time
        
        # Shrink as it ages
        self.size = max(1, self.size * (1 - self.age / self.lifetime))
        
        # Check if it's dead
        return self.age >= self.lifetime
        
    def draw(self, surface):
        """
        Draw the particle
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Calculate alpha based on age
        alpha = 255 * (1 - self.age / self.lifetime)
        
        # Draw the particle
        pygame.draw.circle(surface, self.color + (alpha,), (int(self.x), int(self.y)), int(self.size))


class HitEffect:
    """
    Effect shown when a target is hit
    """
    def __init__(self, x, y, color, size):
        """
        Initialize a hit effect
        
        Args:
            x (int): X position
            y (int): Y position
            color (tuple): RGB color tuple
            size (int): Effect size
        """
        self.x = x
        self.y = y
        self.color = color
        self.max_size = size
        self.size = 0
        self.growth_rate = size / 10  # Grow to full size in 10 frames
        self.shrink_rate = size / 20  # Shrink in 20 frames
        self.growing = True
        self.lifetime = 300  # milliseconds
        self.birth_time = pygame.time.get_ticks()
        
    def update(self):
        """Update the hit effect"""
        if self.growing:
            self.size += self.growth_rate
            if self.size >= self.max_size:
                self.size = self.max_size
                self.growing = False
        else:
            self.size -= self.shrink_rate
            
        # Check if it's dead
        age = pygame.time.get_ticks() - self.birth_time
        return self.size <= 0 or age >= self.lifetime
        
    def draw(self, surface):
        """
        Draw the hit effect
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Calculate alpha based on size
        alpha = 255 * (self.size / self.max_size)
        
        # Draw the effect as a circle
        pygame.draw.circle(surface, self.color + (alpha,), (int(self.x), int(self.y)), int(self.size), 2)
        

class TextEffect:
    """
    Floating text effect
    """
    def __init__(self, x, y, text, color, size, lifetime=1000):
        """
        Initialize a text effect
        
        Args:
            x (int): X position
            y (int): Y position
            text (str): Text to display
            color (tuple): RGB color tuple
            size (int): Font size
            lifetime (int): Lifetime in milliseconds
        """
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.birth_time = pygame.time.get_ticks()
        self.age = 0
        self.vy = -1  # Float upward
        
        # Create the font and render the text
        self.font = pygame.font.SysFont("arial", size, bold=True)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=(x, y))
        
    def update(self):
        """Update the text effect"""
        # Update position
        self.y += self.vy
        self.text_rect.center = (self.x, self.y)
        
        # Update age
        self.age = pygame.time.get_ticks() - self.birth_time
        
        # Check if it's dead
        return self.age >= self.lifetime
        
    def draw(self, surface):
        """
        Draw the text effect
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Calculate alpha based on age
        alpha = 255 * (1 - self.age / self.lifetime)
        
        # Create a copy of the text surface with the new alpha
        text_surface_alpha = self.text_surface.copy()
        text_surface_alpha.set_alpha(alpha)
        
        # Draw the text
        surface.blit(text_surface_alpha, self.text_rect)


class EffectManager:
    """
    Manages all visual effects
    """
    def __init__(self):
        """Initialize the effect manager"""
        self.particles = []
        self.hit_effects = []
        self.text_effects = []
        
    def update(self):
        """Update all effects"""
        # Update particles and remove dead ones
        self.particles = [p for p in self.particles if not p.update()]
        
        # Update hit effects and remove dead ones
        self.hit_effects = [e for e in self.hit_effects if not e.update()]
        
        # Update text effects and remove dead ones
        self.text_effects = [t for t in self.text_effects if not t.update()]
        
    def draw(self, surface):
        """
        Draw all effects
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Create a surface for alpha blending
        alpha_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(alpha_surface)
            
        # Draw hit effects
        for effect in self.hit_effects:
            effect.draw(alpha_surface)
            
        # Draw text effects
        for text in self.text_effects:
            text.draw(alpha_surface)
            
        # Blit the alpha surface onto the main surface
        surface.blit(alpha_surface, (0, 0))
        
    def add_particle_effect(self, pos, color, size, count):
        """
        Add a particle effect at the given position
        
        Args:
            pos (tuple): Position (x, y)
            color (tuple): RGB color tuple
            size (int): Particle size
            count (int): Number of particles to create
        """
        for _ in range(count):
            speed = random.uniform(1, 3)
            lifetime = random.randint(300, 800)
            self.particles.append(Particle(pos[0], pos[1], color, size, speed, lifetime))
            
    def add_hit_effect(self, pos, color, size):
        """
        Add a hit effect at the given position
        
        Args:
            pos (tuple): Position (x, y)
            color (tuple): RGB color tuple
            size (int): Effect size
        """
        self.hit_effects.append(HitEffect(pos[0], pos[1], color, size))
        
    def add_text_effect(self, pos, text, color, size):
        """
        Add a text effect at the given position
        
        Args:
            pos (tuple): Position (x, y)
            text (str): Text to display
            color (tuple): RGB color tuple
            size (int): Font size
        """
        self.text_effects.append(TextEffect(pos[0], pos[1], text, color, size))
        
    def clear(self):
        """Clear all effects"""
        self.particles.clear()
        self.hit_effects.clear()
        self.text_effects.clear()
