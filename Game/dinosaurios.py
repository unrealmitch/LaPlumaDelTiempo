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


# Clase Dinosaurios
class Dinosaurios(Fase):
	def __init__(self, director):

		Fase.__init__(self, director, 'DINOS_LVL')

	def setEscenario(self):
		### ESCENARIO ###
		if DEBUG:
			background = StaticScenario('dino_fondo.png',(0.3,0))
		else:
			background = DynamicScenario("animations/dino_fondo",21,0,(0.3,0))
		
		background2 = StaticScenario('dino_fondo2.png',(0.6,0))

		self.capaEscenario.add(background)
		self.decorado = StaticScenario('dino_escenario.png',(1,0))
		

		self.capaEscenario.add(autonomeSprite('dino2.png',(ANCHO_PANTALLA/1.2,10,5000,0,0,0),(1.2,1.2,1,1,0,0),(0.1,-0.2)))
		for i in range(10):
			random.seed()
			self.capaEscenario.add(autonomeSprite('dino_ave.png',(random.randint(400,7000),random.randint(10,300),7000,0,-float(random.randint(1,100))/1000.,0),(0.5,0.5,1,1,0,0),(float(random.randint(10,100))/100.,float(random.randint(-200,200))/100.)))

		self.capaEscenario.add(background2)
		self.capaEscenario.add(autonomeSprite('dino1.png',(0,320*ESCALA,5000,0,0.01,0),(1.5,1.5,1,1,0,0),(0.3,1)))

		decorado = StaticScenario('dino_escenario.png',(1,0.1))
		self.capaEscenario.add(decorado)
		self.max_x = decorado.rect.right

	def setPlataformas(self):
		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("dino_plataform.txt")
		plataformas = []
		
		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], elem[1]+295, elem[2], elem[3]),elem[4]))


	def setJugador(self):
		self.jugador1 = Jugador(PLAYER_DINO)
		self.jugador1.establecerPosicion((0, 300*ESCALA))

	def setEnemigos(self):
		random.seed()

		n_enemigos = 3 + self.nivel*2
		dist_enemigos = self.max_x/(n_enemigos+1)
		dinos = []

		for i in range(0,n_enemigos):
			#piratas.append((dist_enemigos*ESCALA*(i+1) + random.randint(-dist_enemigos/2, dist_enemigos/2), 500*ESCALA))
			dinos.append((dist_enemigos*(i+1) + random.randint(-50, 50), 500*ESCALA))

		for posicion in dinos:
			if random.randint(0,100) >= 100-5*self.nivel:
				dino = Enemigo(EDINO1)
			elif random.randint(0,100) > 90-10*self.nivel:
				dino = Enemigo(EDINO1)
			else:
				dino = Enemigo(EDINO1)

			dino.establecerPosicion(posicion)
			self.grupoEnemigos.add(dino)

		self.final = Enemigo(EPIRATA4)
		self.final.establecerPosicion((5100*ESCALA, 400))
		self.grupoEnemigos.add(self.final)


	def setAnim(self):
		for i in range(int(ANCHO_PANTALLA/(400*ESCALA))):
			animacionLava = AnimacionLava()
			pyganim.PygAnimation.scale(animacionLava, (int(512*ESCALA), int(256*ESCALA)))
			animacionLava.posicionx = 512*i*ESCALA
			animacionLava.posiciony = 600*ESCALA
			self.animacion.append(animacionLava)
		
		for elem in self.animacion:
			elem.play()

	def setAudio(self):
		sound_bso = GestorRecursos.CargarSonido('dino_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('dino_ambient.ogg')
		pygame.mixer.stop();
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0)
		self.channel_ambient = sound_ambient.play(-1)
				
	def dibujar_forntal(self, pantalla):
		for animacion in self.animacion:
			animacion.posiciony = 600*ESCALA + int(math.sin(self.scroll[1]) * 20)
			animacion.dibujar(pantalla)

	def actualizarScroll(self, jugador):
		if (self.scroll[1] > 1 or self.scroll[1] < 0):
			self.scrolly_speed = -self.scrolly_speed

		self.scroll = (self.scroll[0], self.scroll[1] + self.scrolly_speed)
		self.virtual_scroll = (int(self.scroll[0]), int(math.sin(self.scroll[1]) * self.scrolly_amplitude))

		cambioScroll = self.actualizarScrollOrdenados(jugador)

		self.capaEscenario.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla((self.virtual_scroll[0], 0))

		if(self.fade == 0):
			sound_lvl = float(self.scroll[0])/float(self.max_x)
			self.channel_bso.set_volume(sound_lvl)

