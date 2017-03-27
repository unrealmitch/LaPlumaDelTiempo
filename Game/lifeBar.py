import pygame

from miSprite import *
from pygame.locals import *

class LifeBar(MiSprite):

	def __init__(self):
		# Primero invocamos al constructor de la clase padre
		MiSprite.__init__(self)

		self.vida = 6

		# Se carga la hoja
		self.hoja = GestorRecursos.CargarImagen("dino_lifebar.png",-1)
		self.hoja = self.hoja.convert_alpha()

		# Leemos las coordenadas de un archivo de texto
		datos = GestorRecursos.CargarArchivoCoordenadas("dino_lifebar.txt")
		datos = datos.split()

		cont = 0
		
		self.coordenadasHoja = [];
		self.coordenadasHoja.append([])
		tmp = self.coordenadasHoja[0]
		for postura in range(1, 7+1):
			tmp.append(pygame.Rect((int(int(datos[cont])*ESCALA), int(int(datos[cont+1])*ESCALA)), (int(int(datos[cont+2])*ESCALA), int(int(datos[cont+3])*ESCALA))))
			cont += 4

		# El rectangulo del Sprite
		self.rect = pygame.Rect(0,20,self.coordenadasHoja[0][6][2],self.coordenadasHoja[0][6][3])

		self.image = self.hoja.subsurface(self.coordenadasHoja[0][6])

	def actualizarVida(self, vida):

		self.rect = pygame.Rect(0,20,self.coordenadasHoja[0][vida][2],self.coordenadasHoja[0][vida][3])
		self.image = self.hoja.subsurface(self.coordenadasHoja[0][vida])
