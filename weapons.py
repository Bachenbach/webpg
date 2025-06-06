import pygame

class Weapon:
    def __init__(self, name, damage, speed, cooldown, bullet_size=10, bullet_color=(255, 255, 0)):
        self.name = name
        self.damage = damage
        self.speed = speed
        self.cooldown = cooldown
        self.bullet_size = bullet_size
        self.bullet_color = bullet_color
        self.upgrade_level = 1
        self.price = 100 * self.upgrade_level
    
    def shoot(self, game, x, y, facing_right):
        direction = 1 if facing_right else -1
        bullet_x = x + 40 if facing_right else x - 10
        bullet = Projectile(bullet_x, y + 25, direction * self.speed, 0, 
                           self.damage, self.bullet_size, self.bullet_color)
        game.projectiles.append(bullet)
    
    def upgrade(self):
        self.upgrade_level += 1
        self.damage += 5
        self.cooldown = max(5, self.cooldown - 2)
        self.price = 100 * self.upgrade_level

class Projectile:
    def __init__(self, x, y, vel_x, vel_y, damage, size, color):
        self.x, self.y = x, y
        self.vel_x, self.vel_y = vel_x, vel_y
        self.damage = damage
        self.size = size
        self.color = color
        self.lifetime = 180  # Frames before disappearing
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class WeaponShop:
    def __init__(self, game):
        self.game = game
        self.weapons = [
            Weapon("Pistol", 10, 10, 20),
            Weapon("Shotgun", 15, 8, 30, 15, (255, 150, 0)),
            Weapon("Rifle", 8, 15, 10, 5, (0, 255, 255)),
            Weapon("Rocket Launcher", 30, 5, 60, 20, (255, 0, 0))
        ]
        self.active = False
    
    def toggle_shop(self):
        self.active = not self.active
    
    def buy_weapon(self, weapon_index):
        weapon = self.weapons[weapon_index]
        if self.game.coins >= weapon.price:
            self.game.coins -= weapon.price
            self.game.player.weapons.append(weapon)
            self.game.player.current_weapon = weapon
            return True
        return False
    
    def upgrade_weapon(self, weapon_index):
        if weapon_index < len(self.game.player.weapons):
            weapon = self.game.player.weapons[weapon_index]
            if self.game.coins >= weapon.price:
                self.game.coins -= weapon.price
                weapon.upgrade()
                return True
        return False
    
    def draw(self, screen):
        if not self.active:
            return
            
        # Draw shop background
        pygame.draw.rect(screen, (50, 50, 80), (300, 200, 680, 320))
        
        # Draw title
        font = pygame.font.SysFont(None, 48)
        title = font.render("WEAPON SHOP", True, (255, 255, 255))
        screen.blit(title, (500, 220))
        
        # Draw coins
        coin_text = font.render(f"Coins: {self.game.coins}", True, (255, 215, 0))
        screen.blit(coin_text, (320, 220))
        
        # Draw weapons for sale
        font = pygame.font.SysFont(None, 36)
        for i, weapon in enumerate(self.weapons):
            y_pos = 270 + i * 60
            color = (0, 255, 0) if self.game.coins >= weapon.price else (255, 0, 0)
            
            weapon_text = font.render(
                f"{weapon.name} - Damage: {weapon.damage} - Cooldown: {weapon.cooldown} - Price: {weapon.price}", 
                True, color)
            screen.blit(weapon_text, (320, y_pos))
            
            # Draw buy button
            pygame.draw.rect(screen, (100, 100, 150), (900, y_pos, 60, 30))
            buy_text = font.render("Buy", True, (255, 255, 255))
            screen.blit(buy_text, (910, y_pos))
        
        # Draw close button
        pygame.draw.rect(screen, (200, 50, 50), (500, 500, 120, 40))
        close_text = font.render("CLOSE", True, (255, 255, 255))
        screen.blit(close_text, (530, 510))