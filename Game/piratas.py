# -*- coding: utf-8 -*-

import random,math
import pygame, escena

from escena import *
from personajes import *
from escenario import *
from capa import *
from pygame.locals import *
from animacionesPygame import *
from fase import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
DEBUG = False

# -------------------------------------------------
# Clase Piratas

class Piratas(Fase):
	def __init__(self, director):
		Fase.__init__(self, director, 'PIRATAS_LVL')

	def setEscenario(self):
		### ESCENARIO ###
		if DEBUG:
			background = StaticScenario('pirata_fondo.png',(0.3,0))
		else:
			background = DynamicScenario("animations/pirata_fondo",21,0,(0.3,0))

		self.capaEscenario.add(background)
		
		# Pendiente hacerlo modular [Cargarlo de ficherp]
		# autonomeSprite(image, (startX, startY, maxX, maxY, velX, velY), (startScaleX, startScaleY, maxScaleX, maxScaley, velScaleX, velScaleY), (velScrollX, velScrollY))
		self.capaEscenario.add(autonomeSprite('pirata_barco2_2.png',(ANCHO_PANTALLA/2,320,4000,0,0.005,0),(0.2,0.2,1,1,0,0),(0.17,0.07)))
		self.capaEscenario.add(autonomeSprite('pirata_barco2_2.png',(ANCHO_PANTALLA/1.75,320,4000,0,0.007,0),(0.25,0.25,1,1,0,0),(0.18,0.08)))
		self.capaEscenario.add(autonomeSprite('pirata_barco2_2.png',(ANCHO_PANTALLA/3,310,4000,0,0.01,0),(0.3,0.3,1,1,0,0),(0.19,0.09)))

		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(700,200,2000,0,0.002,-0.001),(0.15,0.15,0.25,0.25,0.000001,0.000001),(0.3,0.25)))
		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(100,50,3000,0,0.01,-0.005),(0.25,0.25,0.3,0.3,0.000005,0.000005),(0.33,-0.5)))
		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(1000,230,2000,0,0.002,-0.001),(0.18,0.18,0.25,0.25,0.000001,0.000001),(0.3,0.25)))

		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(1800,250,5500,0,0,0.002),(0.1,0.1,0.15,0.15,0.000001,0.000001),(0.2,0.2)))
		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(2200,130,5200,0,0,0.03),(0.27,0.27,0.4,0.4,0.000001,0.000001),(0.32,0.4)))
		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(2000,100,5000,0,0,0.04),(0.3,0.3,0.4,0.4,0.000001,0.000001),(0.33,-0.5)))
		
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
		self.jugador1.establecerPosicion((0, 555*ESCALA))

	def setEnemigos(self):
		### ENEMIGOS ###
		random.seed()
		n_enemigos = 3 + self.nivel * 2
		dist_enemigos = self.max_x/(n_enemigos+1)
		piratas = []

		for i in range(0,n_enemigos):
			#piratas.append((dist_enemigos*ESCALA*(i+1) + random.randint(-dist_enemigos/2, dist_enemigos/2), 500*ESCALA))
			piratas.append((dist_enemigos*(i+1) + random.randint(-100, 100), 500*ESCALA))

		for posicion in piratas:
			if random.randint(0,100) >= 100-5*self.nivel:
				pirata = Enemigo(EPIRATA3)
			elif random.randint(0,100) > 90-10*self.nivel:
				pirata = Enemigo(EPIRATA2)
			else:
				pirata = Enemigo(EPIRATA1)

			pirata.establecerPosicion(posicion)
			self.grupoEnemigos.add(pirata)

		self.final = Enemigo(EPIRATA4)
		self.final.establecerPosicion((7000*ESCALA, 400))
		self.grupoEnemigos.add(self.final)

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
		sound_bso = GestorRecursos.CargarSonido('pirata_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('pirata_ambient.ogg')
		pygame.mixer.stop();
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0)
		self.channel_ambient = sound_ambient.play(-1)