import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, color=(150, 150, 150)):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Checkpoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 40, 80
        self.active = False
        self.color = (0, 255, 255)  # Cyan
    
    def draw(self, screen):
        color = (0, 200, 200) if self.active else (0, 150, 150)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

class Level:
    def __init__(self, game):
        self.game = game
        self.platforms = []
        self.checkpoints = []
        self.background_color = (30, 30, 50)
        self.load("level_1")
    
    def load(self, level_name):
        self.platforms = []
        self.checkpoints = []
        
        # Base platform
        self.platforms.append(Platform(0, 650, 1280, 70))
        
        # Level-specific platforms
        if level_name == "level_1":
            self._load_level_1()
        elif level_name == "level_2":
            self._load_level_2()
        elif level_name == "boss_1":
            self._load_boss_level()
    
    def _load_level_1(self):
        # Simple platforms
        self.platforms.append(Platform(200, 550, 200, 20))
        self.platforms.append(Platform(500, 450, 200, 20))
        self.platforms.append(Platform(800, 350, 200, 20))
        
        # Checkpoint
        self.checkpoints.append(Checkpoint(900, 570))
    
    def _load_level_2(self):
        # More complex layout
        self.platforms.append(Platform(150, 600, 150, 20))
        self.platforms.append(Platform(350, 500, 150, 20))
        self.platforms.append(Platform(550, 400, 150, 20))
        self.platforms.append(Platform(750, 500, 150, 20))
        self.platforms.append(Platform(950, 600, 150, 20))
        
        # Moving platform
        self.moving_platform = Platform(400, 300, 150, 20, (200, 100, 100))
        self.platforms.append(self.moving_platform)
        self.moving_direction = 1
        
        # Checkpoints
        self.checkpoints.append(Checkpoint(200, 580))
        self.checkpoints.append(Checkpoint(1000, 580))
    
    def _load_boss_level(self):
        # Arena-style level for boss fights
        self.platforms.append(Platform(0, 700, 1280, 20))
        self.platforms.append(Platform(100, 600, 200, 20))
        self.platforms.append(Platform(980, 600, 200, 20))
        
        # Central platform
        self.platforms.append(Platform(540, 500, 200, 20, (200, 50, 50)))
    
    def update(self):
        # Update moving platforms
        if hasattr(self, 'moving_platform'):
            self.moving_platform.x += 2 * self.moving_direction
            if self.moving_platform.x > 800 or self.moving_platform.x < 200:
                self.moving_direction *= -1
        
        # Check checkpoints
        for checkpoint in self.checkpoints:
            player = self.game.player
            if (player.x + player.width > checkpoint.x and 
                player.x < checkpoint.x + checkpoint.width and
                player.y + player.height > checkpoint.y and 
                player.y < checkpoint.y + checkpoint.height):
                checkpoint.active = True
                self.game.checkpoint_position = (checkpoint.x, checkpoint.y - 50)
    
    def draw(self, screen):
        # Draw background
        screen.fill(self.background_color)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.draw(screen)