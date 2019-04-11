# Danmaku Python Shooter game is developed by Christopher G. Rodriguez
# Created March 1, 2019 (Completed on April 9, 2019)
#
# 5th Period Programming
# See READ_ME file for instructions and credits!


# pylint: disable=import-error
import pygame, random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
TITLE = "Danmaku Python Shooter v1.02b"
#screen = pygame.display.set_mode(SIZE)
''' uncomment below to enable fullscreen mode and comment the above screen variable '''
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (0, 255, 255)
BLUE = (0, 64, 255)
PURPLE = (128, 0, 255)
GREEN = (64, 255, 0)
ORANGE = (255, 128, 0)
GRAY = (91, 91, 91)
BABY_BLUE = (185, 209, 247)


# Fonts
FONT_SM = pygame.font.Font("assets/fonts/whiterabbit.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/whiterabbit.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/whiterabbit.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/Kamikaze.ttf", 76)


# Images
splash_img = pygame.image.load('assets/images/Splash/splash_screen.png').convert()
splash_img_resample = pygame.transform.scale(splash_img, (1280, 720))
background_img = pygame.image.load('assets/images/Background/windows_doom.png').convert()
background_img_resample = pygame.transform.scale(background_img, (1280, 720))

ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()

virus_img = pygame.image.load('assets/images/virus.png').convert_alpha()
virus2_img = pygame.image.load('assets/images/virus2.png').convert_alpha()

virus_img2 = pygame.image.load('assets/images/virus_lv2.png').convert_alpha()
virus2_img2 = pygame.image.load('assets/images/virus2_lv2.png').convert_alpha()

virus_img3 = pygame.image.load('assets/images/virus_lv3.png').convert_alpha()
virus2_img3 = pygame.image.load('assets/images/virus2_lv3.png').convert_alpha()

final_boss_img = pygame.image.load('assets/images/boss.png').convert_alpha()
final_boss_img_scaled = pygame.transform.scale(final_boss_img, (448, 384))

bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/health_powerup.png').convert_alpha()
laser_speed_powerup_img = pygame.image.load('assets/images/laser_speed_powerup.png').convert_alpha()
speed_powerup_img = pygame.image.load('assets/images/speed_powerup.png').convert_alpha()


# Sounds
BOMB_SFX = pygame.mixer.Sound('assets/sounds/bomb.ogg')
END_SFX = pygame.mixer.Sound('assets/sounds/end.ogg')
EXPLOSION_SFX = pygame.mixer.Sound('assets/sounds/explosion.ogg')
LASER_SFX = pygame.mixer.Sound('assets/sounds/laser.ogg')
WIN_SFX = pygame.mixer.Sound('assets/sounds/win.ogg')
ERROR_SFX = pygame.mixer.Sound('assets/sounds/Windows XP Critical Stop.ogg')
POWERUP_SFX = pygame.mixer.Sound('assets/sounds/powerup.ogg')

EXPLOSION_SFX.set_volume(0.1)


# Music
FINAL_BOSS = pygame.mixer.music.load('assets/music/Eye of the Storm_Hybrid Orchestral.ogg')
pygame.mixer.music.set_volume(0.25)


# Stages
START = 0
PLAYING = 1
END = 2
INTERMISSION = 3
BOSS = 4
PAUSE = 5
WIN = 6


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 5

        self.timer = 0
        self.laser_speed = 20  # Original is 20
        
        self.max_health = 50

    def set_normal_mode(self):
        self.health = 50
    
    def set_hard_mode(self):
        self.health = 25

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        pygame.mixer.Channel(0).play(LASER_SFX)
        if self.timer <= 0:
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)

            self.timer = self.laser_speed

        self.timer -= 1

    def update(self):
        global stage, mob_collide

        mob_collide = False
        
        hit_list = pygame.sprite.spritecollide(self, mobs, True)
        hit_list2 = pygame.sprite.spritecollide(self, powerups, True)
        hit_list3 = pygame.sprite.spritecollide(self, bombs, True)
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        ''' Check powerups '''
        for hit in hit_list2:
            hit.apply(self)
            pygame.mixer.Channel(4).play(POWERUP_SFX)

        ''' if player is hit by mob, or health runs out, dies '''

        for h in hit_list3:
            self.health -= 1
            player.score -= 100
            pygame.mixer.Channel(5).play(ERROR_SFX)

        if self.health <= 0:
            stage = END
            self.kill()
            pygame.mixer.Channel(2).play(END_SFX)
        elif len(hit_list) > 0:
            mob_collide = True
            stage = END
            self.kill()
            pygame.mixer.Channel(2).play(END_SFX)


