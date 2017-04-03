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
	# Clase para recrear una secuencia de escenas de diálogo
	# self.actual: [Escenario actual[Fondo], Diálogo actual]
	# self.image & self.time: Arrays bidimensionales para cada escena de dialogo:
	# La primera dimension indica el escenario (mismo fondo), mientras la segunda el dialogo actual
	# En el de imagenes estan las imagenes de dialogo y en delay la espera en cada dialogo
	# En self.fondos estan los escenarios
	# Self.fade indica el fundido actual (0=totalmente en negro)
	# El fundido se aplica al entrar y salir de la EscenaHistoria, así como en la transiccion entre escenarios [fondos]

		EscenaPygame.__init__(self, director)
		self.fase = fase
		self.actual = [0,0]
		self.fade = 0
		if fase == 0:
			GestorRecursos.CargarSonido('intro_1.ogg').play()
			self.imagenes = [[],[],[]]
			self.delay = [[8,3,10,14,3],[8],[8,10,14,14,12,3]]
			self.fondos = ['f1.jpg', 'f2.png', 'f3.jpg']
			for i in range(1,6):
				self.imagenes[0].append('texto' + str(i) + '.png')
			self.imagenes[1].append('texto6.png')
			for i in range(7,13):
				self.imagenes[2].append('texto' + str(i) + '.png')
		else:
			raise 'Not implemented yet'

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
		if self.imagenes[self.actual[0]][self.actual[1]] != None
			self.imagen = GestorRecursos.CargarImagenH(self.imagenes[self.actual[0]][self.actual[1]])
			self.rect = self.imagen.get_rect()
			self.rect.center = (ANCHO_PANTALLA/2, ALTO_PANTALLA/2)
		else
			self.imagen = None

	def update(self, tiempo):
		#Comprobamos si ha pasado el tiempo de retado y cambias a la siguiente escena de diálogo, o en caso de que termine, la siguiente escena [diferente fondo]
		time = pygame.time.get_ticks()
		if time > self.contador:
				if(self.actual[1] == len(self.imagenes[self.actual[0]]) - 1):
					if self.fade < 50:
						if(self.actual[0] == len(self.imagenes) -1):
							self.director.salirEscena();
						else:
							self.fade = 0
							self.actual[0]+=1
							self.actual[1]=0
							self.change_fondo()
							self.change_image()
							self.contador = time + self.delay[self.actual[0]][self.actual[1]] * 1000
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
		if self.imagen != None
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

