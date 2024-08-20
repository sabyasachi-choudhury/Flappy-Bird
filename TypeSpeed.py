import random
import time
import pygame
from pygame.locals import *

pygame.init()

run = True
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Comic Sans MS', 30)
typing = False


def round_to(num, target):
    return round(num/target) * target


class Input:
    def __init__(self):
        self.surf = pygame.Surface((300, 50))
        self.rect = self.surf.get_rect(center=(300, 200))
        self.surf.fill((65, 82, 255))
        self.in_word = ''
        self.in_word_surf = font.render(self.in_word, False, (255, 255, 255))
        self.in_word_rect = self.in_word_surf.get_rect(center=self.rect.center)
        self.correct = False

    def check(self):
        global typing
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            typing = True
        else:
            typing = False

    def type(self, e):
        if typing:
            if e.key != K_RETURN:
                self.in_word += e.unicode
            if e.key == K_BACKSPACE:
                self.in_word = ''.join(list(self.in_word)[:-2])

        self.in_word_surf = font.render(self.in_word, False, (255, 255, 255))
        self.in_word_rect = self.in_word_surf.get_rect(center=self.rect.center)

    def submit(self, e, d):
        if typing:
            if e.key == K_RETURN:
                if self.in_word == d.word:
                    self.correct = True
                    print("good!")
                else:
                    self.correct = False
                    print('oops!')
                self.in_word = ''
                d.new_word()


class Start:
    def __init__(self):
        super(Start, self).__init__()
        self.base = pygame.Surface((150, 50))
        self.brect = self.base.get_rect(center=(300, 260))
        self.base.fill((231, 16, 13))
        self.surf = font.render('START', False, (255, 255, 255))
        self.rect = self.surf.get_rect(center=(300, 260))
        self.start_time, self.timed_time = 0, 0
        self.timing = False

    def time(self, e):
        if e.type == MOUSEBUTTONDOWN:
            if self.brect.collidepoint(pygame.mouse.get_pos()):
                if not self.timing:
                    self.timing = True
                    self.start_time = time.time()
                    self.base.fill((48, 231, 13))
                else:
                    self.timing = False
                    self.timed_time = time.time() - self.start_time
                    self.base.fill((231, 16, 13))
                    print(self.timed_time)
        if e.type == KEYDOWN:
            if e.key == K_RETURN:
                self.timing = False
                self.timed_time = time.time() - self.start_time
                self.base.fill((231, 16, 13))
                print(self.timed_time)


class TimeDisplay:
    def __init__(self, st):
        super(TimeDisplay, self).__init__()
        self.surf = font.render('0:00', False, (0, 24, 102))
        self.rect = self.surf.get_rect(center=(50, 30))

    def change_time(self, st):
        self.surf = font.render(str(round_to(st.timed_time, 0.01)), False, (0, 24, 102))
        self.rect = self.surf.get_rect(center=(50, 30))


class Result:
    def __init__(self):
        super(Result, self).__init__()
        self.surf = font.render('Start!', False, (0, 24, 102))
        self.rect = self.surf.get_rect(center=(530, 30))

    def display_result(self, inp):
        if inp.correct:
            self.surf = font.render('Yes!', False, (0, 24, 102))
        else:
            self.surf = font.render('Oops!', False, (0, 24, 102))


class Display:
    def __init__(self):
        super(Display, self).__init__()
        self.surf = pygame.Surface((200, 50))
        self.rect = self.surf.get_rect(center=(300, 140))
        self.surf.fill((255, 255, 255))

        self.words = ['abstract', 'microscope', 'psychopathic', 'serious', 'programming', 'intellectual', 'sufferer',
                      'reference', 'incongruous', 'perseverance', 'indict', 'embarrassed', 'exaggerated']
        self.word = random.choice(self.words)
        self.word_surf = font.render(self.word, False, (0, 199, 32))
        self.word_rect = self.word_surf.get_rect(center=self.rect.center)

    def new_word(self):
        self.word = random.choice(self.words)
        self.word_surf = font.render(self.word, False, (0, 199, 32))
        self.word_rect = self.word_surf.get_rect(center=self.rect.center)
        self.rect.width = self.word_rect.width + 10


board = Input()
start = Start()
display = Display()
time_display = TimeDisplay(start)
result = Result()

while run:
    screen.fill((65, 255, 255))
    time_display.change_time(start)

    for event in pygame.event.get():
        start.time(event)
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            board.submit(event, display)
            board.check()
            board.type(event)
            result.display_result(board)
            if event.key == K_ESCAPE:
                run = False
        if event.type == MOUSEBUTTONDOWN:
            board.check()

    screen.blit(board.surf, board.rect)
    screen.blit(start.base, start.brect)
    screen.blit(start.surf, start.rect)
    screen.blit(display.surf, display.rect)
    screen.blit(display.word_surf, display.word_rect)
    screen.blit(board.in_word_surf, board.in_word_rect)
    screen.blit(time_display.surf, time_display.rect)
    screen.blit(result.surf, result.rect)

    pygame.time.Clock().tick(30)
    pygame.display.flip()

pygame.quit()