class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 10


    def update(self):
        hit_list = pygame.sprite.spritecollide(self, mobs, True)
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
        elif len(hit_list) > 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        global boss_maxHP, boss_HP
        boss_maxHP = 200
        boss_HP = 200

        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_normal_mode(self):
        if level == 1:
            self.health = 1
        elif level == 2:
            self.health = 2
        elif level == 3:
            self.health = 3
        elif level == 4:
            self.max_health = 200
            self.health = 200
    
    def set_hard_mode(self):
        if level == 1:
            self.health = 2
        elif level == 2:
            self.health = 3
        elif level == 3:
            self.health = 4
        elif level == 4:
            self.max_health = 400
            self.health = 400


    def drop_bomb(self):
        pygame.mixer.Channel(1).play(BOMB_SFX)

        ''' Defines all bombs for final boss '''
        if level != 4:
            bomb = Bomb(bomb_img)
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.centery = self.rect.bottom
            bombs.add(bomb)
        else:
            bomb1 = Bomb(bomb_img)
            bomb1.rect.centerx = self.rect.x + 28
            bomb1.rect.centery = self.rect.bottom

            bomb2 = Bomb(bomb_img)
            bomb2.rect.centerx = self.rect.x + 56
            bomb2.rect.centery = self.rect.bottom

            bomb3 = Bomb(bomb_img)
            bomb3.rect.centerx = self.rect.x + 84
            bomb3.rect.centery = self.rect.bottom

            bomb4 = Bomb(bomb_img)
            bomb4.rect.centerx = self.rect.x + 112
            bomb4.rect.centery = self.rect.bottom
            
            bomb5 = Bomb(bomb_img)
            bomb5.rect.centerx = self.rect.x + 70
            bomb5.rect.centery = self.rect.bottom

            bomb6 = Bomb(bomb_img)
            bomb6.rect.centerx = self.rect.x + 140
            bomb6.rect.centery = self.rect.bottom

            bomb7 = Bomb(bomb_img)
            bomb7.rect.centerx = self.rect.x + 168
            bomb7.rect.centery = self.rect.bottom

            bomb8 = Bomb(bomb_img)
            bomb8.rect.centerx = self.rect.x + 196
            bomb8.rect.centery = self.rect.bottom

            bomb9 = Bomb(bomb_img)
            bomb9.rect.centerx = self.rect.x + 224
            bomb9.rect.centery = self.rect.bottom

            bomb10 = Bomb(bomb_img)
            bomb10.rect.centerx = self.rect.x + 252
            bomb10.rect.centery = self.rect.bottom

            bomb11 = Bomb(bomb_img)
            bomb11.rect.centerx = self.rect.x + 280
            bomb11.rect.centery = self.rect.bottom

            bomb12 = Bomb(bomb_img)
            bomb12.rect.centerx = self.rect.x + 308
            bomb12.rect.centery = self.rect.bottom

            bomb13 = Bomb(bomb_img)
            bomb13.rect.centerx = self.rect.x + 336
            bomb13.rect.centery = self.rect.bottom

            bomb14 = Bomb(bomb_img)
            bomb14.rect.centerx = self.rect.x + 364
            bomb14.rect.centery = self.rect.bottom

            bomb15 = Bomb(bomb_img)
            bomb15.rect.centerx = self.rect.x + 392
            bomb15.rect.centery = self.rect.bottom

            bomb16 = Bomb(bomb_img)
            bomb16.rect.centerx = self.rect.x + 420
            bomb16.rect.centery = self.rect.bottom

            ''' Chooses which of the 16 bombs will appear at random '''
            bomb_spot = random.randrange(1, 16)
            for b in str(bomb_spot):
                if bomb_spot == 1:
                    bombs.add(bomb1)
                elif bomb_spot == 2:
                    bombs.add(bomb2)
                elif bomb_spot == 3:
                    bombs.add(bomb3)
                elif bomb_spot == 4:
                    bombs.add(bomb4)
                elif bomb_spot == 5:
                    bombs.add(bomb5)
                elif bomb_spot == 6:
                    bombs.add(bomb6)
                elif bomb_spot == 7:
                    bombs.add(bomb7)
                elif bomb_spot == 8:
                    bombs.add(bomb8)
                elif bomb_spot == 9:
                    bombs.add(bomb9)
                elif bomb_spot == 10:
                    bombs.add(bomb10)
                elif bomb_spot == 11:
                    bombs.add(bomb11)
                elif bomb_spot == 12:
                    bombs.add(bomb12)
                elif bomb_spot == 13:
                    bombs.add(bomb13)
                elif bomb_spot == 14:
                    bombs.add(bomb14)
                elif bomb_spot == 15:
                    bombs.add(bomb15)
                elif bomb_spot == 16:
                    bombs.add(bomb16)


    def update(self):
        global boss_HP

        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        for h in hit_list:
            self.health -= 1
            player.score += 50
            if level == 4:
                boss_HP -= 1

        if len(hit_list) > 0 and self.health <= 0:
            pygame.mixer.Channel(3).play(EXPLOSION_SFX)
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        
        if hard_mode == False:
            if level == 1:
                self.speed = 10
            elif level == 2:
                self.speed = 8
            elif level == 3:
                self.speed = 5
            elif level == 4:
                self.speed = 3
        else:
            if level == 1:
                self.speed = 8
            elif level == 2:
                self.speed = 8
            elif level == 3:
                self.speed = 4
            elif level == 4:
                self.speed = 2


    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Fleet():
    def __init__(self, mobs):
                
        self.mobs = mobs
        
    def set_normal_mode(self):
        if level == 1:
            self.moving_right = True
            self.speed = 1
            self.drop = 20
            self.bomb_rate = 15 # lower is faster, initial is 15
        elif level == 2:
            self.moving_right = True
            self.speed = 2
            self.drop = 20
            self.bomb_rate = 10
        elif level == 3:
            self.moving_right = True
            self.speed = 3
            self.drop = 20
            self.bomb_rate = 5
        elif level == 4:
            self.speed = 10
            self.moving_right = True
            self.drop = 10
            self.bomb_rate = 1
    
    def set_hard_mode(self):
        if level == 1:
            self.moving_right = True
            self.speed = 3
            self.drop = 20
            self.bomb_rate = 10
        elif level == 2:
            self.moving_right = True
            self.speed = 3
            self.drop = 20
            self.bomb_rate = 7
        elif level == 3:
            self.moving_right = True
            self.speed = 4
            self.drop = 20
            self.bomb_rate = 4
        elif level == 4:
            self.speed = 20
            self.moving_right = True
            self.drop = 10
            self.bomb_rate = 1

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        global stage
        
        for m in mobs:
            m.rect.y += self.drop

    def check_bottom(self):
        global stage
        ''' If an ememy reaches the bottom, trigger game over '''
        for m in mobs:
            if m.rect.bottom > HEIGHT:
                stage = END
                pygame.mixer.Channel(2).play(END_SFX)

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def is_cleared(self):
        ''' Lets rest of game know when the fleet is cleared '''
        return len(self.mobs) == 0
    
    def update(self):
        self.move()
        self.choose_bomber()
        self.check_bottom()


class HealthPowerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = powerup_x
        self.rect.y = powerup_y
        self.speed = 5
        

    def apply(self, ship):
        if hard_mode == True:
            ship.health = 25
        else:
            ship.health = 50

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, player, True)

        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            get_powerup_location()
            self.rect.x = powerup_x
            self.rect.y = powerup_y
        elif len(hit_list) > 0:
            self.kill()


class SpeedPowerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = powerup_x
        self.rect.y = powerup_y
        self.speed = 5


    def apply(self, ship):
        ship.speed += 2

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, player, True)

        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            get_powerup_location()
            self.rect.x = powerup_x
            self.rect.y = powerup_y
        elif len(hit_list) > 0:
            self.kill()


class ShootingSpeedPowerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = powerup_x
        self.rect.y = powerup_y
        self.speed = 5


    def apply(self, ship):
        ship.laser_speed -= 10

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, player, True)

        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            get_powerup_location()
            self.rect.x = powerup_x
            self.rect.y = powerup_y
        elif len(hit_list) > 0:
            self.kill()


# Drawing Functions
def show_title_screen():
    difficulty = "NORMAL"
    if hard_mode == True:
        difficulty = "HARD"
    elif hard_mode == False:
        difficulty = "NORMAL"

    screen.blit(splash_img_resample, [0, 0])
    title_text = FONT_XL.render("Danmaku Python Shooter", 1, WHITE)
    sub_text = FONT_LG.render("Press SPACE to start!", 1, WHITE)
    difficulty_txt = FONT_SM.render("Difficulty: " + str(difficulty) + " (Press ENTER key to change)", 1, YELLOW)
    t1 = title_text.get_width()
    t2 = sub_text.get_width()
    difficulty_rect = difficulty_txt.get_rect()
    difficulty_rect.right = WIDTH - 20
    difficulty_rect.top =  20
    screen.blit(title_text, [WIDTH/2 - t1/2, 256])
    screen.blit(sub_text, [WIDTH/2 - t2/2, 356])
    screen.blit(difficulty_txt, difficulty_rect)

