
import sys

import pygame
from pygame.locals import *

pygame.init()
ventana = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Titulo de la ventana")
color_fondo = (1, 150, 70)
color_linea = (255, 128, 0)
color_circulo = (255, 255, 0)
color_figuras = (205, 0, 155)

while True:
    ventana.fill(color_fondo)
    # lines
    pygame.draw.line(ventana, color_linea, (60, 90), (200, 100), 40)
    pygame.draw.line(ventana, color_linea, (80, 190), (100, 150), 20)
    pygame.draw.line(ventana, color_linea, (10, 30), (250, 190), 10)
    # circles
    pygame.draw.circle(ventana, color_circulo, (400, 100), 100, 30)
    pygame.draw.circle(ventana, color_circulo, (500, 150), 40, 20)
    # figuras
    pygame.draw.rect(ventana, color_figuras, (100, 200, 120, 250))
    pygame.draw.polygon(
        ventana, color_figuras,
        ((400, 400), (500, 400), (500, 500), (400, 500))
    ) # este es completamente movible o se puede cambiar de forma

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()
