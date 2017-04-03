# -*- coding: utf-8 -*-

import random,math
import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from gestorRecursos import *

# -------------------------------------------------
# Clase EscenaHistoria

class EscenaHistoria(EscenaPygame):
	def __init__(self, director, fase):
		EscenaPygame.__init__(self, director)
		self.fase = fase
		self.actual = [0,0]
		self.fade = 0
		if fase == 0:
			GestorRecursos.CargarSonido('intro_1.ogg').play()
			self.imagenes = [[],[],[]]
			self.delay = [[2,2,2,2,2,2],[2],[2,2,2,2,2,2,2]]
			self.fondos = ['f1.jpg', 'f2.png', 'f3.jpg']
			for i in range(1,6):
				self.imagenes[0].append('texto' + str(i) + '.png')
			self.imagenes[1].append('texto6.png')
			for i in range(7,13):
				self.imagenes[2].append('texto' + str(i) + '.png')

		self.imagen = None
		self.rect = None
		self.imagen_fondo = None
		self.change_image()
		self.change_fondo()
		self.contador = pygame.time.get_ticks() + self.delay[0][0] * 1000
		self.space_blocked = False

	def change_fondo(self):
		self.imagen_fondo = GestorRecursos.CargarImagenH(self.fondos[self.actual[0]])
		self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
		
	def change_image(self):
		self.imagen = GestorRecursos.CargarImagenH(self.imagenes[self.actual[0]][self.actual[1]],-1)
		self.rect = self.imagen.get_rect()
		self.rect.center = (ANCHO_PANTALLA/2, ALTO_PANTALLA/2)

	def update(self, tiempo):
		time = pygame.time.get_ticks()
		if time > self.contador:
			
				self.fade = 0
				if(self.actual[1] == len(self.imagenes[self.actual[0]]) - 1):
					if self.fade < 50:
						self.fade = 0
						if(self.actual[0] == len(self.imagenes) -1):
							self.director.salirEscena();
						else:
							self.fade = 0
							self.actual[0]+=1
							self.actual[1]=0
							self.change_fondo()
							self.change_image()
					else:
						self.fade -= 20
				else:
					self.actual[1]+=1
					self.change_image()

				self.contador = time + self.delay[self.actual[0]][self.actual[1]] * 1000

		else:
			if self.fade < 255: self.fade += 10
		


	def dibujar(self, pantalla):
		pantalla.fill((0,0,0))
		self.imagen_fondo.set_alpha(self.fade)
		pantalla.blit(self.imagen_fondo, (0,0))

		self.imagen.set_alpha(self.fade)
		#pantalla.blit(self.imagen, self.imagen.get_rect())
		pantalla.blit(self.imagen, self.rect)

		tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 24)
		texto = tipoLetra.render("SPACE: Siguiente - ESC: Omitir", True, (255,255,255))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, ALTO_PANTALLA*0.95)
		pantalla.blit(texto, rect)
		
	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				if evento.key == K_SPACE and not self.space_blocked:
					self.contador = 0
					self.space_blocked = True
				if evento.key == K_ESCAPE:
					self.director.salirEscena();

			if evento.type == KEYUP:
				if evento.key == K_SPACE:
					self.space_blocked = False
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