def show_main_background():
    screen.blit(background_img_resample, [0, 0])

    HP_text = FONT_SM.render("Health: ", 1, YELLOW)
    screen.blit(HP_text, [750, 690])

    if level == 4:
        boss_text = FONT_SM.render("Boss HP: ", 1, YELLOW)
        screen.blit(boss_text, [100, 690])

def show_pause():
    t1 = FONT_LG.render("PAUSED", True, WHITE)
    t2 = FONT_MD.render("(Press SPACE to resume.)", True, TURQUOISE)
    w1 = t1.get_width()
    w2 = t2.get_width()
    screen.blit(t1, [WIDTH/2 - w1/2, 350])
    screen.blit(t2, [WIDTH/2 - w2/2, 405])

def show_intermission():
    t1 = FONT_LG.render("STAGE CLEARED!", True, WHITE)
    t2 = FONT_MD.render("(Press SPACE to continue.)", True, TURQUOISE)
    w1 = t1.get_width()
    w2 = t2.get_width()
    screen.blit(t1, [WIDTH/2 - w1/2, 350])
    screen.blit(t2, [WIDTH/2 - w2/2, 405])

def show_boss_text():
    t1 = FONT_LG.render("STAGE CLEARED!", True, WHITE)
    t2 = FONT_MD.render("(Press SPACE to fight the final boss!)", True, TURQUOISE)
    w1 = t1.get_width()
    w2 = t2.get_width()
    screen.blit(t1, [WIDTH/2 - w1/2, 350])
    screen.blit(t2, [WIDTH/2 - w2/2, 405])

def show_end():
    end_txt = FONT_LG.render("GAME OVER", 1, RED)
    end_txt2 = FONT_MD.render("Press SPACE to play again or ESC to exit.", 1, WHITE)
    txt1 = end_txt.get_width()
    txt2 = end_txt2.get_width()
    screen.blit(end_txt, [WIDTH/2 - txt1/2, 350])
    screen.blit(end_txt2, [WIDTH/2 - txt2/2, 405])

def show_win():
    win_txt = FONT_LG.render("YOU DEFEATED THE COMPUTER VIRUSES!", 1, WHITE)
    win_txt2 = FONT_MD.render("Press SPACE to play again & ESC to exit!", 1, TURQUOISE)
    txt3 = win_txt.get_width()
    txt4 = win_txt2.get_width()
    screen.blit(win_txt, [WIDTH/2 - txt3/2, 350])
    screen.blit(win_txt2, [WIDTH/2 - txt4/2, 405])

def music():
    if stage == PLAYING:
        pygame.mixer.music.play(-1)
    elif stage == START or stage == END or stage == WIN:
        pygame.mixer.music.stop()
    elif stage == PAUSE:
        pygame.mixer.music.pause()

# Helper Functions
def update_mode():
    if hard_mode == True:
        ship.set_hard_mode()
        for m in mobs:
            m.set_hard_mode()
        fleet.set_hard_mode()
    elif hard_mode == False:
        ship.set_normal_mode()
        for mo in mobs:
            mo.set_normal_mode()
        fleet.set_normal_mode()

