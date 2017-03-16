# -*- coding: utf-8 -*-

import random,math
import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from animacionesPygame import *
from piratas import Piratas

# -------------------------------------------------
# Clase EscenaCarga

class EscenaCarga(Escena):
    def __init__(self, director, recursos):
        Escena.__init__(self, director)
        self.tipoLetra = pygame.font.SysFont('arial', 48)
        self.texto = self.tipoLetra.render('#Loading mision 1...', True, (255,255,255), (0,0,0))

        self.conf_file = open (recursos, "r")
        self.conf_lines = self.conf_file.readlines ()
        self.it = iter (self.conf_lines)

    def update(self, tiempo):
        # Carga los elementos de la fase uno a uno en cada iteracion del bucle 
        # de eventos
        try:
            i = next(self.it, None)
            i = i[0:len(i)-1] # Quita el \n del final de las cadenas
            GestorRecursos.CargarImagenAlpha(i)
        except TypeError:
            # Entra después de cargar todas las lineas del iterador. No se puede
            # hacer len() de un tipo None. Ahora carga la escena del juego.
            escenaPiratas = Piratas(self.director)
            self.director.cambiarEscena(escenaPiratas)
            return

    def dibujar(self, pantalla):
        # Mostrar mensaje de espera
        pantalla.fill((0,0,0))
        pantalla.blit(self.texto, (ANCHO_PANTALLA/3-200,ALTO_PANTALLA/2-50,300,300))

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                self.director.salirPrograma()
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

