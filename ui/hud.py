"""
Heads-up display for the game
"""
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, VALORANT_RED, VALORANT_BLUE
from core.utils import draw_text, format_time

class HUD:
    """
    Heads-up display for showing game information
    """
    def __init__(self):
        """Initialize the HUD"""
        # Create fonts
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_medium = pygame.font.SysFont("arial", 24)
        self.font_large = pygame.font.SysFont("arial", 36)
        self.font_huge = pygame.font.SysFont("arial", 72)
        
        # Game info
        self.game_mode = ""
        self.difficulty = ""
        self.score = 0
        self.accuracy = 0
        self.targets_hit = 0
        self.targets_missed = 0
        self.headshots = 0
        self.reaction_time = 0
        self.fps = 0
        self.time_left = 0
        
    def update(self, player, target_manager, fps, time_left):
        """
        Update the HUD with current game information
        
        Args:
            player (Player): The player object
            target_manager (TargetManager): The target manager
            fps (int): Current FPS
            time_left (float): Time left in seconds
        """
        self.score = target_manager.targets_hit * 100 - target_manager.targets_missed * 50
        self.accuracy = target_manager.get_accuracy()
        self.targets_hit = target_manager.targets_hit
        self.targets_missed = target_manager.targets_missed
        self.headshots = target_manager.headshots
        self.reaction_time = target_manager.get_avg_reaction_time()
        self.fps = fps
        self.time_left = time_left
        
    def draw(self, surface):
        """
        Draw the HUD on the surface
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw score
        draw_text(surface, f"Score: {self.score}", self.font_medium, WHITE, 
                 20, 20, "left")
        
        # Draw accuracy
        draw_text(surface, f"Accuracy: {self.accuracy:.1f}%", self.font_medium, WHITE, 
                 20, 50, "left")
        
        # Draw targets hit/missed
        draw_text(surface, f"Hits: {self.targets_hit} | Misses: {self.targets_missed}", 
                 self.font_medium, WHITE, 20, 80, "left")
        
        # Draw headshots
        draw_text(surface, f"Headshots: {self.headshots}", self.font_medium, WHITE, 
                 20, 110, "left")
        
        # Draw reaction time
        draw_text(surface, f"Avg. Reaction: {self.reaction_time:.0f}ms", self.font_medium, 
                 WHITE, 20, 140, "left")
        
        # Draw time left
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        draw_text(surface, f"Time: {minutes:02d}:{seconds:02d}", self.font_medium, WHITE, 
                 SCREEN_WIDTH - 20, 20, "right")
        
        # Draw FPS
        draw_text(surface, f"FPS: {self.fps}", self.font_small, WHITE, 
                 SCREEN_WIDTH - 20, 50, "right")
        
        # Draw game mode and difficulty
        draw_text(surface, f"Mode: {self.game_mode.capitalize()} | Difficulty: {self.difficulty.capitalize()}", 
                 self.font_small, WHITE, SCREEN_WIDTH // 2, 20, "center")
        
    def draw_countdown(self, surface, countdown):
        """
        Draw the countdown before the game starts
        
        Args:
            surface (pygame.Surface): Surface to draw on
            countdown (int): Countdown value
        """
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))
        
        # Draw the countdown number
        if countdown > 0:
            draw_text(surface, str(countdown), self.font_huge, WHITE, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "center")
        else:
            draw_text(surface, "GO!", self.font_huge, VALORANT_RED, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "center")
        
    def draw_pause_menu(self, surface):
        """
        Draw the pause menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        surface.blit(overlay, (0, 0))
        
        # Draw the pause title
        draw_text(surface, "PAUSED", self.font_large, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, "center")
        
        # Draw the instructions
        draw_text(surface, "Press ESC to resume", self.font_medium, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "center")
        draw_text(surface, "Press R to restart", self.font_medium, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, "center")
        draw_text(surface, "Press M to return to menu", self.font_medium, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, "center")
        draw_text(surface, "Press Q to quit", self.font_medium, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120, "center")
        
    def draw_game_over(self, surface, score, high_score):
        """
        Draw the game over screen
        
        Args:
            surface (pygame.Surface): Surface to draw on
            score (int): Final score
            high_score (int): High score
        """
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        surface.blit(overlay, (0, 0))
        
        # Draw the game over title
        draw_text(surface, "TRAINING COMPLETE", self.font_large, VALORANT_BLUE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, "center")
        
        # Draw the score
        draw_text(surface, f"Score: {score}", self.font_large, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, "center")
        
        # Draw the high score
        if score > high_score:
            draw_text(surface, "NEW HIGH SCORE!", self.font_medium, VALORANT_RED, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, "center")
        else:
            draw_text(surface, f"High Score: {high_score}", self.font_medium, WHITE, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, "center")
        
        # Draw the stats
        draw_text(surface, f"Accuracy: {self.accuracy:.1f}% | Targets Hit: {self.targets_hit} | Headshots: {self.headshots}", 
                 self.font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, "center")
        draw_text(surface, f"Average Reaction Time: {self.reaction_time:.0f}ms", 
                 self.font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, "center")
        
        # Draw the instructions
        draw_text(surface, "Press SPACE to continue", self.font_medium, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, "center")
