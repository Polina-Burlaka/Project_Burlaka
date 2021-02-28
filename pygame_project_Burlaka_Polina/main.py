# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
import pyganim
import os
import sys

# Объявляем переменные
MAIN_WIDTH = 800  # Ширина создаваемого окна
MAIN_HEIGHT = 640  # Высота
DISPLAY = (MAIN_WIDTH, MAIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BG_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)

# для монстров

MOB_WIDTH = 32
MOB_HEIGHT = 32
MOB_COLOR = "#2110FF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_FOR_MOB = [('%s/monsters/fire1.png' % ICON_DIR),
                     ('%s/monsters/fire2.png' % ICON_DIR)]

# для блоков

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32
BLOCK_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_TELEPORT = [
    ('%s/blocks/portal2.png' % ICON_DIR),
    ('%s/blocks/portal1.png' % ICON_DIR)]

ANIMATION_GAME_END = [
    ('%s/blocks/end_game.png' % ICON_DIR),
    ('%s/blocks/end_game2.png' % ICON_DIR)]

# для игрока

MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 2.5  # ускорение
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
ANIMATION_UPDATE = 0.1  # скорость смены кадров
ANIM_SUPER_SPEED_UPDATE = 0.05  # скорость смены кадров при ускорении
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
                   ('%s/mario/r2.png' % ICON_DIR),
                   ('%s/mario/r3.png' % ICON_DIR),
                   ('%s/mario/r4.png' % ICON_DIR),
                   ('%s/mario/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
                  ('%s/mario/l2.png' % ICON_DIR),
                  ('%s/mario/l3.png' % ICON_DIR),
                  ('%s/mario/l4.png' % ICON_DIR),
                  ('%s/mario/l5.png' % ICON_DIR)]

ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY_RIGHT = [('%s/mario/r1.png' % ICON_DIR, 0.1)]
ANIMATION_STAY_LEFT = [('%s/mario/l1.png' % ICON_DIR, 0.1)]


# окна меню
def start_screen(score=0):
    global is_game_start
    intro_text = ["ПРОЙТИ ВСЕ ПРЕПЯТСТВИЯ И УСПЕТЬ К ДЕДЛАЙНУ ", " ",
                  "Управление с помощью стрелок",
                  "для стрельбы нажмите пробел",
                  'Чтобы начать нажмите на экран!'
                  ]
    intro_text2 = ["                ВЫ ПОБЕДИЛИ ", "  ",
                   "                       УРА!!!", " ",
                   ]
    fon = pygame.transform.scale(image.load('images/menu_rules.jpg'), (DISPLAY))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 80
    if is_game_start == 0:
        for line in intro_text:
            string_rendered = font.render(line, 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 30
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                is_game_start = 1

        pygame.display.flip()

    elif is_game_start == 2:
        restart_img = pygame.image.load('images/restart_button.png')
        restart_button = Button(MAIN_WIDTH // 2 - 80, MAIN_HEIGHT - 120, restart_img)
        intro_text2.append('                   Ваш счёт: ' + str(score))
        for line in intro_text2:
            string_rendered = font.render(line, 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 160
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if restart_button.draw():
                is_game_start = 0
            pygame.display.flip()


# отрисовка фона
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# кнопочки меню
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # получаем позицию мыши
        pos = pygame.mouse.get_pos()
        # проверяем условия клика
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


# персонаж и его взаимодействия
class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.jj = 0
        # self.can_doublejump = True
        self.can_jump = True
        self.y = 0
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        self.napravlenie = 'right'
        #        Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_UPDATE))
            boltAnimSuperSpeed.append((anim, ANIM_SUPER_SPEED_UPDATE))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        #        Анимация движения влево
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_UPDATE))
            boltAnimSuperSpeed.append((anim, ANIM_SUPER_SPEED_UPDATE))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        self.boltAnimStay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.boltAnimStay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStay_right.play()
        self.boltAnimStay_right.blit(self.image, (0, 0))  # По-умолчанию, стоим
        self.boltAnimStay_left.play()
        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.napravlenie)
        all_objects.add(bullet)
        bullets.add(bullet)

    def update(self, left, right, up, running, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if running and (left or right):  # если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER  # то прыгаем выше
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        elif up and self.jj == 1 and self.onGround:
            self.yvel += self.y

            if running and (left or right):  # если есть ускорение и мы движемся
                self.yvel -= JUMP_EXTRA_POWER  # то прыгаем выше

            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.napravlenie = 'left'
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if running:  # если усkорение
                self.xvel -= MOVE_EXTRA_SPEED  # то передвигаемся быстрее
                if not up:  # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))  # то отображаем быструю анимацию
            else:  # если не бежим
                if not up:  # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0))  # отображаем анимацию движения
            if up:  # если же прыгаем
                self.boltAnimJumpLeft.blit(self.image, (0, 0))  # отображаем анимацию прыжка

        if right:
            self.napravlenie = 'right'
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                if self.napravlenie == 'right':
                    self.boltAnimStay_right.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay_left.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def jump(self):
        # Обработка прыжка
        # Нам нужно проверять здесь, контактируем ли мы с чем-либо
        # или другими словами, не находимся ли мы в полете.
        jump_fx = pygame.mixer.Sound('sounds/jump.wav')
        jump_fx.set_volume(0.5)
        if self.can_jump and not self.rect.top <= 0:
            self.can_jump = False
            self.y -= JUMP_POWER
            jump_fx.play()

    def collide(self, xvel, yvel, platforms):
        global score
        hits = pygame.sprite.spritecollide(self, golds, True, False)
        if hits:
            global gold_count
            gold_count += 1
            score += 1

        for p in monsters:  # с монстрами пересекаем отдельно
            if sprite.collide_rect(self, p):
                self.die()
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, Death_block) or isinstance(p,
                                                            Monster):  # если пересакаемый блок - blocks.BlockDie или Monster
                    self.die()  # умираем
                elif isinstance(p, Teleportation):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, End_the_game):  # если коснулись принцессы
                    self.winner = True  # победили!!!
                    global is_game_start
                    is_game_start = 2
                else:
                    if xvel > 0:  # если движется вправо
                        self.rect.right = p.rect.left  # то не движется вправо

                    if xvel < 0:  # если движется влево
                        self.rect.left = p.rect.right  # то не движется влево

                    if yvel > 0:  # если падает вниз
                        self.rect.bottom = p.rect.top  # то не падает вниз
                        self.onGround = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                    if yvel < 0:  # если движется вверх
                        self.rect.top = p.rect.bottom  # то не движется вверх
                        self.yvel = 0  # и энергия прыжка пропадает

                    # self.can_doublejump = True
                    self.can_jump = True

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты


# пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, napravlenie):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.napr = napravlenie
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        if self.napr == 'left':
            self.rect.x -= self.speedx
            for p in platforms:
                if sprite.collide_rect(self, p):
                    self.kill()
        else:
            self.rect.x += self.speedx
            for p in platforms:
                if sprite.collide_rect(self, p):
                    self.kill()


# блоки
class Blocks(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(Color(BLOCK_COLOR))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color(BLOCK_COLOR))
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)


class Death_block(Blocks):
    def __init__(self, x, y):
        Blocks.__init__(self, x, y)
        self.image = image.load("%s/blocks/death_block.png" % ICON_DIR)


class Teleportation(Blocks):
    def __init__(self, x, y, goX, goY):
        Blocks.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_TELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BLOCK_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


# конец игры
class End_the_game(Blocks):
    def __init__(self, x, y):
        Blocks.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_GAME_END:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BLOCK_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


# монетки
class Gold(Blocks):
    def __init__(self, x, y):
        Blocks.__init__(self, x, y)
        self.image = image.load("%s/blocks/coin.png" % ICON_DIR)


# противники
class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, motion_left, motion_up):
        sprite.Sprite.__init__(self)
        self.image = Surface((MOB_WIDTH, MOB_HEIGHT))
        self.image.fill(Color(MOB_COLOR))
        self.rect = Rect(x, y, MOB_WIDTH, MOB_HEIGHT)
        self.image.set_colorkey(Color(MOB_COLOR))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = motion_left  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = motion_up  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается

        boltAnim = []
        for anim in ANIMATION_FOR_MOB:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms, bullets):  # по принципу героя
        self.image.fill(Color(MOB_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
        self.collide(platforms, bullets)
        self.rect.y += self.yvel
        self.rect.x += self.xvel

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идем в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идем в обратную сторону, вертикаль

    def collide(self, platforms, bullets):
        for object in platforms:
            if sprite.collide_rect(self, object) and self != object:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel

        for object in monsters:
            if sprite.collide_rect(self, object) and self != object:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel


# обновление окна в соответствии с положением персонажа
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + MAIN_WIDTH / 2, -t + MAIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - MAIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - MAIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


# загрузка уровня из текстового файла
def World_creation():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя
    levelFile = open('%s/levels/world_level.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                if commands[0] == "portal":  # если первая команда portal, то создаем портал
                    tp = Teleportation(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    all_objects.add(tp)
                    platforms.append(tp)
                    animated_objects.add(tp)
                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    all_objects.add(mn)
                    # platforms.append(mn)
                    monsters.add(mn)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


screen_width = 640
screen_height = 360

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Super Mario VS Deadline')

bg_img = pygame.image.load('images/menu_image.png')
start_img = pygame.image.load('images/button_start.png')

exit_img = pygame.image.load('images/button_exit.png')
start_button = Button(screen_width // 2 - 200, screen_height // 2 - 50, start_img)
exit_button = Button(screen_width // 2 + 90, screen_height // 2 - 50, exit_img)

white = (255, 255, 255)
run = True
main_menu = True
is_game_start = 0
gold_count = 0
score = 0

while run:
    BackGround = Background('%s/images/menu_image.png' % ICON_DIR, [0, 0])
    screen.blit(BackGround.image, BackGround.rect)
    for e in pygame.event.get():  # Обрабатываем события
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        pygame.init()
        pygame.mixer.music.load('sounds/melody.wav')
        pygame.mixer.music.play(-1, 0.0)
        level = []
        all_objects = pygame.sprite.Group()  # Все объекты
        animated_objects = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
        monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
        bullets = pygame.sprite.Group()
        platforms = []  # то, во что мы будем врезаться или опираться
        golds = pygame.sprite.Group()
        font_score = pygame.font.Font(None, 30)

        World_creation()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pygame.init()  # Инициация PyGame, обязательная строчка
        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Super Mario VS Deadline")  # Пишем в шапку
        BackGround = Background('%s/images/game_fon.jpg' % ICON_DIR, [0, 0])

        bg = Surface((MAIN_WIDTH, MAIN_HEIGHT))  # Создание видимой поверхности
        # будем использовать как фон
        bg.blit(BackGround.image, BackGround.rect)

        left = right = False  # по умолчанию - стоим
        up = False
        running = False

        hero = Player(playerX, playerY)  # создаем героя по (x,y) координатам
        all_objects.add(hero)

        timer = pygame.time.Clock()
        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = Blocks(x, y)
                    all_objects.add(pf)
                    platforms.append(pf)
                if col == "*":
                    bd = Death_block(x, y)
                    all_objects.add(bd)
                    platforms.append(bd)
                if col == "P":
                    pr = End_the_game(x, y)
                    all_objects.add(pr)
                    platforms.append(pr)
                    animated_objects.add(pr)
                if col == "g":
                    gg = Gold(x, y)
                    golds.add(gg)
                    all_objects.add(gg)

                x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
            y += BLOCK_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        total_level_width = len(level[0]) * BLOCK_WIDTH  # Высчитываем фактическую ширину уровня
        total_level_height = len(level) * BLOCK_HEIGHT  # высоту

        camera = Camera(camera_configure, total_level_width, total_level_height)
        run_game = True

        while run_game:  # Основной цикл программы
            timer.tick(60)

            if is_game_start == 0:
                score = 0
                start_screen()
            if is_game_start == 1:
                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == KEYDOWN and e.key == K_UP:
                        up = True
                        hero.jump()
                    if e.type == KEYDOWN and e.key == K_LEFT:
                        left = True
                    if e.type == KEYDOWN and e.key == K_RIGHT:
                        right = True
                    if e.type == KEYDOWN and e.key == K_LSHIFT:
                        running = True
                    if e.type == KEYDOWN and e.key == K_SPACE:
                        hero.shoot()

                    if e.type == pygame.KEYUP:
                        if e.type == KEYUP and e.key == K_UP:
                            up = False

                        if e.type == KEYUP and e.key == K_RIGHT:
                            right = False
                        if e.type == KEYUP and e.key == K_LEFT:
                            left = False
                        if e.type == KEYUP and e.key == K_LSHIFT:
                            running = False

                        if e.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                                hero.jump()

                screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
                score_coin = Gold(50 // 2, 50 // 2)
                golds.add(score_coin)
                draw_text('X ' + str(score), font_score, white, 50 - 10, 10)
                animated_objects.update()  # показываеaм анимацию

                camera.update(hero)  # центризируем камеру относительно персонажа
                hero.update(left, right, up, running, platforms)  # передвижение
                hits = pygame.sprite.groupcollide(monsters, bullets, True, True)
                for e in all_objects:
                    screen.blit(e.image, camera.apply(e))
                pygame.display.update()  # обновление и вывод всех изменений на экран
                bullets.update()
                golds.update()
                monsters.update(platforms, bullets)  # передвигаем всех монстров
                pygame.display.flip()
                if hero.winner:
                    run_game = False
            if is_game_start == 2:
                start_screen(score)
    pygame.display.flip()
