"""
Menu system for the game
"""
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, VALORANT_RED, VALORANT_BLUE
from core.utils import draw_text

class Button:
    """
    Button class for menus
    """
    def __init__(self, x, y, width, height, text, font, action=None):
        """
        Initialize a button
        
        Args:
            x (int): X position
            y (int): Y position
            width (int): Button width
            height (int): Button height
            text (str): Button text
            font (pygame.font.Font): Font to use
            action (str, optional): Action to perform when clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        
    def update(self, mouse_pos):
        """
        Update the button state
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface):
        """
        Draw the button
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw the button background
        if self.hovered:
            pygame.draw.rect(surface, VALORANT_RED, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)
        else:
            pygame.draw.rect(surface, BLACK, self.rect)
            pygame.draw.rect(surface, VALORANT_RED, self.rect, 2)
            
        # Draw the button text
        text_color = WHITE
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """
        Handle mouse events
        
        Args:
            event (pygame.event.Event): Mouse event
            
        Returns:
            str or None: The button's action if clicked, None otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action
        return None


class MainMenu:
    """
    Main menu for the game
    """
    def __init__(self):
        """Initialize the main menu"""
        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 24)
        self.font_button = pygame.font.SysFont("arial", 20)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y_start = SCREEN_HEIGHT // 2
        button_spacing = 70
        
        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, 
                  "Start Training", self.font_button, "Start Training"),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, 
                  "Settings", self.font_button, "Settings"),
            Button(button_x, button_y_start + button_spacing * 2, button_width, button_height, 
                  "Leaderboard", self.font_button, "Leaderboard"),
            Button(button_x, button_y_start + button_spacing * 3, button_width, button_height, 
                  "Quit", self.font_button, "Quit")
        ]
        
    def update(self, mouse_pos):
        """
        Update the menu
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        for button in self.buttons:
            button.update(mouse_pos)
            
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Background is now drawn in the main game class
        
        # Draw title
        draw_text(surface, "NeuroShot", self.font_title, VALORANT_RED, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 20, "center")
        draw_text(surface, "Reflex Protocol", self.font_subtitle, VALORANT_BLUE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30, "center")
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Event to handle
            
        Returns:
            str or None: The action to perform, or None
        """
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action
        return None


class ModeSelectionMenu:
    """
    Menu for selecting game mode
    """
    def __init__(self):
        """Initialize the mode selection menu"""
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_button = pygame.font.SysFont("arial", 20)
        self.font_description = pygame.font.SysFont("arial", 16)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y_start = SCREEN_HEIGHT // 3
        button_spacing = 70
        
        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, 
                  "Flick", self.font_button, "Flick"),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, 
                  "Tracking", self.font_button, "Tracking"),
            Button(button_x, button_y_start + button_spacing * 2, button_width, button_height, 
                  "Switch", self.font_button, "Switch"),
            Button(button_x, button_y_start + button_spacing * 3, button_width, button_height, 
                  "Spike", self.font_button, "Spike"),
            Button(button_x, button_y_start + button_spacing * 4, button_width, button_height, 
                  "Back", self.font_button, "Back")
        ]
        
        # Mode descriptions
        self.descriptions = {
            "Flick": "Test your reaction time and precision by hitting targets that appear randomly.",
            "Tracking": "Keep your crosshair on moving targets for as long as possible.",
            "Switch": "Quickly switch between multiple targets in sequence.",
            "Spike": "Hit the core nodes while avoiding decoys, simulating spike defusal under pressure."
        }
        
        self.hovered_mode = None
        
    def update(self, mouse_pos):
        """
        Update the menu
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        self.hovered_mode = None
        for button in self.buttons:
            button.update(mouse_pos)
            if button.hovered and button.action != "Back":
                self.hovered_mode = button.action
            
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Background is now drawn in the main game class
        
        # Draw title
        draw_text(surface, "Select Training Mode", self.font_title, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6, "center")
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Draw mode description
        if self.hovered_mode:
            description = self.descriptions.get(self.hovered_mode, "")
            draw_text(surface, description, self.font_description, WHITE, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, "center")
            
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Event to handle
            
        Returns:
            str or None: The action to perform, or None
        """
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action
        return None


