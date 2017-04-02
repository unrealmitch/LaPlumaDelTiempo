# -*- coding: utf-8 -*-

import random,math
import pygame, escena

from escena import *
from personajes import *
from escenario import *
from capa import *
from lifeBar import *
from pygame.locals import *
from animacionesPygame import *
from fase_arcade import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
DEBUG = False
MINIMO_X_JUGADOR = (ANCHO_PANTALLA  / 3)
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Piratas

class Piratas_Arcade(Fase_arcade):
	def __init__(self, director):

		Fase_arcade.__init__(self, director, 'PIRATAS_LVL')
		self.scroll = (1100*ESCALA,0.)

	def setEscenario(self):
		### ESCENARIO ###
		if DEBUG:
			background = StaticScenario('pirata_fondo.png',(0.3,0))
		else:
			background = DynamicScenario("animations/pirata_fondo",21,0,(0.3,0))

		self.capaEscenario.add(background)
		
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(1700,300,0,0,0,0),(-0.6,0.6,0,0,0,0),(0.86,-0.86)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(1550,250,0,0,0,0),(-0.75,0.75,0,0,0,0),(0.88,-0.88)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(1400,200,0,0,0,0),(-0.9,0.9,0,0,0,0),(0.9,-0.9)))
		
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5400,240,0,0,0,0),(0.7,0.7,0,0,0,0),(0.86,0.86)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5300,250,0,0,0,0),(0.75,0.75,0,0,0,0),(0.88,0.88)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5200,250,0,0,0,0),(0.8,0.8,0,0,0,0),(0.9,0.9)))

		decorado = StaticScenario('pirata_escenario.png',(1,1))
		self.capaEscenario.add(decorado)
		self.max_x = decorado.rect.right

	def setPlataformas(self):
		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("pirata_plataform.txt")
		plataformas = []
		
		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], elem[1], elem[2], elem[3]),elem[4]))

	def setJugador(self):
		self.jugador1 = Jugador(PLAYER_PIRATA)
		self.jugador1.establecerPosicion((1820*ESCALA, 400*ESCALA))

	def setEnemigos(self):
		self.final = None

	def setAnim(self):
		for i in range(int(ANCHO_PANTALLA/(400*ESCALA))):
			animacionOla = AnimacionOlas()
			pyganim.PygAnimation.scale(animacionOla, (int(510*ESCALA), int(390*ESCALA)))
			animacionOla.posicionx = 509*i*ESCALA
			animacionOla.posiciony = 420*ESCALA
			self.animacion.append(animacionOla)
		
		for elem in self.animacion:
			elem.play()

	def setAudio(self):
		sound_bso = GestorRecursos.CargarSonido('arcade_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('pirata_ambient.ogg')
		pygame.mixer.stop();
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0.5)
		self.channel_ambient = sound_ambient.play(-1)

	## FUNCIONES ARCADE ##
