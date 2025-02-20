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

def cursor_replacement():
    mouse_cursor = load_image("arrow.png")
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        x, y = pygame.mouse.get_pos()
        screen.blit(mouse_cursor, (x, y))

def start_screen():
    fon = pygame.transform.scale(load_image('starting_background.png'), (W, H))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        screen.blit(fon, (0, 0))
        cursor_replacement()

        clock.tick(FPS)


clock = pygame.time.Clock()

start_screen()

game_fon = pygame.transform.scale(load_image('game_background.png'), (W, H))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(game_fon, (0, 0))
    cursor_replacement()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