class DifficultyMenu:
    """
    Menu for selecting difficulty
    """
    def __init__(self, selected_mode):
        """
        Initialize the difficulty menu
        
        Args:
            selected_mode (str): The selected game mode
        """
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_mode = pygame.font.SysFont("arial", 24)
        self.font_button = pygame.font.SysFont("arial", 20)
        self.font_description = pygame.font.SysFont("arial", 16)
        
        self.selected_mode = selected_mode
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y_start = SCREEN_HEIGHT // 3
        button_spacing = 70
        
        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, 
                  "Easy", self.font_button, "Easy"),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, 
                  "Medium", self.font_button, "Medium"),
            Button(button_x, button_y_start + button_spacing * 2, button_width, button_height, 
                  "Hard", self.font_button, "Hard"),
            Button(button_x, button_y_start + button_spacing * 3, button_width, button_height, 
                  "Extreme", self.font_button, "Extreme"),
            Button(button_x, button_y_start + button_spacing * 4, button_width, button_height, 
                  "Back", self.font_button, "Back")
        ]
        
        # Difficulty descriptions
        self.descriptions = {
            "Easy": "Larger, slower targets with longer lifetimes. Perfect for beginners.",
            "Medium": "Balanced difficulty for regular practice.",
            "Hard": "Smaller, faster targets with shorter lifetimes. For experienced players.",
            "Extreme": "Tiny, very fast targets that disappear quickly. For elite players only."
        }
        
        self.hovered_difficulty = None
        
    def update(self, mouse_pos):
        """
        Update the menu
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        self.hovered_difficulty = None
        for button in self.buttons:
            button.update(mouse_pos)
            if button.hovered and button.action != "Back":
                self.hovered_difficulty = button.action
            
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Background is now drawn in the main game class
        
        # Draw title
        draw_text(surface, "Select Difficulty", self.font_title, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6, "center")
        
        # Draw selected mode
        draw_text(surface, f"Mode: {self.selected_mode.capitalize()}", self.font_mode, VALORANT_BLUE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 50, "center")
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Draw difficulty description
        if self.hovered_difficulty:
            description = self.descriptions.get(self.hovered_difficulty, "")
            draw_text(surface, description, self.font_description, WHITE, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, "center")
            
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Event to handle
            
        Returns:
            str or None: The action to perform, or None
        """
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action
        return None