def draw_health(player):
    ratio = ship.health / ship.max_health
    color = GREEN
    
    if ratio < .26:
        color = RED
    elif ratio < .51:
        color = YELLOW
    else:
        color = GREEN

    bar_length = ratio * 249
    
    pygame.draw.rect(screen, WHITE, [850, 682, 249, 28])
    pygame.draw.rect(screen, color, [850, 682, bar_length, 28])

def draw_boss_health():
    ratio = boss_HP / boss_maxHP
    color = GREEN
    
    if ratio < .26:
        color = RED
    elif ratio < .51:
        color = YELLOW
    else:
        color = GREEN

    bar_length = ratio * 400
    
    pygame.draw.rect(screen, WHITE, [215, 682, 400, 28])
    pygame.draw.rect(screen, color, [215, 682, bar_length, 28])

def draw_current_level(level):
    if hard_mode == True:
        difficulty_txt = FONT_SM.render("(Hard Mode)", 1, YELLOW)
        difficulty_rect = difficulty_txt.get_rect()
        difficulty_rect.left = 20
        difficulty_rect.top =  60
        screen.blit(difficulty_txt, difficulty_rect)
    
    if level < 4:
        h1 = FONT_MD.render("Level: " + str(level), True, YELLOW)
        screen.blit(h1, [20, 20])

def show_stats():
    if player.score >= player.high_score:
        player.high_score = player.score
    
    score_txt = FONT_MD.render("Score: " + str(player.score), 1, YELLOW)
    score_rect = score_txt.get_rect()
    score_rect.right = WIDTH - 20
    score_rect.top = 20
    screen.blit(score_txt, score_rect)

    high_score_txt = FONT_MD.render("High Score: " + str(player.high_score), 1, YELLOW)
    high_score_rect = high_score_txt.get_rect()
    high_score_rect.right = WIDTH - 20
    high_score_rect.top = 60
    screen.blit(high_score_txt, high_score_rect)

def update_highscore():
    if player.score >= player.high_score:
        player.high_score = player.score

    with open('high_score.txt', 'w') as f:
        f.write(str(player.high_score))

def get_powerup_location():
    global powerup_x, powerup_y
    
    powerup_x = random.randrange(0, WIDTH)
    powerup_y = random.randrange(-30000, -1000)

def start_level(level):
    global mobs, mob_list, ship, fleet

    ''' initialize player position '''
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    v_img = virus_img
    v_img2 = virus2_img

    if level == 1:
        v_img = virus_img
        v_img2 = virus2_img
    elif level == 2:
        v_img = virus_img2
        v_img2 = virus2_img2
    elif level == 3:
        v_img = virus_img3
        v_img2 = virus2_img3

    ''' Initializes mob positions '''
    # Place the following in a text file
    mob1 = Mob(76, 100, v_img)
    mob2 = Mob(288, 100, v_img2)
    mob3 = Mob(500, 100, v_img)
    mob4 = Mob(712, 100, v_img2)
    mob5 = Mob(924, 100, v_img)
    mob6 = Mob(1136, 100, v_img2)
    
    mob7 = Mob(76, 0, v_img2)
    mob8 = Mob(288, 0, v_img)
    mob9 = Mob(500, 0, v_img2)
    mob10 = Mob(712, 0, v_img)
    mob11 = Mob(924, 0, v_img2)
    mob12 = Mob(1136, 0, v_img)

    mob13 = Mob(76, -100, v_img)
    mob14 = Mob(288, -100, v_img2)
    mob15 = Mob(500, -100, v_img)
    mob16 = Mob(712, -100, v_img2)
    mob17 = Mob(924, -100, v_img)
    mob18 = Mob(1136, -100, v_img2)

    mob19 = Mob(76, -200, v_img2)
    mob20 = Mob(288, -200, v_img)
    mob21 = Mob(500, -200, v_img2)
    mob22 = Mob(712, -200, v_img)
    mob23 = Mob(924, -200, v_img2)
    mob24 = Mob(1136, -200, v_img)

    mob25 = Mob(76, -300, v_img)
    mob26 = Mob(288, -300, v_img2)
    mob27 = Mob(500, -300, v_img)
    mob28 = Mob(712, -300, v_img2)
    mob29 = Mob(924, -300, v_img)
    mob30 = Mob(1136, -300, v_img2)

    mob_list = [mob1, mob2, mob3, mob4, mob5, mob6,
             mob7, mob8, mob9, mob10, mob11, mob12,
             mob13, mob14, mob15, mob16, mob17, mob18,
             mob19, mob20, mob21, mob22, mob23, mob24,
             mob25, mob26, mob27, mob28, mob29, mob30]

    mobs.add(mob_list)
    fleet = Fleet(mobs)

