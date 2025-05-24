"""
Target entity for the game
"""
import random
import pygame
from core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_SIZE_MIN, TARGET_SIZE_MAX,
    TARGET_SPEED_MIN, TARGET_SPEED_MAX, TARGET_LIFETIME_MIN, TARGET_LIFETIME_MAX
)

class Target(pygame.sprite.Sprite):
    """
    Target class for the game
    """
    def __init__(self, target_type="standard", size=None, lifetime=None, speed=None):
        """
        Initialize a target
        
        Args:
            target_type (str): Type of target ("standard", "headshot", "decoy")
            size (int, optional): Size of the target
            lifetime (int, optional): Lifetime of the target in milliseconds
            speed (float, optional): Movement speed of the target
        """
        super().__init__()
        
        # Set target properties
        self.type = target_type
        self.size = size if size else random.randint(TARGET_SIZE_MIN, TARGET_SIZE_MAX)
        self.lifetime = lifetime if lifetime else random.randint(TARGET_LIFETIME_MIN, TARGET_LIFETIME_MAX)
        self.speed = speed if speed else random.uniform(TARGET_SPEED_MIN, TARGET_SPEED_MAX)
        
        # Create the target surface
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_target()
        
        # Set up the rect and position
        self.rect = self.image.get_rect()
        self.spawn()
        
        # Movement
        self.velocity = pygame.Vector2(
            random.uniform(-self.speed, self.speed),
            random.uniform(-self.speed, self.speed)
        )
        
        # Timing
        self.spawn_time = pygame.time.get_ticks()
        self.time_alive = 0
        self.hit = False
        self.hit_time = 0
        
        # Tracking mode variables
        self.tracked = False
        self.track_start_time = 0
        self.total_tracked_time = 0
        
    def draw_target(self):
        """Draw the target based on its type"""
        if self.type == "standard":
            # Outer ring
            pygame.draw.circle(self.image, (255, 70, 85), (self.size // 2, self.size // 2), self.size // 2)
            # Inner ring
            pygame.draw.circle(self.image, (255, 255, 255), (self.size // 2, self.size // 2), self.size // 3)
            # Center
            pygame.draw.circle(self.image, (255, 70, 85), (self.size // 2, self.size // 2), self.size // 6)
        
        elif self.type == "headshot":
            # Outer ring
            pygame.draw.circle(self.image, (255, 215, 0), (self.size // 2, self.size // 2), self.size // 2)
            # Inner ring
            pygame.draw.circle(self.image, (255, 255, 255), (self.size // 2, self.size // 2), self.size // 3)
            # Center
            pygame.draw.circle(self.image, (255, 215, 0), (self.size // 2, self.size // 2), self.size // 6)
        
        elif self.type == "decoy":
            # Outer ring
            pygame.draw.circle(self.image, (100, 100, 100), (self.size // 2, self.size // 2), self.size // 2)
            # Inner ring
            pygame.draw.circle(self.image, (150, 150, 150), (self.size // 2, self.size // 2), self.size // 3)
            # Center
            pygame.draw.circle(self.image, (200, 200, 200), (self.size // 2, self.size // 2), self.size // 6)
            
        elif self.type == "switch":
            # Highlighted target for switch mode
            pygame.draw.circle(self.image, (0, 255, 255), (self.size // 2, self.size // 2), self.size // 2)
            pygame.draw.circle(self.image, (255, 255, 255), (self.size // 2, self.size // 2), self.size // 3)
            pygame.draw.circle(self.image, (0, 255, 255), (self.size // 2, self.size // 2), self.size // 6)
            
        elif self.type == "spike":
            # Core node for spike mode
            pygame.draw.circle(self.image, (18, 184, 253), (self.size // 2, self.size // 2), self.size // 2)
            # Draw a hexagon pattern
            points = []
            for i in range(6):
                angle = i * (360 / 6)
                x = self.size // 2 + int((self.size // 3) * pygame.math.Vector2(1, 0).rotate(angle).x)
                y = self.size // 2 + int((self.size // 3) * pygame.math.Vector2(1, 0).rotate(angle).y)
                points.append((x, y))
            pygame.draw.polygon(self.image, (255, 255, 255), points)
            pygame.draw.circle(self.image, (18, 184, 253), (self.size // 2, self.size // 2), self.size // 6)
    
    def spawn(self):
        """Spawn the target at a random position on the screen"""
        # Ensure the target is fully visible on screen
        padding = self.size
        self.rect.x = random.randint(padding, SCREEN_WIDTH - padding)
        self.rect.y = random.randint(padding, SCREEN_HEIGHT - padding)
        
    def update(self):
        """Update the target's position and check if it should be removed"""
        current_time = pygame.time.get_ticks()
        self.time_alive = current_time - self.spawn_time
        
        # Move the target if it hasn't been hit
        if not self.hit:
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y
            
            # Bounce off the edges of the screen
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.velocity.x *= -1
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.velocity.y *= -1
                
        # Check if the target should be removed due to lifetime
        if self.time_alive >= self.lifetime:
            self.kill()
            
    def get_hit(self):
        """Mark the target as hit and record the hit time"""
        if not self.hit:
            self.hit = True
            self.hit_time = pygame.time.get_ticks()
            return True
        return False
    
    def get_reaction_time(self):
        """Calculate the reaction time for hitting this target"""
        if self.hit:
            return self.hit_time - self.spawn_time
        return 0
    
    def start_tracking(self):
        """Start tracking this target (for tracking mode)"""
        if not self.tracked:
            self.tracked = True
            self.track_start_time = pygame.time.get_ticks()
    
    def stop_tracking(self):
        """Stop tracking this target (for tracking mode)"""
        if self.tracked:
            self.tracked = False
            current_time = pygame.time.get_ticks()
            self.total_tracked_time += current_time - self.track_start_time
            
    def get_tracking_percentage(self):
        """Calculate the percentage of time this target was tracked"""
        if self.time_alive == 0:
            return 0
            
        # Add current tracking time if still being tracked
        total_time = self.total_tracked_time
        if self.tracked:
            current_time = pygame.time.get_ticks()
            total_time += current_time - self.track_start_time
            
        return (total_time / self.time_alive) * 100


class TargetManager:
    """
    Manages the creation, updating, and removal of targets
    """
    def __init__(self, game_mode, difficulty="medium"):
        """
        Initialize the target manager
        
        Args:
            game_mode (str): The current game mode
            difficulty (str): Difficulty level
        """
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.targets = pygame.sprite.Group()
        self.last_spawn_time = 0
        self.spawn_delay = TARGET_LIFETIME_MIN  # Will be adjusted based on difficulty
        self.adjust_difficulty(difficulty)
        
        # Stats
        self.targets_spawned = 0
        self.targets_hit = 0
        self.targets_missed = 0
        self.headshots = 0
        self.reaction_times = []
        
    def adjust_difficulty(self, difficulty):
        """
        Adjust target parameters based on difficulty
        
        Args:
            difficulty (str): Difficulty level
        """
        from core.settings import DIFFICULTY_MODIFIERS
        
        self.difficulty = difficulty
        modifiers = DIFFICULTY_MODIFIERS.get(difficulty, DIFFICULTY_MODIFIERS["medium"])
        
        # Adjust spawn rate based on difficulty
        self.spawn_delay = int(TARGET_LIFETIME_MIN * modifiers["spawn_rate_multiplier"])
        
    def spawn_target(self, target_type=None):
        """
        Spawn a new target
        
        Args:
            target_type (str, optional): Type of target to spawn
        """
        from core.settings import DIFFICULTY_MODIFIERS, MAX_TARGETS
        
        # Don't spawn if we've reached the maximum number of targets
        if len(self.targets) >= MAX_TARGETS:
            return
            
        modifiers = DIFFICULTY_MODIFIERS.get(self.difficulty, DIFFICULTY_MODIFIERS["medium"])
        
        # Determine target type based on game mode if not specified
        if target_type is None:
            if self.game_mode == "flick":
                # 20% chance for headshot target in flick mode
                target_type = "headshot" if random.random() < 0.2 else "standard"
            elif self.game_mode == "tracking":
                target_type = "standard"
            elif self.game_mode == "switch":
                target_type = "switch"
            elif self.game_mode == "spike":
                # 70% chance for decoy, 30% chance for spike target
                target_type = "spike" if random.random() < 0.3 else "decoy"
            else:
                target_type = "standard"
                
        # Create the target with difficulty-adjusted parameters
        size = int(random.randint(TARGET_SIZE_MIN, TARGET_SIZE_MAX) * modifiers["target_size_multiplier"])
        lifetime = int(random.randint(TARGET_LIFETIME_MIN, TARGET_LIFETIME_MAX) * modifiers["target_lifetime_multiplier"])
        speed = random.uniform(TARGET_SPEED_MIN, TARGET_SPEED_MAX) * modifiers["target_speed_multiplier"]
        
        target = Target(target_type, size, lifetime, speed)
        self.targets.add(target)
        self.targets_spawned += 1
        
        return target
        
    def update(self):
        """Update all targets and spawn new ones if needed"""
        current_time = pygame.time.get_ticks()
        
        # Spawn new targets based on spawn rate
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_target()
            self.last_spawn_time = current_time
            
        # Update all targets
        self.targets.update()
        
    def draw(self, surface):
        """
        Draw all targets on the surface
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        self.targets.draw(surface)
        
    def check_hit(self, pos, hit_radius=0):
        """
        Check if a position hits any target
        
        Args:
            pos (tuple): Position to check (x, y)
            hit_radius (int): Additional radius to make hit detection more forgiving
            
        Returns:
            Target or None: The hit target or None if no target was hit
        """
        for target in self.targets:
            # Calculate distance from position to target center
            target_center = target.rect.center
            distance = pygame.math.Vector2(pos[0] - target_center[0], pos[1] - target_center[1]).length()
            
            # Check if the position is within the target radius plus the hit radius
            if distance <= (target.size / 2) + hit_radius and not target.hit:
                target.get_hit()
                
                # Record stats
                self.targets_hit += 1
                self.reaction_times.append(target.get_reaction_time())
                
                if target.type == "headshot":
                    self.headshots += 1
                    
                return target
                
        # No target was hit
        self.targets_missed += 1
        return None
        
    def get_accuracy(self):
        """
        Calculate the current accuracy
        
        Returns:
            float: Accuracy percentage (0-100)
        """
        total_shots = self.targets_hit + self.targets_missed
        if total_shots == 0:
            return 0
        return (self.targets_hit / total_shots) * 100
        
    def get_avg_reaction_time(self):
        """
        Calculate the average reaction time
        
        Returns:
            float: Average reaction time in milliseconds
        """
        if not self.reaction_times:
            return 0
        return sum(self.reaction_times) / len(self.reaction_times)
        
    def reset_stats(self):
        """Reset all statistics"""
        self.targets_spawned = 0
        self.targets_hit = 0
        self.targets_missed = 0
        self.headshots = 0
        self.reaction_times = []
        
    def clear_targets(self):
        """Remove all targets"""
        self.targets.empty()