class SettingsMenu:
    """
    Menu for game settings
    """
    def __init__(self, settings):
        """
        Initialize the settings menu
        
        Args:
            settings (dict): Current game settings
        """
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_option = pygame.font.SysFont("arial", 20)
        self.font_button = pygame.font.SysFont("arial", 20)
        
        self.settings = settings
        
        # Create buttons
        button_width = 200
        button_height = 40
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y_start = SCREEN_HEIGHT // 4
        button_spacing = 50
        
        # Toggle buttons
        self.buttons = [
            Button(button_x, button_y_start, button_width, button_height, 
                  f"Sound: {'On' if settings['sound_enabled'] else 'Off'}", 
                  self.font_button, "toggle_sound"),
            Button(button_x, button_y_start + button_spacing, button_width, button_height, 
                  f"Fullscreen: {'On' if settings['fullscreen'] else 'Off'}", 
                  self.font_button, "toggle_fullscreen"),
            Button(button_x, button_y_start + button_spacing * 2, button_width, button_height, 
                  f"Show FPS: {'On' if settings['show_fps'] else 'Off'}", 
                  self.font_button, "toggle_fps"),
            Button(button_x, button_y_start + button_spacing * 3, button_width, button_height, 
                  f"Show Stats: {'On' if settings['show_stats'] else 'Off'}", 
                  self.font_button, "toggle_stats"),
            Button(button_x, button_y_start + button_spacing * 4, button_width, button_height, 
                  "Crosshair: " + settings["crosshair_style"].capitalize(), 
                  self.font_button, "cycle_crosshair"),
            Button(button_x, button_y_start + button_spacing * 5, button_width, button_height, 
                  "Crosshair Color", self.font_button, "cycle_color"),
            Button(button_x, button_y_start + button_spacing * 6, button_width, button_height, 
                  "Save and Exit", self.font_button, "Save and Exit")
        ]
        
        # Color preview
        self.color_rect = pygame.Rect(button_x + button_width + 20, 
                                     button_y_start + button_spacing * 5, 
                                     30, 30)
        
    def update(self, mouse_pos):
        """
        Update the menu
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        for button in self.buttons:
            button.update(mouse_pos)
            
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Background is now drawn in the main game class
        
        # Draw title
        draw_text(surface, "Settings", self.font_title, WHITE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8, "center")
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Draw color preview
        pygame.draw.rect(surface, self.settings["crosshair_color"], self.color_rect)
        pygame.draw.rect(surface, WHITE, self.color_rect, 1)
            
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Event to handle
            
        Returns:
            str or None: The action to perform, or None
        """
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                if action == "toggle_sound":
                    self.settings["sound_enabled"] = not self.settings["sound_enabled"]
                    button.text = f"Sound: {'On' if self.settings['sound_enabled'] else 'Off'}"
                elif action == "toggle_fullscreen":
                    self.settings["fullscreen"] = not self.settings["fullscreen"]
                    button.text = f"Fullscreen: {'On' if self.settings['fullscreen'] else 'Off'}"
                elif action == "toggle_fps":
                    self.settings["show_fps"] = not self.settings["show_fps"]
                    button.text = f"Show FPS: {'On' if self.settings['show_fps'] else 'Off'}"
                elif action == "toggle_stats":
                    self.settings["show_stats"] = not self.settings["show_stats"]
                    button.text = f"Show Stats: {'On' if self.settings['show_stats'] else 'Off'}"
                elif action == "cycle_crosshair":
                    styles = ["default", "dot", "circle", "valorant"]
                    current_index = styles.index(self.settings["crosshair_style"])
                    next_index = (current_index + 1) % len(styles)
                    self.settings["crosshair_style"] = styles[next_index]
                    button.text = f"Crosshair: {styles[next_index].capitalize()}"
                elif action == "cycle_color":
                    colors = [
                        (255, 70, 85),    # VALORANT_RED
                        (18, 184, 253),   # VALORANT_BLUE
                        (255, 255, 255),  # WHITE
                        (0, 255, 0),      # GREEN
                        (255, 255, 0)     # YELLOW
                    ]
                    # Find the closest color in our list
                    current_color = self.settings["crosshair_color"]
                    current_index = 0
                    for i, color in enumerate(colors):
                        if color == current_color:
                            current_index = i
                            break
                    next_index = (current_index + 1) % len(colors)
                    self.settings["crosshair_color"] = colors[next_index]
                elif action == "Save and Exit":
                    return action
        return None


