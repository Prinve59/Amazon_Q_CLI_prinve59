"""
Utility functions for the game
"""
import os
import json
import pygame
from core.settings import IMAGES_DIR, SOUNDS_DIR, FONTS_DIR

def load_image(filename, scale=1.0, convert_alpha=True):
    """
    Load an image from the images directory
    
    Args:
        filename (str): Image filename
        scale (float): Scale factor for the image
        convert_alpha (bool): Whether to convert the image to have alpha channel
        
    Returns:
        pygame.Surface: The loaded image
    """
    path = os.path.join(IMAGES_DIR, filename)
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
            
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
            
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def load_sound(filename):
    """
    Load a sound from the sounds directory
    
    Args:
        filename (str): Sound filename
        
    Returns:
        pygame.mixer.Sound: The loaded sound
    """
    path = os.path.join(SOUNDS_DIR, filename)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return None

def load_font(filename, size):
    """
    Load a font from the fonts directory
    
    Args:
        filename (str): Font filename
        size (int): Font size
        
    Returns:
        pygame.font.Font: The loaded font
    """
    path = os.path.join(FONTS_DIR, filename)
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Error loading font {path}: {e}")
        return pygame.font.SysFont("arial", size)

def load_json(filename):
    """
    Load JSON data from a file
    
    Args:
        filename (str): JSON filename
        
    Returns:
        dict: The loaded JSON data or empty dict if file doesn't exist
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(data, filename):
    """
    Save JSON data to a file
    
    Args:
        data (dict): Data to save
        filename (str): JSON filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON to {filename}: {e}")

def draw_text(surface, text, font, color, x, y, align="center"):
    """
    Draw text on a surface with alignment options
    
    Args:
        surface (pygame.Surface): Surface to draw on
        text (str): Text to draw
        font (pygame.font.Font): Font to use
        color (tuple): RGB color tuple
        x (int): X position
        y (int): Y position
        align (str): Text alignment ("left", "center", "right")
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "left":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
        
    surface.blit(text_surface, text_rect)

def format_time(milliseconds):
    """
    Format milliseconds as MM:SS.ms
    
    Args:
        milliseconds (int): Time in milliseconds
        
    Returns:
        str: Formatted time string
    """
    seconds = milliseconds / 1000
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:05.2f}"
def load_background(filename, width, height):
    """
    Load a background image and scale it to the specified dimensions
    
    Args:
        filename (str): Background image filename
        width (int): Target width
        height (int): Target height
        
    Returns:
        pygame.Surface: The loaded and scaled background image
    """
    from core.settings import BACKGROUNDS_DIR
    
    path = os.path.join(BACKGROUNDS_DIR, filename)
    try:
        # Create a placeholder if the file doesn't exist
        if not os.path.exists(path):
            # Create a gradient background as a placeholder
            surface = pygame.Surface((width, height))
            for y in range(height):
                # Create a gradient from dark blue to dark purple
                color = (20, 20, 40 + int(y / height * 40))
                pygame.draw.line(surface, color, (0, y), (width, y))
                
            # Add some grid lines for depth
            grid_spacing = 50
            grid_color = (60, 60, 100, 30)
            for x in range(0, width, grid_spacing):
                pygame.draw.line(surface, grid_color, (x, 0), (x, height), 1)
            for y in range(0, height, grid_spacing):
                pygame.draw.line(surface, grid_color, (0, y), (width, y), 1)
                
            return surface
            
        # Load and scale the image
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))
    except pygame.error as e:
        print(f"Error loading background {path}: {e}")
        # Return a placeholder surface with a gradient
        surface = pygame.Surface((width, height))
        for y in range(height):
            color = (20, 20, 40 + int(y / height * 40))
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface
