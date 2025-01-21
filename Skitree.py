import pygame
import random as rn

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clown Game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("background.png")
clock = pygame.time.Clock()
FPS = 60
running = True
score = 0
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.x = 0
        self.y = 0
        self.speed = 7

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.image.get_height():
            self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self):
        self.image =pygame.image.load('tree.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.new()

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def move(self):
        global score
        self.x -= self.speed
        if self.x < -self.image.get_width():
            self.new()
            score += 1

    def new(self):
        self.x = rn.randint(WIDTH, WIDTH + 200)
        self.y = rn.randint(0, HEIGHT - self.image.get_height())
        self.speed = 5

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player = Player()
enemies = [Enemy() for _ in range(3)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    for enemy in enemies:
        enemy.move()
        if player.rect.colliderect(enemy.rect):
            game_over_font = pygame.font.SysFont(None, 50)
            game_over_text = game_over_font.render(
                f"Score: {score} - Press any key to play again!", True, (255, 0, 0)
            )
            screen.blit(bg, (0, 0))
            screen.blit(game_over_text, (100, HEIGHT // 2))
            pygame.display.flip()

            lose = True
            while lose:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        for enemy in enemies:
                            enemy.new()
                        score = 0
                        lose = False

    screen.blit(bg, (0, 0))
    player.draw()
    for enemy in enemies:
        enemy.draw()
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

