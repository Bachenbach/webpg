import pygame
import sys
from game.player import Player  # Changed from relative to absolute
from game.enemies import Enemy, Boss
from game.levels import Level
from game.weapons import Weapon, WeaponShop
from game.ui import HealthBar, UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Advanced Platformer")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_paused = False
        
        # Game systems
        self.level = Level(self)
        self.player = Player(self, 100, 500)
        self.weapon_shop = WeaponShop(self)
        self.ui = UIManager(self)
        
        # Game state
        self.current_level = 1
        self.coins = 0
        self.score = 0
        self.checkpoint_position = (100, 500)
        
        # Game objects
        self.projectiles = []
        self.enemies = []
        
        # Load first level
        self.load_level(self.current_level)
    
    def load_level(self, level_num):
        self.level.load(f"level_{level_num}")
        self.player.reset_position(*self.checkpoint_position)
        self.spawn_enemies()
        
        if level_num % 3 == 0:
            self.spawn_boss()
        
        self.projectiles = []
    
    def spawn_enemies(self):
        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy(self, 300 + i*150, 600, "basic"))
        
        if self.current_level > 1:
            for i in range(3):
                self.enemies.append(Enemy(self, 200 + i*200, 300, "flying"))
    
    def spawn_boss(self):
        self.boss = Boss(self, 800, 400, f"boss_{self.current_level//3}")
        self.enemies.append(self.boss)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_paused = not self.game_paused
                if event.key == pygame.K_SPACE and not self.game_paused:
                    self.player.shoot()
                if event.key == pygame.K_e and not self.game_paused:
                    self.weapon_shop.toggle_shop()
    
    def update(self):
        if self.game_paused:
            return
            
        self.player.update()
        
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.health <= 0:
                self.coins += enemy.coin_value
                self.score += enemy.score_value
                self.enemies.remove(enemy)
        
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)
        
        self.level.update()
        
        if len(self.enemies) == 0 and not hasattr(self, 'boss'):
            self.current_level += 1
            self.load_level(self.current_level)
    
    def render(self):
        self.screen.fill((30, 30, 40))
        self.level.draw(self.screen)
        
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        self.ui.draw(self.screen)
        
        if self.game_paused:
            self.ui.draw_pause_menu()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()