#Создай собственный Шутер!
import time as tm
from random import *
from typing import Any
from pygame import *

dlene = 500
sherene = 700
window = display.set_mode((sherene, dlene))

lost = 0
points = 0

class GameSprite(sprite.Sprite):
    def __init__(self,x, y, png, speed):
        super().__init__()
        self.png = transform.scale(image.load(png), (70,70))
        self.rect = self.png.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        global window
        window.blit(self.png, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed


class Enemy(GameSprite):
    def __init__(self, x, y, png, speed):
        super().__init__(x, y, png, speed)
        self.ast = png == 'asteroid.png'
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > dlene:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, sherene-70)



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < sherene - 70:
            self.rect.x += self.speed

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 50)
text_lose = font1.render(
    "Пропущено: " + str(lost), 1, (205, 255, 255)
    )


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
clock = time.Clock()

back = transform.scale(image.load('galaxy.jpg'), (sherene, dlene))

rocket = Player(sherene/2, dlene-70, 'rocket.png', 7)

bullets = []
num_b = 5
start_reload = 0

enemies = []
for i in range(5):
    En1 = Enemy(randint(0, sherene-70), 0, 'ufo.png', 2)
    enemies.append(En1)
En1 = Enemy(randint(0, sherene-70), 0, 'asteroid.png', 2)
enemies.append(En1)

text_reload = font1.render("", 1, (255, 0, 0))

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and num_b: 
                bullets.append(Bullet(rocket.rect.x, rocket.rect.y, 'bullet.png', 3 ))
                fire.play()
                num_b -= 1
                if not num_b:
                    start_reload = tm.time()
            if not num_b:  
                if tm.time() - start_reload >= 3:
                    num_b = 5 
                    print(tm.time() - start_reload >= 3) 
                    text_reload = font1.render("", 1, (255, 0, 0))
                else:     
                    text_reload = font1.render(
                    "wait, reload...", 1, (200, 0, 0))


    text_lose = font1.render(
    "Пропущено: " + str(lost), 1, (205, 255, 255)
    )
    text_points = font1.render(
    "Счет: " + str(points), 1, (205, 255, 255)
    )

    window.blit(back, (0, 0))
    window.blit(text_lose, (10,10))
    window.blit(text_points, (10,50))
    window.blit(text_reload, (sherene/2-60,dlene-100))


    rocket.reset()
    for x in bullets:
        x.reset()
    for x in enemies:
        x.reset()
    display.update()   
    rocket.update()
    for x in bullets:
        x.update()
    for x in enemies:
        x.update()

    for x in enemies:
        if not x.ast:
            for y in bullets:
                if sprite.collide_rect(x, y):
                    print(1)
                    x.rect.y = 0
                    x.rect.x = randint(0, sherene)
                    bullets.remove(y)
                    points += 1
        if sprite.collide_rect(x, rocket):
            lost = 3


    if points >= 15:
        text_points = font2.render(
        "YOU WIN", 1, (0, 255, 0)
        )
        window.blit(text_points, (250,350))
        run = False
        display.update() 
        tm.sleep(2)
    clock.tick(60)


    if lost >= 3:
        text_points = font2.render(
        "YOU LOSE ", 1, (255, 0, 0)
        )
        window.blit(text_points, (250,350))
        run = False
        display.update() 
        tm.sleep(2)
    clock.tick(60)

# while True:
#     for e in event.get():
#         if e.type == QUIT:
#             run = False
#     display.update()   