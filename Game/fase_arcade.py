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
from fase import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
DEBUG = True
MINIMO_X_JUGADOR = (ANCHO_PANTALLA  / 3)
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Piratas

class Fase_arcade(Fase):
	def __init__(self, director, nivel):

		Fase.__init__(self, director, nivel)

		#Cargamos la configuracion
		self.teclasConfig = {ARRIBA: GestorRecursos.getConfigParam('ARRIBA'), ABAJO: GestorRecursos.getConfigParam('ABAJO'), 
		IZQUIERDA: GestorRecursos.getConfigParam('IZQUIERDA'), DERECHA: GestorRecursos.getConfigParam('DERECHA'), 
		ATAQUE1: GestorRecursos.getConfigParam('ATAQUE1')}

		#Variabables control tiempo de la fase
		self.time = 0
		self.clock_start = pygame.time.get_ticks()
		self.nextEnemy = 0

	###FUNCIONES CONFIGURACION FASE###
	def setEscenario(self):
		raise "Fase not implemented yet"

	def setPlataformas(self):
		raise "Fase not implemented yet"

	def setJugador(self):
		raise "Fase not implemented yet"

	def setEnemigos(self):
		raise "Fase not implemented yet"

	def setAnim(self):
		raise "Fase not implemented yet"

	def setAudio(self):
		raise "Fase not implemented yet"

	def refreshSprites(self):
		self.grupoJugadores.add(self.jugador1)
		self.grupoSpritesDinamicos.add(self.grupoJugadores)
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)

		self.grupoSprites.add(self.grupoSpritesDinamicos)
		self.grupoSprites.add(self.grupoEnemigos)
		self.grupoSprites.add(self.grupoPlataformas)

	## FUNCIONES ARCADE ##
	def addEnemy(self):
		if pygame.time.get_ticks() > self.nextEnemy:
			random.seed()

			dificultad = (self.time / 10) + 1

			nextTime = 10000/dificultad
			nextTime = random.randint(nextTime, nextTime*2)
			if nextTime < 500: nextTime = 500
			self.nextEnemy = pygame.time.get_ticks() + nextTime

			if random.randint(0,100) > 101-1*dificultad:
				pirata = Enemigo(EPIRATA4, True)
			elif random.randint(0,100) > 100-5*dificultad:
				pirata = Enemigo(EPIRATA3, True)
			elif random.randint(0,100) >= 80-10*dificultad:
				pirata = Enemigo(EPIRATA2, True)
			else:
				pirata = Enemigo(EPIRATA1, True)

			distancia = (300*ESCALA + random.randint(0,1000)) * random.choice([1,-1])
			pirata.establecerPosicion( (distancia+self.jugador1.posicion[0] , random.randint(0,400)*ESCALA))
			#pirata.establecerPosicion( (self.jugador1.posicion[0] , 50) )
			self.grupoEnemigos.add(pirata)
			self.grupoSpritesDinamicos.add(self.grupoEnemigos)
			self.grupoSprites.add(self.grupoEnemigos)

			return True
		else:
			return False

	###FUNCIONES DE ACCION###
	def check_end(self):
		#Cuando hacemos el fundido a negro (Salímos) [Si morimos o muere el jefe final]
		if(not self.jugador1.alive()):
			if(self.fade == 0): 
				self.fade = -250
				if self.time > self.nivel:
					GestorRecursos.CargarSonido('mision_complete_long.ogg').play()
					GestorRecursos.setConfigParam(self.clave_nivel, self.time)
				else:
					GestorRecursos.CargarSonido('game_over.ogg').play()
				

		if(self.fade < 0):
			self.channel_bso.set_volume(-self.fade/300)
			self.channel_ambient.set_volume(-self.fade/300)
				
			if(self.fade>-10):
				self.salir()

	def update(self, tiempo):
		if(self.fade == 0):
			self.time = (pygame.time.get_ticks() - self.clock_start) / 1000
			self.addEnemy()
		Fase.update(self, tiempo)

	def dibujar(self, pantalla):
		Fase.dibujar(self,pantalla)

		###Tiempo GUI###
		tiempo = self.time
		tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 18)
		texto = tipoLetra.render("Time: " + str(self.time), True, (255,0,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 50)
		
		pantalla.blit(texto, rect)
		texto = tipoLetra.render("Goal: " + str(self.nivel), True, (255,100,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 75)
		pantalla.blit(texto, rect)

