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

# Clase Fase_Arcade

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
		self.nextHearth = 0
		self.playerDrunk = False

		self.lifebar = LifeBar(5,1)


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

	def addObjects(self):
		if pygame.time.get_ticks() > self.nextHearth:
			random.seed()

			dificultad = (self.time / 15) + 1

			nextTime = 15000/dificultad
			nextTime = random.randint(nextTime, nextTime*3)
			if nextTime < 1000: nextTime = 1000
			self.nextHearth = pygame.time.get_ticks() + nextTime


			distancia = random.randint(0,self.max_x)
			objetos = [CORAZON]

			randomitem = random.randint(0,100)

			if randomitem > 30:
				tobjeto = CORAZON
			else:
				tobjeto = RON

			if tobjeto == CORAZON:
				objeto = Objeto(CORAZON, 'arcade_hearth_little.png', 'arcade_life.ogg')
			elif tobjeto == RON:
				objeto = Objeto(RON, 'arcade_ron.png', 'arcade_eructo.ogg')

			objeto.establecerPosicion( (distancia, random.randint(0,200)*ESCALA))
			#objeto.establecerPosicion( (self.jugador1.posicion[0] , 50) )
			self.grupoObjetos.add(objeto)
			self.grupoSpritesDinamicos.add(self.grupoObjetos)
			self.grupoSprites.add(self.grupoObjetos)

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
			self.addObjects()
		Fase.update(self, tiempo)

		objetos = pygame.sprite.spritecollide(self.jugador1, self.grupoObjetos, False)
		for objeto in objetos:
			GestorRecursos.CargarSonido(objeto.sound_pick).play()
			objeto.kill()
			if objeto.tipo == CORAZON:
				vida = self.jugador1.addVida()
				self.lifebar.actualizarVida(vida)
			elif objeto.tipo == RON:
				tmp = self.teclasConfig[IZQUIERDA]
				self.teclasConfig[IZQUIERDA] = self.teclasConfig[DERECHA]
				self.teclasConfig[DERECHA] = tmp
				if self.playerDrunk:
					self.playerDrunk = False
					self.jugador1.hoja = GestorRecursos.CargarImagen("pirata_Player.png",-1)
				else:
					self.playerDrunk = True
					self.jugador1.hoja = GestorRecursos.CargarImagen("pirata_Player_drunk.png",-1)

				

		self.channel_bso.set_volume(0.1 + (self.time/100.))

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

