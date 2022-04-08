import random
import pygame
pygame.init()

W = 550
H = 800

# загружаем картинки у увеличиваем их в 2 раза
BIRD_SPRITES = [
    pygame.transform.scale2x(pygame.image.load('sprites/bird1.png')),
    pygame.transform.scale2x(pygame.image.load('sprites/bird2.png')),
    pygame.transform.scale2x(pygame.image.load('sprites/bird3.png')),
]
PIPE_SPRITE = pygame.transform.scale2x(pygame.image.load('sprites/pipe.png'))
BASE_SPRITE = pygame.transform.scale2x(pygame.image.load('sprites/base.png'))
BG_SPRITE = pygame.transform.scale2x(pygame.image.load('sprites/bg.png'))
font = pygame.font.SysFont('Arial', 32)


class Base:
    WIDTH = BASE_SPRITE.get_width() - 2
    VEL = 5
    Y = 730

    def __init__(self):
        pass

    def draw(self, win):
        pass

    def move(self):
        pass


class Bird:
    MAX_ROTATION = 25
    ROT_VELOCITY = 20
    ANIM_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.deg = 0
        self.time = 0
        self.vel = 0
        self.height = self.y
        self.anim_count = 0
        self.img = BIRD_SPRITES[0]

    def draw(self, win):
        pass

    def move(self):
        # не забудь про анимацию падения
        pass

    def jump(self):
        pass

    def get_mask(self):
        pass


class Pipe:
    GAP = 200  # расстояние между трубами
    VEL = 5

    def __init__(self, x):
        self.x = x

        self.PIPE_TOP = pygame.transform.flip(PIPE_SPRITE, False, True)  # отражаем спрайт по горизонтали
        self.PIPE_BOTTOM = PIPE_SPRITE

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()  # верхняя точка верхней трубы
        self.bottom = self.height + self.GAP  # верхняя точка нижней трубы

        self.passed = False

    def move(self):
        pass

    def draw(self, win):
        pass

    def collide(self, bird):
        pass


def draw_window(win):
    # рисуем всё здесь
    win.blit(BG_SPRITE, (0, 0))

    pygame.display.update()


win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


while True:
    clock.tick(30)  # задаём FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    draw_window(win)
