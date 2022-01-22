"""
    This first game
    check the import
"""

import random
import pygame
from pygame.locals import *
import time


pygame.init()


def game():
    screen = pygame.display.set_mode((700, 250))
    clock = pygame.time.Clock()

    font = pygame.font.Font("freesansbold.ttf", 20)
    # check_point = pygame.mixer.Sound("checkPoint.wav")
    # death_sound = pygame.mixer.Sound("die.wav")

    dino_icon = pygame.image.load("sprites/dino_.png")
    pygame.display.set_icon(dino_icon)

    pygame.display.set_caption("Dino Run")

    game_over = pygame.image.load("sprites/game_over.png")
    replay_button = pygame.image.load("sprites/replay_button.png")
    logo = pygame.image.load("sprites/logo.png")

    GREY = (240, 240, 240)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == "__main__":
    while True:
        game()

