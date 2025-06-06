import pygame
from game.weapons import Weapon  

class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x, self.y = x, y
        self.width, self.height = 40, 60
        self.vel_x, self.vel_y = 0, 0
        self.jump_power = -15
        self.speed = 5
        self.gravity = 0.8
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.double_jump = False
        self.double_jump_available = True
        self.facing_right = True
        
        # Weapons
        self.current_weapon = Weapon("pistol", 10, 500, 10)
        self.weapons = [self.current_weapon]
        
        # Cooldowns
        self.shoot_cooldown = 0
    
    def update(self):
        # Movement
        keys = pygame.key.get_pressed()
        
        # Left/Right movement
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            
        # Jumping
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.double_jump_available = True
        elif keys[pygame.K_w] and self.double_jump and self.double_jump_available:
            self.vel_y = self.jump_power * 0.8
            self.double_jump_available = False
        
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check for collisions with platforms
        self.on_ground = False
        for platform in self.game.level.platforms:
            if (self.y + self.height >= platform.y and 
                self.y < platform.y and
                self.x + self.width > platform.x and 
                self.x < platform.x + platform.width):
                self.y = platform.y - self.height
                self.vel_y = 0
                self.on_ground = True
        
        # Check for falling off screen
        if self.y > self.game.screen_height:
            self.health = 0
        
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            self.current_weapon.shoot(self.game, self.x, self.y, self.facing_right)
            self.shoot_cooldown = self.current_weapon.cooldown
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.game_over()
    
    def draw(self, screen):
        # Draw player (rectangle for now)
        color = (100, 200, 100)  # Green
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Draw weapon
        weapon_x = self.x + self.width if self.facing_right else self.x - 20
        pygame.draw.rect(screen, (150, 150, 150), (weapon_x, self.y + 20, 30, 10))
        
        # Draw health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, self.width, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, self.width * health_ratio, 10))
    
    def reset_position(self):
        self.x, self.y = 100, 500
        self.vel_x, self.vel_y = 0, 0