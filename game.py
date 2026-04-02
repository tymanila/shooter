import sys
from random import randint

from pygame import *
window = display.set_mode((700,500))
display.set_caption('стреляка')


class GameSprite(sprite.Sprite):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(filename), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x +=  self.speed
    def shoot(self):
        bullet = Bullet('bullet.png', 15, 15, self.rect.x + 30, self.rect.y, 5)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.kill()
            missed += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

background = GameSprite("galaxy.jpg", 700,500, 0, 0, 0)
player = Player("rocket.png", 80, 80, 400, 400, 5)
count = 0
clock = time.Clock()
enemies = sprite.Group()
for i in range(3):
    enemy = Enemy('ufo.png', 100, 70, randint(0, 600), -100, randint(2, 4))
    enemies.add(enemy)
font.init()
font = font.Font(None, 70)
win = font.render('You Won', True, (0, 255, 0))
loose = font.render('You Lose', True, (255, 0, 0))
bullets = sprite.Group()
game_over = False
missed = 0
while True:
    background.draw()
    player.draw()
    player.update()
    enemies.draw(window)
    enemies.update()
    bullets.draw(window)
    bullets.update()
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()


    collides = sprite.groupcollide(bullets, enemies, True, True)
    for c in collides:
        enemy = Enemy('ufo.png', 100, 70, randint(0, 600), -100, randint(2, 4))
        enemies.add(enemy)
        count += 1
    score = font.render('счет: ' + str(count), True, (255, 255, 255))
    window.blit(score, (10, 10))
    missed_text = font.render('пропущено: ' + str(missed), True, (255, 255, 255))
    window.blit(missed_text, (10, 100))



    if count > 25:
        window.blit(win, (220, 220))
        for e in enemies:
            e.kill()
        player.speed = 0

    

    if sprite.spritecollide(player, enemies,  False) or missed > 2:
        game_over =  True
    if game_over:
        window.blit(loose, (220, 220))
        for e in enemies:
            e.kill()
        player.speed = 0
    clock.tick(60)
    display.update()

#vbruve
