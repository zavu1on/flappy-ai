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

speed = 1


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

    def jump(self):
        self.vel = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1

        s = self.vel * self.time + 1.5 * self.time ** 2

        if s >= 16:  # ограничиваем бесконечное ускорение при падении
            s = 16
        elif s < 0:
            s -= 2

        self.y += s

        # ограничиваем бесконечный поворот птички
        if s < 0 or self.y < self.height + 50:
            self.deg = self.MAX_ROTATION
        elif self.deg > -90:
            self.deg -= self.ROT_VELOCITY

    def draw(self, win):
        self.anim_count += 1

        # анимируем птичку
        if self.anim_count <= self.ANIM_TIME:
            self.img = BIRD_SPRITES[0]
        elif self.anim_count <= self.ANIM_TIME * 2:
            self.img = BIRD_SPRITES[1]
        elif self.anim_count <= self.ANIM_TIME * 3:
            self.img = BIRD_SPRITES[2]
        elif self.anim_count <= self.ANIM_TIME * 4:
            self.img = BIRD_SPRITES[1]
        elif self.anim_count == self.ANIM_TIME * 4 + 1:
            self.img = BIRD_SPRITES[0]
            self.anim_count = 0

        # если птичка падает, делаем картинку статичной
        if self.deg <= -80:
            self.img = BIRD_SPRITES[1]
            self.anim_count = self.ANIM_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.deg)
        render_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )

        win.blit(rotated_image, render_rect.topleft)  # рисуем птичку

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class PipePair:
    GAP = 200  # расстояние между трубами
    VEL = 5

    def __init__(self, x):
        self.x = x

        self.PIPE_TOP = pygame.transform.flip(PIPE_SPRITE, False, True)  # отражаем спрайт по горизонтали
        self.PIPE_BOTTOM = PIPE_SPRITE

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()  # нижня точка верхней трубы
        self.bottom = self.height + self.GAP  # верхняя точка нижней трубы

        self.passed = False

    def move(self):
        self.x -= self.VEL * speed

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # получаем маски
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # высчитываем смещение
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # ищем пересечения
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return b_point or t_point


class Base:
    VEL = 5
    WIDTH = BASE_SPRITE.get_width()
    IMG = BASE_SPRITE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # поочередно меняем платформы
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_SPRITE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    text = font.render(f'Score: {score}', True, (255, 255, 255))
    win.blit(text, (W - 10 - text.get_width(), 10))

    pygame.display.update()


win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

bird = Bird(230, 350)
base = Base(730)
pipes = [PipePair(700)]

score = 0

while True:
    rm_list = []
    add_pipe = False

    clock.tick(30)  # устанавливаем FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # обработчик закрытия игры
            exit()
        if event.type == pygame.KEYDOWN and event.key == 32:
            bird.jump()

    for pipe in pipes:
        pipe.move()

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            # если труба уплыла за экран
            rm_list.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
            # если птичка перелетела через трубу
            speed += .05
            pipe.passed = True
            add_pipe = True

        if pipe.collide(bird):
            print(score)
            exit()

    if add_pipe:
        score += 1
        pipes.append(PipePair(700))

    for r in rm_list:
        pipes.remove(r)

    bird.move()
    base.move()

    draw_window(win, bird, pipes, base, score)
