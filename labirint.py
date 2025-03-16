from pygame import *

# Переменные
win_w = 850
win_h = 850
p_speed = 5
n_speed = -5
back = (192, 209, 229)

# Классы
class GameSprite(sprite.Sprite):    # Класс для всех справйтов в этой игре
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):    # Класс для спрайта игрока
    def __init__(self, picture, w, h, x, y, x_speed=0, y_speed=0):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        # Движение по горизонтали
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(player, walls, False)
        if self.x_speed > 0: # Вправо
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: # Влево
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        # Движение по вертикали
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(player, walls, False)
        if self.y_speed > 0: # Вниз
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # Вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self): # Стрелять
        bullet = Bullet('Star.png', 20, 15, self.rect.right, self.rect.centery-20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):    # Класс для спрайта врага
    def __init__(self, picture, w, h, x, y, speed, direction='right'):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = direction
    def update(self):
        if self.rect.x <= 10:
            self.direction = 'right'
        if self.rect.x >= win_w - 110:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):   # Класс для спрайтов пуль
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        sprite.groupcollide(bullets, walls, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        self.rect.x += self.speed
        if self.rect.x > win_w:
            self.kill()

# Создание окна
window = display.set_mode((win_w, win_h))
display.set_caption('Игрулька на питончике')

# Спрайты и группы
player = Player('Dasha.png', 89, 165, 5, win_h-170)
monster1 = Enemy('Ebardo.png', 100, 165, 10, 240, 5)
monsters = sprite.Group()
monsters.add(monster1)
w1 = GameSprite('Wall_h.jpg', 213, 40, 0, 405)
w2 = GameSprite('Wall_h.jpg', 213, 40, 425, 405)
w3 = GameSprite('Wall_h.jpg', 213, 40, 638, 405)
w4 = GameSprite('Wall_h.jpg', 213, 40, 213, 618)
w5 = GameSprite('Wall_h.jpg', 213, 40, 425, 618)
w6 = GameSprite('Wall_h.jpg', 213, 40, 213, 193)
w7 = GameSprite('Wall_h.jpg', 213, 40, 425, 193)
w8 = GameSprite('Wall_v.jpg', 40, 213, 598, 638)
w9 = GameSprite('Wall_v.jpg', 40, 213, 213, 0)
walls = sprite.Group()
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
bullets = sprite.Group()
final = GameSprite('Finish.png', 75, 75, 318, 65)
win = transform.scale(image.load('thumb.jpg'), (win_w, win_h))
lose = transform.scale(image.load('game-over_1.png'), (win_w, win_h))

# Игровой цикл
run = True
finish = False
while run:
    for e in event.get():
        # Нажатие на "Закрыть"
        if e.type == QUIT:
            run = False
        # Нажатие клавиши
        elif e.type == KEYDOWN:
            if e.key == K_w or e.key == K_UP:
                player.y_speed = n_speed
            elif e.key == K_s or e.key == K_DOWN:
                player.y_speed = p_speed
            elif e.key == K_a or e.key == K_LEFT:
                player.x_speed = n_speed
            elif e.key == K_d or e.key == K_RIGHT:
                player.x_speed = p_speed
            elif e.key == K_SPACE:
                player.fire()
        # Отжатие клавиши
        elif e.type == KEYUP:
            if e.key == K_w or e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_s or e.key == K_DOWN:
                player.y_speed = 0
            elif e.key == K_a or e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_d or e.key == K_RIGHT:
                player.x_speed = 0
    if finish == False:
        window.fill(back)
        bullets.update()
        bullets.draw(window)
        walls.draw(window)
        final.reset()
        player.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0, 0))
        monsters_touched = sprite.spritecollide(player, monsters, False)
        for m in monsters_touched:
            if sprite.collide_rect(player, m):
                finish = True
                window.blit(lose, (0, 0))
    time.delay(50)
    display.update()
