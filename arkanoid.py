import os
import random
import sys
from pprint import pprint

import pygame

WINDOW_SIZE = W, H = 1024, 727
FPS = 60

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Арканоид')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    def __init__(self, group, file_image, x, y):
        super().__init__()
        group.add(self)
        self.file_image = file_image
        self.image = load_image(file_image)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x // 2 - self.rect[2] // 2
        self.rect.y = y

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        # mouse_clicked = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(*mouse_pos):
            self.image = pygame.transform.scale_by(load_image(self.file_image), 1.1)
            self.rect = self.image.get_rect()
            self.rect.x = self.x // 2 - self.rect[2] // 2
            self.rect.y = self.y
        else:
            self.image = load_image(self.file_image)
            self.rect = self.image.get_rect()
            self.rect.x = self.x // 2 - self.rect[2] // 2
            self.rect.y = self.y


def cursor_replacement():
    mouse_cursor = load_image("arrow.png")
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        x, y = pygame.mouse.get_pos()
        screen.blit(mouse_cursor, (x, y))


# Стартовый экран с правилами и клавишами управления
def start_screen():
    fon = pygame.transform.scale(load_image('starting_background.png'), (W, H))
    button_group = pygame.sprite.Group()
    start_button = Button(button_group, 'button_start.png', W, 484)
    rules_button = Button(button_group, 'rules_button.png', W, 320)
    back_button = Button(button_group, 'back_button.png', 1880, 514)

    rules_screen = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    return  # начинаем игру
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if rules_button.rect.collidepoint(event.pos):
                    rules_screen = True  # открываем правила
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if back_button.rect.collidepoint(event.pos):
                    rules_screen = False  # закрываем правила
        if rules_screen:
            start_button.remove(button_group)
            rules_button.remove(button_group)
            back_button.add(button_group)
        else:
            start_button.add(button_group)
            rules_button.add(button_group)
            back_button.remove(button_group)

        pygame.display.flip()
        screen.blit(fon, (0, 0))
        button_group.update(event)
        button_group.draw(screen)
        cursor_replacement()
        clock.tick(FPS)


def load_level(filename):
    filename = "level/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map

def generate_level(level):
    i, j = None, None
    # Создаем кирпичи с разной прочностью
    for j in range(5):
        for i in range(9):
            health = int(level[j][i])
            print(i, j, health)
            brick = Brick(i * (brick_width + 0) + 80, j * (brick_height + 0) + 50, health)
    return i, j


class Border(pygame.sprite.Sprite):
    def __init__(self, border_image, x, y):
        super().__init__(borders, all_sprites)
        self.image = load_image(border_image)
        if border_image == 'lower_border.png':
            self.danger = 1
        else:
            self.danger = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(players, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = 668 - self.rect[3] // 2
        self.pos = (self.rect.x, self.rect.y)
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.speed = 8

    def update(self, mouse_x):
        # Платформа следует за курсором мыши по горизонтали
        self.rect.x = mouse_x - self.width // 2
        # Ограничение, чтобы платформа не выходила за границы экрана
        if self.rect.x < -20:
            self.rect.x = -20
        if self.rect.x > W - self.width + 20:
            self.rect.x = W - self.width + 20

# класс Мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(balls, all_sprites)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = player.pos[1] - 10
        self.pos = (self.rect.x, self.rect.y)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = -5
        self.is_moving = False  # Мяч не двигается, пока не нажата кнопка мыши

    def move(self):
        if self.is_moving:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            # Отскок от стен и плтаформы
            if pygame.sprite.collide_mask(self, upper_border):
                self.speed_y = -self.speed_y
            if pygame.sprite.collide_mask(self, left_border) or pygame.sprite.collide_mask(self, right_border):
                self.speed_x = -self.speed_x
        else:
            # Мяч следует за платформой
            self.rect.x = player.rect.x + player.width // 2

    def collide_with_brick(self, brick):
        if self.rect.colliderect(brick.rect):
            # Определяем, с какой стороны произошло столкновение
            if abs(self.rect.bottom - brick.rect.top) < 10 and self.speed_y > 0:
                self.speed_y = -self.speed_y  # Столкновение сверху
            elif abs(self.rect.top - brick.rect.bottom) < 10 and self.speed_y < 0:
                self.speed_y = -self.speed_y  # Столкновение снизу
            elif abs(self.rect.right - brick.rect.left) < 10 and self.speed_x > 0:
                self.speed_x = -self.speed_x  # Столкновение слева
            elif abs(self.rect.left - brick.rect.right) < 10 and self.speed_x < 0:
                self.speed_x = -self.speed_x  # Столкновение справа
            brick.take_damage()  # Наносим урон кирпичу

    def start_moving(self):
        self.is_moving = True


# Класс Кирпича
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__(bricks, all_sprites)
        if health == 1:
            self.image = load_image('brick_1.png')
        elif health == 2:
            self.image = load_image('brick_2.png')
        elif health == 3:
            self.image = load_image('brick_3.png')
        else:
            self.image = load_image('concrete_block.png')
            health = 100
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health  # Прочность кирпича

    def take_damage(self):
        self.health -= 1  # Уменьшаем прочность кирпича
        if self.health <= 0:
            self.kill()  # Удаляем кирпич, если прочность <= 0


player_image = load_image('game_stick.png')
ball_image = load_image('ball.png')

brick_width = 96
brick_height = 48

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
players = pygame.sprite.Group()
balls = pygame.sprite.Group()
borders = pygame.sprite.Group()

clock = pygame.time.Clock()

start_screen()

game_fon = pygame.transform.scale(load_image('game_background.png'), (W, H))
left_border = Border('lateral_border.png', 0, H - 711 - 13)
right_border = Border('lateral_border.png', W - 13, H - 711 - 13)
upper_border = Border('upper_border.png', 0, 0)
lower_border = Border('lower_border.png', 0, H - 13)

map_level = load_level('1.txt')
print(map_level)
level_x, level_y = generate_level(map_level)

player = Player()
ball = Ball()

# # Создаем кирпичи с разной прочностью
# for i in range(9):
#     for j in range(5):
#         health = random.randint(1, 4)  # Случайная прочность от 1 до 3
#         brick = Brick(i * (brick_width + 0) + 80, j * (brick_height + 0) + 50, health)
#         bricks.add(brick)
#         all_sprites.add(brick)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            ball.start_moving()

    screen.blit(game_fon, (0, 0))

    collisions = pygame.sprite.spritecollide(ball, bricks, False, pygame.sprite.collide_mask)
    for brick in collisions:
        ball.speed_y = -ball.speed_y  # Мяч отскакивает
        brick.take_damage()  # Наносим урон кирпичу

    # Проверка столкновений мяча с платформой
    if pygame.sprite.spritecollide(ball, players, False, pygame.sprite.collide_mask):
        ball.speed_y = -ball.speed_y

    # Проверка на проигрыш
    if ball.rect.bottom >= H:
        running = False

    all_sprites.draw(screen)

    mouse_x, _ = pygame.mouse.get_pos()
    player.update(mouse_x)

    ball.move()

    cursor_replacement()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
