# -*- coding: utf-8 -*-

import random,math
import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from animacionesPygame import *
from piratas import Piratas
from dinosaurios import Dinosaurios
from piratas_arcade import Piratas_Arcade
from gestorRecursos import *
from escenaCarga import EscenaCarga

# -------------------------------------------------
# Clase EscenaCarga

class EscenaTexto(EscenaPygame):
    def __init__(self, director, fase):
    	self.fase = fase
        EscenaPygame.__init__(self, director)
        self.imagen = GestorRecursos.CargarImagen('VeilRoom1.jpg')
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        
    def update(self, tiempo):
        return

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN and evento.key == K_SPACE:
                escena = EscenaCarga(self.director, self.fase)
                self.director.cambiarEscena(escena)
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

