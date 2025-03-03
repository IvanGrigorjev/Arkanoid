import os
import random
import sys
from pprint import pprint

import pygame
from pygame import font

WINDOW_SIZE = W, H = 1024, 727
FPS = 60

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Арканоид')

# Загрузка звуков
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("sound/hit.wav")  # Звук удара мяча о платформу
brick_sound = pygame.mixer.Sound("sound/brick.wav")  # Звук удара мяча о кирпич
lose_sound = pygame.mixer.Sound("sound/lose.wav")  # Звук потери жизни
win_sound = pygame.mixer.Sound("sound/win.wav")  # Звук завершения раунда


# Функция загрузки изображений из вложенной папки DATA
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


# Класс для кнопок стартового меню
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


# Функция подмены курсора мыши
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
            rules_image = load_image('rules.png')
            screen.blit(rules_image, (150, 350))
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
    def __init__(self, health=3):
        super().__init__(players, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = W // 2 - self.rect[2] // 2
        self.rect.y = 668 - self.rect[3] // 2
        self.pos = (self.rect.x, self.rect.y)
        self.width = self.rect[2]
        self.height = self.rect[3]

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
        self.rect.x = (W - self.rect[2]) // 2
        self.rect.y = player.pos[1] - 12
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
            self.rect.x = player.rect.x + player.width // 2.2

    def start_moving(self):
        self.is_moving = True

    def reset_position(self):
        # Сбрасываем позицию мяча на платформу
        self.rect.x = (W - self.rect[2]) // 2
        self.rect.y = player.pos[1] - 12
        self.is_moving = False

    def up_speed(self):
        # Увеличиваем скорость мяча
        self.speed_x *= 1.2
        self.speed_y *= 1.2


# Класс Кирпича
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__(blocks, all_sprites)
        if health == 1:
            self.image = load_image('brick_1.png')
            self.add(bricks)
        elif health == 2:
            self.image = load_image('brick_2.png')
            self.add(bricks)
        elif health == 3:
            self.image = load_image('brick_3.png')
            self.add(bricks)
        else:
            self.image = load_image('concrete_block.png')
            health = 1000
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health  # Прочность кирпича
        self.points = health * 10  # Очки за разрушение кирпича
        self.mask = pygame.mask.from_surface(self.image)  # Маска для коллизий

    def update(self):
        if self.health == 1:
            self.image = load_image('brick_1.png')
        elif self.health == 2:
            self.image = load_image('brick_2.png')
        elif self.health == 3:
            self.image = load_image('brick_3.png')

    def take_damage(self):
        self.health -= 1  # Уменьшаем прочность кирпича
        if self.health <= 0:
            self.kill()  # Удаляем кирпич, если прочность <= 0
            return self.points  # Возвращаем очки за разрушение кирпича
        return 0


# Картинка для спрайта платформы
player_image = load_image('game_stick.png')

# Жизни игрока
lives = 3

# Счет игрока
score = 0

# Пауза
paused = False

# Картинка для мячика
ball_image = load_image('ball.png')

# Размеры кирпичей
brick_width = 96
brick_height = 48

# Группы спрайтов
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
blocks = pygame.sprite.Group()
players = pygame.sprite.Group()
balls = pygame.sprite.Group()
borders = pygame.sprite.Group()

clock = pygame.time.Clock()

# Начинаем игру со стратового экрана
start_screen()

round_number = 1  # Начинаем с первого раунда

game_fon = pygame.transform.scale(load_image('game_background.png'), (W, H))
left_border = Border('lateral_border.png', 0, H - 711 - 13)
right_border = Border('lateral_border.png', W - 13, H - 711 - 13)
upper_border = Border('upper_border.png', 0, 0)
lower_border = Border('lower_border.png', 0, H - 13)

map_level = load_level('1.txt')
level_x, level_y = generate_level(map_level)

player = Player()
ball = Ball()

game_over = load_image('end_backround.png')
game_over.set_alpha(0)
game_over_flag = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            ball.start_moving()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Пауза при нажатии P
                paused = not paused

    font = pygame.font.Font(None, 36)

    if not paused:
        screen.blit(game_fon, (0, 0))

        collisions = pygame.sprite.spritecollide(ball, blocks, False, pygame.sprite.collide_mask)
        for brick in collisions:
            # Определяем, с какой стороны произошло столкновение
            if abs(ball.rect.bottom - brick.rect.top) < 10 and ball.speed_y > 0:
                ball.speed_y = -ball.speed_y  # Столкновение сверху
            elif abs(ball.rect.top - brick.rect.bottom) < 10 and ball.speed_y < 0:
                ball.speed_y = -ball.speed_y  # Столкновение снизу
            elif abs(ball.rect.right - brick.rect.left) < 10 and ball.speed_x > 0:
                ball.speed_x = -ball.speed_x  # Столкновение слева
            elif abs(ball.rect.left - brick.rect.right) < 10 and ball.speed_x < 0:
                ball.speed_x = -ball.speed_x  # Столкновение справа
            score += brick.take_damage()  # Увеличиваем счет за разрушение кирпича
            brick_sound.play()  # Воспроизводим звук удара о кирпич

        # Проверка столкновений мяча с платформой
        if pygame.sprite.collide_mask(ball, player):
            ball.speed_y = -ball.speed_y
            hit_sound.play()  # Воспроизводим звук удара о платформу

        # Проверка на потерю жизни
        if ball.rect.bottom >= H:
            lose_sound.play()  # Воспроизводим звук потери жизни
            lives -= 1  # Уменьшаем количество жизней
            if lives <= 0:
                game_over_flag = True
                for brick in blocks:
                    brick.kill()
                player.kill()
                screen.blit(game_over, (0, 0))
                game_over.set_alpha(game_over.get_alpha() + 4)  # Игра завершается, если жизни закончились
            else:
                ball.reset_position()  # Перезапускаем мяч на платформе

        if len(bricks) == 0 and not game_over_flag:
            if round_number == 1:
                # Переход ко второму раунду
                win_sound.play()  # Воспроизводим звук завершения раунда
                round_number = 2
                ball.up_speed()  # Увеличиваем скорость мяча
                map_level = load_level('2.txt')
                level_x, level_y = generate_level(map_level)
                ball.reset_position()  # Перезапускаем мяч на платформе
            else:
                win_sound.play()  # Воспроизводим звук завершения раунда
                player.kill()
                ball.kill()
                for brick in blocks:
                    brick.kill()
                screen.blit(game_over, (0, 0))
                game_over.set_alpha(game_over.get_alpha() + 4)

        mouse_x, _ = pygame.mouse.get_pos()
        player.update(mouse_x)

        ball.move()

        bricks.update()

        # Отображение количества жизней и очки
        for i in range(lives):
            lives_images = pygame.transform.scale_by(load_image('health.png'), 0.7)
            screen.blit(lives_images, (20 + i * 40, 670))
        score_text = font.render(f"Очки: {score}", True, "BLACK")
        screen.blit(score_text, (W - 200, 686))

    if paused:
        screen.fill((100, 100, 100))
        pause_text = font.render("Пауза", True, "WHITE")
        screen.blit(pause_text, (W // 2 - 40, H // 2))

    all_sprites.draw(screen)

    cursor_replacement()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