def begin_fight():
    global mobs, mob_list

    ''' Make boss the only mob enemy and add it to the list '''
    boss_img = final_boss_img_scaled
    mob = Mob(10, -300, boss_img)

    mob_list = [mob]

    mobs.add(mob_list)


def setup():
    global stage, hard_mode, level, powerup_x, powerup_y, done
    global player, ship, lasers, mobs, bombs, powerups, fleet

    ''' Initial Game Level '''
    level = 1

    ''' Initial Difficulty Set to Normal '''
    hard_mode = False
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    ''' Set scores '''
    player.score = 5000
    player.high_score = 5000
    
    ''' Retrieve High Score if it exists '''
    file_high_score = open('high_score.txt', 'r')
    player.high_score = int(file_high_score.readline())
    file_high_score.close()
    
    ''' Make remaining sprite groups '''
    mobs = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    ''' Add powerups '''
    get_powerup_location()
    powerup1 = HealthPowerup(powerup_x, powerup_y, powerup_img)

    get_powerup_location()
    powerup2 = SpeedPowerup(powerup_x, powerup_y, speed_powerup_img)

    get_powerup_location()
    powerup3 = ShootingSpeedPowerup(powerup_x, powerup_y, laser_speed_powerup_img)

    powerups.add(powerup1, powerup2, powerup3)

    ''' Begin first level '''
    start_level(level)
    
    ''' set stage '''
    stage = START
    done = False

    
# Game loop
setup()
music()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    music()
                elif event.key == pygame.K_RETURN:
                    hard_mode = not hard_mode
                    update_mode()
            elif stage == PLAYING:
                if event.key == pygame.K_r:
                    setup()
                    music()
                elif event.key == pygame.K_p:
                    stage = PAUSE
                    music()
            elif stage == PAUSE:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    pygame.mixer.music.unpause()
            elif stage == INTERMISSION:
                if event.key == pygame.K_SPACE:
                    ''' Begins the next stage and resumes play '''
                    start_level(level)
                    stage = PLAYING
            elif stage == BOSS:
                if event.key == pygame.K_SPACE:
                    ''' Begins the final stage and resumes play '''
                    begin_fight()
                    stage = PLAYING
            elif stage == END:
                music()
                if event.key == pygame.K_SPACE:
                    setup()
            elif stage == WIN:
                music()
                if event.key == pygame.K_SPACE:
                    setup()
        
    pressed = pygame.key.get_pressed()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage != START and stage != PAUSE:
        lasers.update()
        bombs.update()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

        if pressed[pygame.K_SPACE]:
            ship.shoot()

        player.update()
        
        powerups.update()
        
        fleet.update()
        mobs.update()


        ''' For every fleet cleared, calls an intermission until end level '''
        if fleet.is_cleared():
            level += 1
            if level < 4:
                stage = INTERMISSION
            elif level == 4:
                stage = BOSS
            elif level > 4 and mob_collide == False:
                stage = WIN
                pygame.mixer.Channel(4).play(WIN_SFX)
            else:
                stage = END
                pygame.mixer.Channel(2).play(END_SFX)
                

    if stage == END or stage == WIN:
        update_highscore()

        
    # Drawing code functions
    screen.fill(BLACK)

    if stage == START:
        show_title_screen()
    elif stage != START:
        show_main_background()
        draw_health(player)
        if level == 4:
            draw_boss_health()
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        powerups.draw(screen)
        draw_current_level(level)
        show_stats()

    if stage == PAUSE:
        show_pause()
    elif stage == INTERMISSION:
        show_intermission()
    elif stage == BOSS:
        show_boss_text()
    elif stage == END:
        music()
        show_end()
    elif stage == WIN:
        music()
        show_win()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
