# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from miSprite import *
from gestorRecursos import *
from personajes import GRAVEDAD

#Objetos
CORAZON = 1
RON = 2
ESPADA = 3
BOTAS = 4
MUELLE = 5

#Clase objeto, un simple misprite que almacena el tipo de objeto, el sonido que hace al cogerse
#y permite al objeto caer mientras no está sobre una plataforma
class Objeto(MiSprite):
	def __init__(self, tipo, image, sound_pick = 'arcade_life.ogg'):
		MiSprite.__init__(self);
		self.tipo = tipo
		self.image = GestorRecursos.CargarImagen(image, -1)
		self.rect = self.image.get_rect()
		self.sound_pick = sound_pick
		self.falling = False

	def mover(self,grupoPlataformas):
		if pygame.sprite.spritecollide(self, grupoPlataformas, False) == []:
			self.falling = True
		else:
			self.falling = False
		
	def update(self,grupoPlataformas,tiempo):

		if pygame.sprite.spritecollide(self, grupoPlataformas, False) == []:
			self.falling = True
		else:
			self.falling = False

		velocidadx, velocidady = self.velocidad

		if self.falling:
			velocidady += GRAVEDAD * float(tiempo) 
		else: 
			velocidady = 0

		self.velocidad = (velocidadx, velocidady)
		MiSprite.update(self, tiempo)