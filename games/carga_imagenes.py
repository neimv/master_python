
import sys
from random import randint

import pygame
from pygame.locals import *

pygame.init()
ventana = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Titulo de la ventana")
color_fondo = (1, 150, 70)
color_rectangulo = (255, 60, 40)
# Carga imagen
imagen = pygame.image.load("imagenes/pygame-head-party.png")
# Position of image
pos_x, pos_y = (10, 40)

while True:
    ventana.fill(color_fondo)
    ventana.blit(imagen, (pos_x, pos_y))

    for i in range(10):
        pos_x, pos_y = randint(1, 700), randint(1, 500)
        pygame.draw.rect(ventana, color_rectangulo, (pos_x, pos_y, 50, 80))

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()

