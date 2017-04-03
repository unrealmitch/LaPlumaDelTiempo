import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from animacionesPygame import *
import random,math

class Capa():
	def __init__(self):
		#Permite imprimir por orden segun se anhaden, necesario para profundidad
		self.objects = []


	def add(self,object):
		self.objects.append(object)

	def update(self, time):
		for object in self.objects:
			object.update(time)

	def establecerPosicionPantalla(self,scroll):
		for object in self.objects:
			object.establecerPosicionPantalla(scroll)

	def draw(self,pantalla):
		for object in self.objects:
			object.draw(pantalla)