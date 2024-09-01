#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer 


# фонова музка

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

# шрифти 
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 35)
win = font1.render("WIN", 1, (255, 255, 255))
lose = font1.render("LOSE", 1, (255, 0, 0))
speed = font2.render("RUN", 1, (180, 0, 0))


score = 0
lost = 0
max_lost = 10

goal = 15
life = 3


# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed



# картинки
img_back = "image (1).png"
img_hero = "ковбой-removebg-preview.png"
img_enemy = "images-removebg-preview (1).png"

img_bullet = "bullet.png"

# створюємо вікно
win_width = 500
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
backdround = transform.scale(image.load(img_back), (win_width, win_height))

# спрайт ракети
ship = Player(img_hero, 100, 400, 80, 100, 10)


monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()
    
###

run = True

finish = False

rel_time = False

num_fire = 0

while run:
    # подія натискання на кнопку закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire  < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True 






    if not finish:
        window.blit(backdround, (0,0))
    
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait reload...', 1,(150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 
                rel_time = False

        text = font2.render("Рахунок: " + str(score), 1, (200, 250, 250))
        window.blit(text, (5, 5))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (200, 250, 250) )
        window.blit(text_lose, (5, 25))

        ship.update()
        monsters.update()
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        if score == 5:
            ship.speed = 30
            window.blit(lose, (200, 200))




        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        


        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        text_life = font1.render(str(life), 1, (200, 0, 0))
        window.blit(text_life, (450, 10))

        display.update()

    time.delay(50)


