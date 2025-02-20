import os
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'block':
            self.add(blocks_group)
            self.endurance = 100
        elif tile_type == 'brick_1':
            self.add(bricks_group)
            self.endurance = 1
        elif tile_type == 'brick_2':
            self.add(bricks_group)
            self.endurance = 2
        elif tile_type == 'brick_3':
            self.add(bricks_group)
            self.endurance = 3
        self.rect = self.image.get_rect().move(
            80 + tile_width * pos_x, 49 + tile_height * pos_y)
        self.pos = (pos_x, pos_y)


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                Tile('brick_1', x, y)
            elif level[y][x] == 'y':
                Tile('brick_2', x, y)
            elif level[y][x] == 'z':
                Tile('brick_3', x, y)
            elif level[y][x] == '#':
                Tile('block', x, y)
    return x, y


class Border(pygame.sprite.Sprite):
    def __init__(self, border_image, x, y):
        super().__init__(borders_group, all_sprites)
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
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = 668 - self.rect[3] // 2
        self.pos = (self.rect.x, self.rect.y)

    def update(self, *args, **kwargs):
        pass

    def move(self, dx, dy):
        pass


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(balls_group, all_sprites)
        self.image = ball_image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = player.pos[1] - 10
        self.pos = (self.rect.x, self.rect.y)

    def update(self, *args, **kwargs):
        pass


    def move(self, dx, dy):
        pass


tile_images = {
    'brick_1': load_image('brick_1.png'),
    'brick_2': load_image('brick_2.png'),
    'brick_3': load_image('brick_3.png'),
    'block': load_image('concrete_block.png')
}
player_image = load_image('game_stick.png')
ball_image = load_image('ball.png')

tile_width = 96
tile_height = 48

all_sprites = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
balls_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()

clock = pygame.time.Clock()

start_screen()

game_fon = pygame.transform.scale(load_image('game_background.png'), (W, H))
left_border = Border('lateral_border.png', 0, H - 711 - 13)
right_border = Border('lateral_border.png', W - 13, H - 711 - 13)
upper_border = Border('upper_border.png', 0, 0)
lower_border = Border('lower_border.png', 0, H - 13)

map_level = load_level('1.txt')
level_x, level_y = generate_level(map_level)

player = Player()
ball = Ball()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(game_fon, (0, 0))
    all_sprites.draw(screen)
    ball.update()
    cursor_replacement()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
