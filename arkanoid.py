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
    def __init__(self, group, file_image, y):
        super().__init__()
        group.add(self)
        self.file_image = file_image
        self.image = load_image(file_image)
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = y

    def update(self, *args):
        mous_pos = pygame.mouse.get_pos()
        if self.rect.x <= mous_pos[0] <= self.rect.x + self.rect[2] and\
                self.rect.y <= mous_pos[1] <= self.rect.y + self.rect[3]:
            self.image = pygame.transform.scale(load_image(self.file_image), (450, 180))
            self.rect = self.image.get_rect()
            self.rect.x = W // 2 - self.rect[2] // 2
            self.rect.y = self.y
        else:
            self.image = load_image(self.file_image)
            self.rect = self.image.get_rect()
            self.rect.x = W // 2 - self.rect[2] // 2
            self.rect.y = self.y



def cursor_replacement():
    mouse_cursor = load_image("arrow.png")
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        x, y = pygame.mouse.get_pos()
        screen.blit(mouse_cursor, (x, y))


def start_screen():
    fon = pygame.transform.scale(load_image('starting_background.png'), (W, H))
    button_group = pygame.sprite.Group()
    start_button = Button(button_group, 'button_start.png', 484)
    rules_button = Button(button_group, 'rules_button.png', 320)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        screen.blit(fon, (0, 0))
        button_group.update(event)
        button_group.draw(screen)
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
