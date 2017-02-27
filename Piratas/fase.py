# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from animacionesPygame import *
import random,math


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
DEBUG = False
MINIMO_X_JUGADOR = ANCHO_PANTALLA  / 4
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
	def __init__(self, director):

		Escena.__init__(self, director)
		fH = ALTO_PANTALLA/800.	#!Factor de escala Y, para posicionar bien en este eje si se escala el decorado



		### ESCENARIO ###
		#self.background = StaticScenario('Fondo.png',(0.5,0))
		self.background = DynamicScenario('fondo',21,0,(0.5,0))
		self.decorado = StaticScenario('barco.png',(1,1))
		
		barco1 = autonomeSprite('Ship-Pirate-1.png',(100,50,1000,0,0.01,0.005),(0.25,0.25,0.33,0.33,0.000005,0.000005),(0.5,-0.5))
		barco2 = autonomeSprite('Ship-Pirate-1.png',(700,200,1000,0,0.002,0.001),(0.15,0.15,0.25,0.25,0.000001,0.000001),(0.5,0.25))
		#self.barcobg1 = BarcoBg(100,275)
		self.grupoEscenario = pygame.sprite.Group(barco1,barco2)

		# Que parte del decorado estamos visualizando
		self.scroll = (0,0.)
		self.scroll_waves = 0.01

		### JUGADORES ###
		self.jugador1 = Jugador()
		self.jugador1.establecerPosicion((300, fH*555))
		self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("plat-piratas.txt")
		plataformas = []
		self.grupoPlataformas = pygame.sprite.Group()

		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], fH*elem[1], elem[2], elem[3])))

		self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
		self.grupoSpritesDinamicos.add()

		self.grupoSprites = pygame.sprite.Group( self.jugador1 )
		self.grupoSprites.add(self.grupoPlataformas)

		### ANIMACIONES ###
		self.animacionOlas = []
		for i in range(3):
			animacionOla = AnimacionOla2()
			animacionOla.posicionx = 510*i
			animacionOla.posiciony = 420
			animacionOla.nextFrame(i*10)
			animacionOla.play()
			self.animacionOlas.append(animacionOla)

		### Sonido ###
		sound_bso = GestorRecursos.CargarSonido('bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('test.ogg')
		channel_bso = sound_bso.play(-1)
		channel_ambient = sound_ambient.play(-1)

		#sound = pygame.mixer.Sound('test.ogg')
		#channel = sound.play();

	def actualizarScrollOrdenados(self, jugador):
		if (jugador.rect.left<MINIMO_X_JUGADOR):
			desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

			if self.scroll[0] <= 0:
				self.scroll = (0, self.scroll[1])
				jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] - desplazamiento, self.scroll[1])
				return True;

		if (jugador.rect.right>MAXIMO_X_JUGADOR):
			desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

			if self.scroll[0] + ANCHO_PANTALLA >= self.decorado.rect.right:
				self.scroll = (self.decorado.rect.right - ANCHO_PANTALLA, self.scroll[1])
				jugador.establecerPosicion((self.scroll[0]+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] + desplazamiento, self.scroll[1]);
				return True;

		return False;


	def actualizarScroll(self, jugador):
		if (self.scroll[1] > 1 or self.scroll[1] < 0):
			self.scroll_waves = -self.scroll_waves

		self.scroll = (self.scroll[0], self.scroll[1] + self.scroll_waves)
		virtual_scroll = (int(self.scroll[0]), int(math.sin(self.scroll[1]) * 30))

		cambioScroll = self.actualizarScrollOrdenados(jugador)

		self.decorado.establecerPosicionPantalla(virtual_scroll)
		self.background.establecerPosicionPantalla(virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(virtual_scroll)

		for sprite in iter(self.grupoEscenario):
			sprite.establecerPosicionPantalla(virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(virtual_scroll)

	def update(self, tiempo):
		self.background.update(tiempo)
		self.grupoSpritesDinamicos.update(self.grupoPlataformas,tiempo)
		self.grupoEscenario.update(tiempo)
		self.actualizarScroll(self.jugador1)
		
	def dibujar(self, pantalla):
		pantalla.fill((0,0,0))
		self.background.draw(pantalla)
		self.grupoEscenario.draw(pantalla)
		self.decorado.draw(pantalla)
		
		# Luego los Sprites
		self.grupoSprites.draw(pantalla)

		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)

		for animacion in self.animacionOlas:
			animacion.dibujar(pantalla)

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN and evento.key == K_ESCAPE:
				self.director.salirPrograma()
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		teclasPulsadas = pygame.key.get_pressed()
		self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)