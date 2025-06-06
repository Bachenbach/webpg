import pygame
import random

class Enemy:
    def __init__(self, game, x, y, enemy_type):
        self.game = game
        self.x, self.y = x, y
        self.type = enemy_type
        self.width, self.height = 50, 50
        self.vel_x, self.vel_y = 0, 0
        
        # Enemy stats
        self.stats = {
            "basic": {"health": 30, "speed": 2, "damage": 10, "coin_value": 5, "score_value": 100},
            "flying": {"health": 20, "speed": 3, "damage": 5, "coin_value": 3, "score_value": 150},
            "tank": {"health": 100, "speed": 1, "damage": 20, "coin_value": 10, "score_value": 200}
        }
        
        self.health = self.stats[enemy_type]["health"]
        self.max_health = self.health
        self.speed = self.stats[enemy_type]["speed"]
        self.damage = self.stats[enemy_type]["damage"]
        self.coin_value = self.stats[enemy_type]["coin_value"]
        self.score_value = self.stats[enemy_type]["score_value"]
        
        # AI behavior
        self.direction = random.choice([-1, 1])
        self.move_timer = 0
        self.attack_cooldown = 0
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Different behaviors based on type
        if self.type == "basic":
            self.vel_x = self.direction * self.speed
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.direction *= -1
                self.move_timer = random.randint(60, 180)
            
            # Simple platform collision
            self.x += self.vel_x
            for platform in self.game.level.platforms:
                if (self.x <= platform.x + platform.width and 
                    self.x + self.width >= platform.x and
                    self.y + self.height >= platform.y and 
                    self.y < platform.y):
                    self.y = platform.y - self.height
                    self.vel_y = 0
                elif (self.x + self.width > platform.x + platform.width or 
                      self.x < platform.x) and self.move_timer <= 0:
                    self.direction *= -1
                    self.move_timer = random.randint(60, 180)
        
        elif self.type == "flying":
            # Fly towards player
            if self.game.player.x < self.x:
                self.vel_x = -self.speed
            else:
                self.vel_x = self.speed
                
            if self.game.player.y < self.y:
                self.vel_y = -self.speed
            else:
                self.vel_y = self.speed
                
            self.x += self.vel_x
            self.y += self.vel_y
        
        # Check collision with player
        if (abs(self.game.player.x - self.x) < self.width and 
            abs(self.game.player.y - self.y) < self.height and 
            self.attack_cooldown == 0):
            self.game.player.take_damage(self.damage)
            self.attack_cooldown = 60
    
    def take_damage(self, amount):
        self.health -= amount
    
    def draw(self, screen):
        # Draw enemy (rectangle for now)
        if self.type == "basic":
            color = (200, 50, 50)  # Red
        elif self.type == "flying":
            color = (50, 50, 200)  # Blue
        else:
            color = (150, 50, 150)  # Purple
            
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 15, self.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 15, self.width * health_ratio, 5))

class Boss(Enemy):
    def __init__(self, game, x, y, boss_type):
        super().__init__(game, x, y, "tank")  # Inherit from tank stats
        self.boss_type = boss_type
        self.width, self.height = 100, 100
        self.health = 500
        self.max_health = self.health
        self.phase = 1
        self.attack_pattern = 0
        self.pattern_timer = 0
        
        # Boss-specific attacks
        self.projectiles = []
    
    def update(self):
        # Boss AI with different phases
        if self.health < self.max_health * 0.3:
            self.phase = 3
        elif self.health < self.max_health * 0.6:
            self.phase = 2
        else:
            self.phase = 1
            
        # Different behaviors per phase
        if self.phase == 1:
            # Simple movement
            if self.game.player.x < self.x:
                self.vel_x = -self.speed
            else:
                self.vel_x = self.speed
                
            self.x += self.vel_x
            
            # Basic attack
            if self.pattern_timer <= 0:
                self.perform_attack()
                self.pattern_timer = 120
            else:
                self.pattern_timer -= 1
                
        elif self.phase == 2:
            # More aggressive
            self.speed = 2
            if self.pattern_timer <= 0:
                self.attack_pattern = (self.attack_pattern + 1) % 3
                self.perform_attack()
                self.pattern_timer = 90
            else:
                self.pattern_timer -= 1
                
        elif self.phase == 3:
            # Final phase - very aggressive
            self.speed = 3
            if self.pattern_timer <= 0:
                self.attack_pattern = random.randint(0, 4)
                self.perform_attack()
                self.pattern_timer = 60
            else:
                self.pattern_timer -= 1
        
        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if proj.lifetime <= 0:
                self.projectiles.remove(proj)
    
    def perform_attack(self):
        if self.attack_pattern == 0:
            # Single powerful shot
            pass
        elif self.attack_pattern == 1:
            # Spread shot
            pass
        elif self.attack_pattern == 2:
            # Circular pattern
            pass
    
    def draw(self, screen):
        # Draw boss (bigger rectangle)
        color = (180, 50, 180)  # Purple
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 50, self.y - 30, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 50, self.y - 30, 200 * health_ratio, 20))
        
        # Draw phase indicator
        phase_text = f"Phase {self.phase}"
        font = pygame.font.SysFont(None, 30)
        text = font.render(phase_text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 50))