class LeaderboardMenu:
    """
    Menu for displaying leaderboard
    """
    def __init__(self, scores):
        """
        Initialize the leaderboard menu
        
        Args:
            scores (dict): Scores data
        """
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_header = pygame.font.SysFont("arial", 24)
        self.font_score = pygame.font.SysFont("arial", 18)
        self.font_button = pygame.font.SysFont("arial", 20)
        
        self.scores = scores
        self.current_mode = "flick"
        self.current_difficulty = "medium"
        
        # Get available modes and difficulties
        self.modes = list(scores.keys()) if scores else ["flick"]
        if not self.modes:
            self.modes = ["flick"]
        self.current_mode = self.modes[0]
        
        self.difficulties = list(scores.get(self.current_mode, {}).keys()) if scores else ["medium"]
        if not self.difficulties:
            self.difficulties = ["medium"]
        self.current_difficulty = self.difficulties[0] if self.difficulties else "medium"
        
        # Create buttons
        button_width = 150
        button_height = 40
        
        # Mode and difficulty selection buttons
        self.mode_button = Button(SCREEN_WIDTH // 4 - button_width // 2, 100, 
                                 button_width, button_height, 
                                 f"Mode: {self.current_mode.capitalize()}", 
                                 self.font_button, "cycle_mode")
        
        self.difficulty_button = Button(SCREEN_WIDTH * 3 // 4 - button_width // 2, 100, 
                                      button_width, button_height, 
                                      f"Difficulty: {self.current_difficulty.capitalize()}", 
                                      self.font_button, "cycle_difficulty")
        
        # Back button
        self.back_button = Button(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 100, 
                                 button_width, button_height, 
                                 "Back", self.font_button, "Back")
        
    def update(self, mouse_pos):
        """
        Update the menu
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        self.mode_button.update(mouse_pos)
        self.difficulty_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
            
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Background is now drawn in the main game class
        
        # Draw title
        draw_text(surface, "Leaderboard", self.font_title, WHITE, 
                 SCREEN_WIDTH // 2, 40, "center")
        
        # Draw buttons
        self.mode_button.draw(surface)
        self.difficulty_button.draw(surface)
        self.back_button.draw(surface)
        
        # Draw scores
        scores_list = self.get_scores()
        if scores_list:
            # Draw headers
            draw_text(surface, "Rank", self.font_header, WHITE, 
                     SCREEN_WIDTH // 6, 180, "center")
            draw_text(surface, "Score", self.font_header, WHITE, 
                     SCREEN_WIDTH * 2 // 6, 180, "center")
            draw_text(surface, "Accuracy", self.font_header, WHITE, 
                     SCREEN_WIDTH * 3 // 6, 180, "center")
            draw_text(surface, "Reaction", self.font_header, WHITE, 
                     SCREEN_WIDTH * 4 // 6, 180, "center")
            draw_text(surface, "Date", self.font_header, WHITE, 
                     SCREEN_WIDTH * 5 // 6, 180, "center")
            
            # Draw scores
            for i, score in enumerate(scores_list):
                y = 220 + i * 30
                draw_text(surface, f"#{i+1}", self.font_score, WHITE, 
                         SCREEN_WIDTH // 6, y, "center")
                draw_text(surface, str(score["score"]), self.font_score, WHITE, 
                         SCREEN_WIDTH * 2 // 6, y, "center")
                draw_text(surface, f"{score['accuracy']:.1f}%", self.font_score, WHITE, 
                         SCREEN_WIDTH * 3 // 6, y, "center")
                draw_text(surface, f"{score['reaction_time']:.0f}ms", self.font_score, WHITE, 
                         SCREEN_WIDTH * 4 // 6, y, "center")
                draw_text(surface, score["date"], self.font_score, WHITE, 
                         SCREEN_WIDTH * 5 // 6, y, "center")
        else:
            # No scores
            draw_text(surface, "No scores yet!", self.font_header, WHITE, 
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "center")
            
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Event to handle
            
        Returns:
            str or None: The action to perform, or None
        """
        # Mode button
        action = self.mode_button.handle_event(event)
        if action == "cycle_mode":
            # Cycle through available modes
            if self.modes:
                current_index = self.modes.index(self.current_mode)
                next_index = (current_index + 1) % len(self.modes)
                self.current_mode = self.modes[next_index]
                self.mode_button.text = f"Mode: {self.current_mode.capitalize()}"
                
                # Update difficulties for this mode
                self.difficulties = list(self.scores.get(self.current_mode, {}).keys())
                if not self.difficulties:
                    self.difficulties = ["medium"]
                self.current_difficulty = self.difficulties[0] if self.difficulties else "medium"
                self.difficulty_button.text = f"Difficulty: {self.current_difficulty.capitalize()}"
                
        # Difficulty button
        action = self.difficulty_button.handle_event(event)
        if action == "cycle_difficulty":
            # Cycle through available difficulties
            if self.difficulties:
                current_index = self.difficulties.index(self.current_difficulty)
                next_index = (current_index + 1) % len(self.difficulties)
                self.current_difficulty = self.difficulties[next_index]
                self.difficulty_button.text = f"Difficulty: {self.current_difficulty.capitalize()}"
                
        # Back button
        action = self.back_button.handle_event(event)
        if action:
            return action
            
        return None
        
    def get_scores(self):
        """
        Get scores for the current mode and difficulty
        
        Returns:
            list: List of score dictionaries
        """
        if not self.scores:
            return []
            
        mode_scores = self.scores.get(self.current_mode, {})
        if not mode_scores:
            return []
            
        difficulty_scores = mode_scores.get(self.current_difficulty, [])
        return difficulty_scores
