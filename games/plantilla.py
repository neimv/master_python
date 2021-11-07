
import sys

import pygame
from pygame.locals import *

pygame.init()
ventana = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Titulo de la ventana")
color_fondo = (1, 150, 70)

while True:
    ventana.fill(color_fondo)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()

