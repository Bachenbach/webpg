import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.max_health = max_health
        self.current_health = max_health
    
    def update(self, current_health):
        self.current_health = current_health
    
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Foreground
        health_width = (self.current_health / self.max_health) * self.width
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, health_width, self.height))
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

class UIManager:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        
        # Health bars
        self.player_health_bar = HealthBar(20, 20, 200, 20, self.game.player.max_health)
        
        # Boss health bar (only shown during boss fights)
        self.boss_health_bar = None
    
    def draw(self, screen):
        # Player health
        self.player_health_bar.update(self.game.player.health)
        self.player_health_bar.draw(screen)
        
        # Coins
        coin_text = self.font.render(f"Coins: {self.game.coins}", True, (255, 215, 0))
        screen.blit(coin_text, (20, 50))
        
        # Score
        score_text = self.font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 80))
        
        # Level
        level_text = self.font.render(f"Level: {self.game.current_level}", True, (255, 255, 255))
        screen.blit(level_text, (20, 110))
        
        # Weapon info
        weapon_text = self.font.render(
            f"Weapon: {self.game.player.current_weapon.name} (Lvl {self.game.player.current_weapon.upgrade_level})", 
            True, (200, 200, 200))
        screen.blit(weapon_text, (500, 20))
        
        # Boss health (if active)
        if hasattr(self.game, 'boss'):
            if not self.boss_health_bar:
                self.boss_health_bar = HealthBar(300, 20, 600, 30, self.game.boss.max_health)
            self.boss_health_bar.update(self.game.boss.health)
            self.boss_health_bar.draw(screen)
        
        # Shop button
        pygame.draw.rect(screen, (100, 100, 200), (1100, 20, 150, 40))
        shop_text = self.font.render("SHOP (E)", True, (255, 255, 255))
        screen.blit(shop_text, (1110, 30))
    
    def draw_pause_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.game.screen.blit(overlay, (0, 0))
        
        # Menu box
        pygame.draw.rect(self.game.screen, (50, 50, 80), (440, 240, 400, 300))
        
        # Title
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("PAUSED", True, (255, 255, 255))
        self.game.screen.blit(title, (520, 260))
        
        # Buttons
        button_font = pygame.font.SysFont(None, 48)
        
        # Resume button
        pygame.draw.rect(self.game.screen, (100, 200, 100), (490, 350, 300, 60))
        resume_text = button_font.render("RESUME", True, (255, 255, 255))
        self.game.screen.blit(resume_text, (550, 365))
        
        # Quit button
        pygame.draw.rect(self.game.screen, (200, 100, 100), (490, 430, 300, 60))
        quit_text = button_font.render("QUIT", True, (255, 255, 255))
        self.game.screen.blit(quit_text, (580, 445))