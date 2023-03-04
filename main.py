from pygame import *
from random import randint
from datetime import datetime, timedelta


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
score_text = font.Font(None, 36)
score = 0
lost_text = font.Font(None, 36)
lost = 0


lose_text = font.Font(None, 36)
win_text = font.Font(None, 36)


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))


background = transform.scale(
    image.load("jpg.jpg"),
    (win_width, win_height)
)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
       
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):


    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)


        self.num_bullets = 10
        self.next_time_for_shot = datetime.now()


    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    def fire(self):
        if self.num_bullets <= 0 and self.next_reload >= datetime.now:
            self.num_bullets = 10

        if self.num_bullets > 0 and self.next_time_for_shot <= datetime.now():
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            fire_sound.play()
            self.num_bullets -= 1
            self.next_time_for_shot = datetime.now() + timedelta(seconds=2)

            if self.num_bullets <= 0:
                self.next_reload = datetime.now() + timedelta(seconds=5)


class Enemy(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y < 0:
            self.kill()


ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)


bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


run = True
game_over = False
is_win = False


while run:

    window.blit(background, (0, 0))
   
    text1 = score_text.render("Рахунок: " + str(score), 1, (255, 255, 255))
    window.blit(text1, (10, 20))
    text2 = lost_text.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text2, (10, 50))

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if game_over == False:
                if e.key == K_SPACE:
                   
                    ship.fire()


    if game_over == False:


        collides = sprite.groupcollide(monsters, bullets, True, False)
        for c in collides:
            
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, True) or lost >= 10:
            lost += 2
            game_over = True 

        if score >= 8:
            game_over = True
            is_win = True


        ship.update()
        monsters.update()
        bullets.update()
       
    else:
        if is_win == True:
            text4 = win_text.render("Ви перемогли", 1, (255, 255, 255))
            window.blit(text4, (200, 200))
        else:
            text3 = lose_text.render("Ви програли", 1, (255, 255, 255))
            window.blit(text3, (200, 200))


    ship.reset()
    monsters.draw(window)
    bullets.draw(window)


    display.update()
    time.delay(60)



