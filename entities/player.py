"""
Player entity for the game (crosshair control)
"""
import pygame
from core.settings import CROSSHAIR_SIZE, VALORANT_RED

class Player:
    """
    Player class that handles crosshair and shooting
    """
    def __init__(self):
        """Initialize the player"""
        self.crosshair_size = CROSSHAIR_SIZE
        self.crosshair_color = VALORANT_RED
        self.crosshair_style = "default"
        
        # Create the crosshair surface
        self.crosshair = self.create_crosshair()
        self.crosshair_rect = self.crosshair.get_rect()
        
        # Set the crosshair to the center of the screen
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        self.crosshair_rect.center = (screen_width // 2, screen_height // 2)
        
        # Shooting properties
        self.ammo = 30
        self.max_ammo = 30
        self.reloading = False
        self.reload_start_time = 0
        self.reload_time = 1500  # milliseconds
        
        # Stats
        self.shots_fired = 0
        self.shots_hit = 0
        self.headshots = 0
        
    def create_crosshair(self):
        """
        Create the crosshair surface
        
        Returns:
            pygame.Surface: The crosshair surface
        """
        size = self.crosshair_size
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.crosshair_style == "default":
            # Draw a simple crosshair
            thickness = max(1, size // 10)
            gap = size // 4
            
            # Horizontal line
            pygame.draw.rect(surface, self.crosshair_color, 
                            (0, size // 2 - thickness // 2, 
                             size // 2 - gap, thickness))
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size // 2 + gap, size // 2 - thickness // 2, 
                             size // 2 - gap, thickness))
            
            # Vertical line
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size // 2 - thickness // 2, 0, 
                             thickness, size // 2 - gap))
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size // 2 - thickness // 2, size // 2 + gap, 
                             thickness, size // 2 - gap))
            
            # Center dot
            pygame.draw.circle(surface, self.crosshair_color, 
                              (size // 2, size // 2), thickness)
            
        elif self.crosshair_style == "dot":
            # Just a simple dot
            pygame.draw.circle(surface, self.crosshair_color, 
                              (size // 2, size // 2), size // 6)
            
        elif self.crosshair_style == "circle":
            # Circle crosshair
            thickness = max(1, size // 20)
            pygame.draw.circle(surface, self.crosshair_color, 
                              (size // 2, size // 2), size // 3, thickness)
            pygame.draw.circle(surface, self.crosshair_color, 
                              (size // 2, size // 2), size // 10)
            
        elif self.crosshair_style == "valorant":
            # Valorant-style crosshair
            thickness = max(1, size // 15)
            gap = size // 5
            outer_length = size // 3
            
            # Outer lines
            pygame.draw.rect(surface, self.crosshair_color, 
                            (0, size // 2 - thickness // 2, 
                             outer_length, thickness))
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size - outer_length, size // 2 - thickness // 2, 
                             outer_length, thickness))
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size // 2 - thickness // 2, 0, 
                             thickness, outer_length))
            pygame.draw.rect(surface, self.crosshair_color, 
                            (size // 2 - thickness // 2, size - outer_length, 
                             thickness, outer_length))
            
        return surface
        
    def update(self):
        """Update the player state"""
        # Get the game instance to check if we're in fullscreen mode
        game = pygame.display.get_surface()
        fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
        
        # Update crosshair position to follow the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # If we're in fullscreen mode, we need to scale the mouse position
        if fullscreen:
            # Get the game's actual resolution
            game_width = 1024  # SCREEN_WIDTH
            game_height = 768  # SCREEN_HEIGHT
            
            # Get the screen's resolution
            screen_width = pygame.display.get_surface().get_width()
            screen_height = pygame.display.get_surface().get_height()
            
            # Calculate scale factors
            scale_x = game_width / screen_width
            scale_y = game_height / screen_height
            
            # Scale the mouse position
            mouse_pos = (int(mouse_pos[0] * scale_x), int(mouse_pos[1] * scale_y))
        
        self.crosshair_rect.center = mouse_pos
        
        # Check if reloading is complete
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.reload_start_time >= self.reload_time:
                self.ammo = self.max_ammo
                self.reloading = False
                
    def draw(self, surface):
        """
        Draw the player's crosshair
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        surface.blit(self.crosshair, self.crosshair_rect)
        
    def shoot(self, target_manager):
        """
        Handle shooting logic
        
        Args:
            target_manager (TargetManager): The target manager to check for hits
            
        Returns:
            Target or None: The hit target or None if no target was hit
        """
        if self.reloading or self.ammo <= 0:
            return None
            
        # Decrease ammo and record shot
        self.ammo -= 1
        self.shots_fired += 1
        
        # Check if we hit a target using the mouse position
        mouse_pos = pygame.mouse.get_pos()
        hit_radius = 8  # pixels - small hit forgiveness radius
        hit_target = target_manager.check_hit(mouse_pos, hit_radius)
        
        if hit_target:
            self.shots_hit += 1
            if hit_target.type == "headshot":
                self.headshots += 1
                
        # Auto-reload if out of ammo
        if self.ammo <= 0:
            self.reload()
            
        return hit_target
        
    def reload(self):
        """Start reloading"""
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            
    def set_crosshair_style(self, style, color=None, size=None):
        """
        Change the crosshair style
        
        Args:
            style (str): Crosshair style ("default", "dot", "circle", "valorant")
            color (tuple, optional): RGB color tuple
            size (int, optional): Size of the crosshair
        """
        self.crosshair_style = style
        
        if color:
            self.crosshair_color = color
            
        if size:
            self.crosshair_size = size
            
        # Recreate the crosshair with new settings
        self.crosshair = self.create_crosshair()
        self.crosshair_rect = self.crosshair.get_rect()
        
        # Reset position to center
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        self.crosshair_rect.center = (screen_width // 2, screen_height // 2)
        
    def get_accuracy(self):
        """
        Calculate the current accuracy
        
        Returns:
            float: Accuracy percentage (0-100)
        """
        if self.shots_fired == 0:
            return 0
        return (self.shots_hit / self.shots_fired) * 100
