"""
Main game class that manages the game state and loop
"""
import pygame
import sys
import time
import datetime
from core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, STATE_MENU, STATE_PLAYING,
    STATE_PAUSED, STATE_GAME_OVER, STATE_LEADERBOARD, STATE_SETTINGS,
    DEFAULT_SETTINGS, SCORES_FILE, SETTINGS_FILE
)
from core.utils import load_json, save_json
from entities.player import Player
from entities.target import TargetManager
from entities.effects import EffectManager
from ui.hud import HUD
from ui.menu import MainMenu, ModeSelectionMenu, DifficultyMenu, SettingsMenu, LeaderboardMenu

class Game:
    """
    Main game class
    """
    def __init__(self):
        """Initialize the game"""
        # Initialize pygame
        pygame.init()
        
        # Load settings
        self.settings = load_json("settings.json")
        if not self.settings:
            self.settings = DEFAULT_SETTINGS.copy()
            save_json(self.settings, "settings.json")
        
        # Get the desktop screen size for proper fullscreen scaling
        desktop_info = pygame.display.Info()
        self.desktop_width = desktop_info.current_w
        self.desktop_height = desktop_info.current_h
            
        # Set up the display
        self.fullscreen = self.settings["fullscreen"]
        if self.fullscreen:
            # Use the desktop resolution for fullscreen
            self.screen = pygame.display.set_mode((self.desktop_width, self.desktop_height), pygame.FULLSCREEN)
            # Create a scaled surface for rendering at the base resolution
            self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.scale_factor_x = self.desktop_width / SCREEN_WIDTH
            self.scale_factor_y = self.desktop_height / SCREEN_HEIGHT
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.game_surface = self.screen
            self.scale_factor_x = 1.0
            self.scale_factor_y = 1.0
            
        pygame.display.set_caption(TITLE)
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        self.fps = FPS
        
        # Game state
        self.state = STATE_MENU
        self.running = True
        self.game_mode = None
        self.difficulty = None
        self.session_time = 60  # seconds
        self.start_time = 0
        self.time_left = 0
        self.countdown = 3
        self.countdown_start = 0
        
        # Load scores
        self.scores = load_json("scores.json")
        
        # Create game objects
        self.player = None
        self.target_manager = None
        self.effect_manager = None
        self.hud = None
        
        # Load menu background
        from core.settings import BACKGROUND_MAPS
        from core.utils import load_background
        self.background = load_background(BACKGROUND_MAPS.get("menu", "valorant_menu.jpg"), SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create menus
        self.main_menu = MainMenu()
        self.mode_menu = ModeSelectionMenu()
        self.difficulty_menu = None
        self.settings_menu = SettingsMenu(self.settings)
        self.leaderboard_menu = LeaderboardMenu(self.scores)
        self.current_menu = self.main_menu
        
        # Hide the mouse cursor but don't lock it to the center
        pygame.mouse.set_visible(False)
        
    def start_game(self, mode, difficulty):
        """
        Start a new game
        
        Args:
            mode (str): Game mode
            difficulty (str): Difficulty level
        """
        self.game_mode = mode
        self.difficulty = difficulty
        
        # Create game objects
        self.player = Player()
        self.target_manager = TargetManager(mode, difficulty)
        self.effect_manager = EffectManager()
        self.hud = HUD()
        
        # Set HUD info
        self.hud.game_mode = mode
        self.hud.difficulty = difficulty
        
        # Load the background for this mode
        from core.settings import BACKGROUND_MAPS
        from core.utils import load_background
        
        background_file = BACKGROUND_MAPS.get(mode, "valorant_menu.jpg")
        if self.fullscreen:
            self.background = load_background(background_file, SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            self.background = load_background(background_file, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Start countdown
        self.state = STATE_PLAYING
        self.countdown = 3
        self.countdown_start = time.time()
        
    def update(self):
        """Update the game state"""
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Update based on game state
        if self.state == STATE_MENU:
            self.current_menu.update(mouse_pos)
            
        elif self.state == STATE_PLAYING:
            # Check if countdown is active
            current_time = time.time()
            if self.countdown >= 0:
                if current_time - self.countdown_start > 1:
                    self.countdown -= 1
                    self.countdown_start = current_time
                    
                    # Start the game when countdown reaches -1
                    if self.countdown == -1:
                        self.start_time = time.time()
            else:
                # Update game objects
                self.player.update()
                self.target_manager.update()
                self.effect_manager.update()
                
                # Update time left
                self.time_left = max(0, self.session_time - (time.time() - self.start_time))
                
                # Check if time is up
                if self.time_left <= 0:
                    self.state = STATE_GAME_OVER
                    self.save_score()
                    
                # Update HUD
                self.hud.update(self.player, self.target_manager, int(self.clock.get_fps()), self.time_left)
                
        elif self.state == STATE_PAUSED:
            # Nothing to update in pause state
            pass
            
        elif self.state == STATE_GAME_OVER:
            # Nothing to update in game over state
            pass
            
        elif self.state == STATE_SETTINGS:
            self.settings_menu.update(mouse_pos)
            
        elif self.state == STATE_LEADERBOARD:
            self.leaderboard_menu.update(mouse_pos)
            
    def draw(self):
        """Draw the game"""
        # Clear the game surface
        if self.fullscreen:
            # Draw background
            self.game_surface.blit(self.background, (0, 0))
        else:
            # Draw background
            self.screen.blit(self.background, (0, 0))
        
        # Draw based on game state
        if self.state == STATE_MENU:
            if self.fullscreen:
                self.current_menu.draw(self.game_surface)
            else:
                self.current_menu.draw(self.screen)
            
        elif self.state == STATE_PLAYING:
            # Draw game objects
            if self.fullscreen:
                self.target_manager.draw(self.game_surface)
                self.effect_manager.draw(self.game_surface)
                self.player.draw(self.game_surface)
                
                # Draw HUD
                self.hud.draw(self.game_surface)
                
                # Draw countdown if active
                if self.countdown >= 0:
                    self.hud.draw_countdown(self.game_surface, self.countdown)
            else:
                self.target_manager.draw(self.screen)
                self.effect_manager.draw(self.screen)
                self.player.draw(self.screen)
                
                # Draw HUD
                self.hud.draw(self.screen)
                
                # Draw countdown if active
                if self.countdown >= 0:
                    self.hud.draw_countdown(self.screen, self.countdown)
                
        elif self.state == STATE_PAUSED:
            # Draw game objects (background)
            if self.fullscreen:
                self.target_manager.draw(self.game_surface)
                self.effect_manager.draw(self.game_surface)
                self.player.draw(self.game_surface)
                self.hud.draw(self.game_surface)
                
                # Draw pause menu
                self.hud.draw_pause_menu(self.game_surface)
            else:
                self.target_manager.draw(self.screen)
                self.effect_manager.draw(self.screen)
                self.player.draw(self.screen)
                self.hud.draw(self.screen)
                
                # Draw pause menu
                self.hud.draw_pause_menu(self.screen)
            
        elif self.state == STATE_GAME_OVER:
            # Draw game objects (background)
            if self.fullscreen:
                self.target_manager.draw(self.game_surface)
                self.effect_manager.draw(self.game_surface)
                self.player.draw(self.game_surface)
                
                # Get high score for current mode and difficulty
                high_score = self.get_high_score()
                
                # Draw game over screen
                self.hud.draw_game_over(self.game_surface, self.hud.score, high_score)
            else:
                self.target_manager.draw(self.screen)
                self.effect_manager.draw(self.screen)
                self.player.draw(self.screen)
                
                # Get high score for current mode and difficulty
                high_score = self.get_high_score()
                
                # Draw game over screen
                self.hud.draw_game_over(self.screen, self.hud.score, high_score)
            
        elif self.state == STATE_SETTINGS:
            if self.fullscreen:
                self.settings_menu.draw(self.game_surface)
            else:
                self.settings_menu.draw(self.screen)
            
        elif self.state == STATE_LEADERBOARD:
            if self.fullscreen:
                self.leaderboard_menu.draw(self.game_surface)
            else:
                self.leaderboard_menu.draw(self.screen)
        
        # If in fullscreen mode, scale the game surface to the screen
        if self.fullscreen:
            # Scale the game surface to fill the screen
            scaled_surface = pygame.transform.scale(self.game_surface, (self.desktop_width, self.desktop_height))
            self.screen.blit(scaled_surface, (0, 0))
            
        # Update the display
        pygame.display.flip()
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING and self.countdown < 0:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                    elif self.state == STATE_MENU and self.current_menu != self.main_menu:
                        # Go back to previous menu
                        if self.current_menu == self.mode_menu:
                            self.current_menu = self.main_menu
                        elif self.current_menu == self.difficulty_menu:
                            self.current_menu = self.mode_menu
                    elif self.state == STATE_SETTINGS:
                        self.save_settings()
                        self.state = STATE_MENU
                        self.current_menu = self.main_menu
                    elif self.state == STATE_LEADERBOARD:
                        self.state = STATE_MENU
                        self.current_menu = self.main_menu
                        
                elif event.key == pygame.K_r:
                    if self.state == STATE_PLAYING:
                        self.player.reload()
                    elif self.state == STATE_PAUSED:
                        # Restart the game
                        self.start_game(self.game_mode, self.difficulty)
                        
                elif event.key == pygame.K_m and self.state == STATE_PAUSED:
                    # Return to menu
                    self.state = STATE_MENU
                    self.current_menu = self.main_menu
                    
                elif event.key == pygame.K_q and self.state == STATE_PAUSED:
                    # Quit the game
                    self.running = False
                    
                elif event.key == pygame.K_SPACE and self.state == STATE_GAME_OVER:
                    # Return to menu after game over
                    self.state = STATE_MENU
                    self.current_menu = self.main_menu
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Convert mouse position if in fullscreen mode
                    mouse_pos = pygame.mouse.get_pos()
                    if self.fullscreen:
                        # Convert from screen coordinates to game coordinates
                        mouse_pos = (
                            int(mouse_pos[0] / self.scale_factor_x),
                            int(mouse_pos[1] / self.scale_factor_y)
                        )
                    
                    if self.state == STATE_PLAYING and self.countdown < 0:
                        # Shoot
                        hit_target = self.player.shoot(self.target_manager)
                        
                        if hit_target:
                            # Add hit effect
                            if hit_target.type == "headshot":
                                self.effect_manager.add_hit_effect(hit_target.rect.center, (255, 215, 0), hit_target.size)
                                self.effect_manager.add_text_effect(hit_target.rect.center, "HEADSHOT!", (255, 215, 0), 24)
                            else:
                                self.effect_manager.add_hit_effect(hit_target.rect.center, (255, 70, 85), hit_target.size)
                                
                            # Add particle effect
                            self.effect_manager.add_particle_effect(hit_target.rect.center, (255, 255, 255), 3, 15)
                        else:
                            # Miss effect at mouse position
                            self.effect_manager.add_hit_effect(mouse_pos, (150, 150, 150), 10)
                            
                    elif self.state == STATE_MENU:
                        # Handle menu button clicks
                        action = self.current_menu.handle_event(event)
                        
                        if action:
                            if self.current_menu == self.main_menu:
                                if action == "Start Training":
                                    self.current_menu = self.mode_menu
                                elif action == "Settings":
                                    self.state = STATE_SETTINGS
                                elif action == "Leaderboard":
                                    self.state = STATE_LEADERBOARD
                                elif action == "Quit":
                                    self.running = False
                                    
                            elif self.current_menu == self.mode_menu:
                                if action == "Back":
                                    self.current_menu = self.main_menu
                                else:
                                    # Selected a game mode
                                    self.difficulty_menu = DifficultyMenu(action.lower())
                                    self.current_menu = self.difficulty_menu
                                    
                            elif self.current_menu == self.difficulty_menu:
                                if action == "Back":
                                    self.current_menu = self.mode_menu
                                else:
                                    # Selected a difficulty
                                    self.start_game(self.difficulty_menu.selected_mode, action.lower())
                                    
                    elif self.state == STATE_SETTINGS:
                        action = self.settings_menu.handle_event(event)
                        if action == "Save and Exit":
                            self.save_settings()
                            self.state = STATE_MENU
                            self.current_menu = self.main_menu
                            
                    elif self.state == STATE_LEADERBOARD:
                        action = self.leaderboard_menu.handle_event(event)
                        if action == "Back":
                            self.state = STATE_MENU
                            self.current_menu = self.main_menu
                            
    def save_settings(self):
        """Save the current settings to file"""
        save_json(self.settings, "settings.json")
        
        # Apply settings
        if self.settings["fullscreen"] != self.fullscreen:
            self.fullscreen = self.settings["fullscreen"]
            
            # Get desktop info for proper fullscreen
            desktop_info = pygame.display.Info()
            self.desktop_width = desktop_info.current_w
            self.desktop_height = desktop_info.current_h
            
            if self.fullscreen:
                # Switch to fullscreen at desktop resolution
                self.screen = pygame.display.set_mode((self.desktop_width, self.desktop_height), pygame.FULLSCREEN)
                # Create a scaled surface for rendering at the base resolution
                self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.scale_factor_x = self.desktop_width / SCREEN_WIDTH
                self.scale_factor_y = self.desktop_height / SCREEN_HEIGHT
            else:
                # Switch to windowed mode at base resolution
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.game_surface = self.screen
                self.scale_factor_x = 1.0
                self.scale_factor_y = 1.0
                
    def save_score(self):
        """Save the current score to the leaderboard"""
        if not self.game_mode or not self.difficulty:
            return
            
        # Create score entry
        score_entry = {
            "score": self.hud.score,
            "accuracy": self.hud.accuracy,
            "reaction_time": self.hud.reaction_time,
            "targets_hit": self.hud.targets_hit,
            "targets_missed": self.hud.targets_missed,
            "headshots": self.hud.headshots,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Add to scores
        if self.game_mode not in self.scores:
            self.scores[self.game_mode] = {}
            
        if self.difficulty not in self.scores[self.game_mode]:
            self.scores[self.game_mode][self.difficulty] = []
            
        self.scores[self.game_mode][self.difficulty].append(score_entry)
        
        # Sort scores by value (descending)
        self.scores[self.game_mode][self.difficulty].sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        if len(self.scores[self.game_mode][self.difficulty]) > 10:
            self.scores[self.game_mode][self.difficulty] = self.scores[self.game_mode][self.difficulty][:10]
            
        # Save to file
        save_json(self.scores, "scores.json")
        
        # Update leaderboard menu
        self.leaderboard_menu = LeaderboardMenu(self.scores)
        
    def get_high_score(self):
        """
        Get the high score for the current mode and difficulty
        
        Returns:
            int: High score or 0 if no scores
        """
        if not self.game_mode or not self.difficulty:
            return 0
            
        if self.game_mode not in self.scores:
            return 0
            
        if self.difficulty not in self.scores[self.game_mode]:
            return 0
            
        if not self.scores[self.game_mode][self.difficulty]:
            return 0
            
        return self.scores[self.game_mode][self.difficulty][0]["score"]
        
    def run(self):
        """Run the game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw the game
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
            
        # Clean up
        pygame.quit()
        sys.exit()
