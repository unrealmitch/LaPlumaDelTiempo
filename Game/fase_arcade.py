# -*- coding: utf-8 -*-

import random,math
import pygame, escena

from escena import *
from personajes import *
from escenario import *
from capa import *
from gui import *
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

		self.max_round = GestorRecursos.getConfigParam(self.clave_nivel+'_round')
		self.max_score = GestorRecursos.getConfigParam(self.clave_nivel+'_score')

		#Variabables control tiempo de la fase
		self.time = 0								#Tiempo alcanzado en modo arcade
		self.clock_start = pygame.time.get_ticks()	#Inicio del modo arcade
		self.nextEnemy = 0							#Cuando se crea un nuevo enemigo
		self.nextObject = pygame.time.get_ticks() + 3000	#Cuando se crea un nuevo objeto
		self.level = 1								#Nivel de dificultad de la fase
		self.round = 5								#Cuanto durará la fase actual

		self.gui = Gui(5,1)							#UTILIZAMOS UNA GUI DIFERENTE!
		self.gui.actualizarPsj(self.jugador1)


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

			dificultad = self.level

			nextTime = 15000/dificultad
			nextTime = random.randint(nextTime, nextTime*2)
			if nextTime < 750: nextTime = 750
			self.nextEnemy = pygame.time.get_ticks() + nextTime

			if random.randint(0,100) > 108-1*dificultad:
				pirata = Enemigo(EPIRATA5, True)
			elif random.randint(0,100) > 105-2*dificultad:
				pirata = Enemigo(EPIRATA4, True)
			elif random.randint(0,100) > 100-4*dificultad:
				pirata = Enemigo(EPIRATA3, True)
			elif random.randint(0,100) >= 70-8*dificultad:
				pirata = Enemigo(EPIRATA2, True)
			else:
				pirata = Enemigo(EPIRATA1, True)

			distancia = (300*ESCALA + random.randint(0,500+dificultad*100)) * random.choice([1,-1])
			pirata.establecerPosicion( (distancia+self.jugador1.posicion[0] , random.randint(0,400)*ESCALA))
			#pirata.establecerPosicion( (self.jugador1.posicion[0] , 50) )
			self.grupoEnemigos.add(pirata)
			self.grupoSpritesDinamicos.add(self.grupoEnemigos)
			self.grupoSprites.add(self.grupoEnemigos)

			return True
		else:
			return False

	def addObjects(self):
		if pygame.time.get_ticks() > self.nextObject:
			random.seed()

			dificultad = self.level

			nextTime = 15000/dificultad
			nextTime = random.randint(nextTime, nextTime*4)
			if nextTime < 1500: nextTime = 1500
			self.nextObject = pygame.time.get_ticks() + nextTime


			distancia = random.randint(0,self.max_x)
			objetos = [CORAZON]

			randomitem = random.randint(0,100)

			if randomitem > 30:
				tobjeto = CORAZON
			elif randomitem > 7:
				tobjeto = random.choice([RON,BOTAS,MUELLE])
			else:
				tobjeto = random.choice([RON,ESPADA])

			if tobjeto == CORAZON:
				objeto = Objeto(CORAZON, 'arcade_hearth_little.png', 'arcade_life.ogg')
			elif tobjeto == RON:
				objeto = Objeto(RON, 'arcade_ron.png', 'arcade_eructo.ogg')
			elif tobjeto == ESPADA:
				objeto = Objeto(ESPADA, 'arcade_espada.png', 'arcade_powerup.ogg')
			elif tobjeto == BOTAS:
				objeto = Objeto(BOTAS, 'arcade_botas.png', 'arcade_powerup.ogg')
			elif tobjeto == MUELLE:
				objeto = Objeto(MUELLE, 'arcade_up.png', 'arcade_powerup.ogg')

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
					GestorRecursos.setConfigParam(self.clave_nivel, self.time)
					GestorRecursos.CargarSonido('mision_complete_long.ogg').play()
				else:
					GestorRecursos.CargarSonido('game_over.ogg').play()

				if self.level > self.max_round: GestorRecursos.setConfigParam(self.clave_nivel+'_round', self.level)
				if self.score > self.max_score: GestorRecursos.setConfigParam(self.clave_nivel+'_score', self.score)
				

		if(self.fade < 0):
			self.channel_bso.set_volume(-self.fade/300)
			self.channel_ambient.set_volume(-self.fade/300)
				
			if(self.fade>-10):
				self.salir()

	def update(self, tiempo):
		#Añadimos la lógica del modo arcade [Dificultad por nivel, añadir aleatoriamente enemigos y objetos]
		if(self.fade == 0):
			self.time = (pygame.time.get_ticks() - self.clock_start) / 1000
			self.addEnemy()
			self.addObjects()
			if  self.time >= self.round:	#Alcanzado proximo nivel
				GestorRecursos.CargarSonido('arcade_nextlvl.ogg').play()
				self.level += 1
				self.round = self.time + 5 + self.level*2

				if self.level % 2 == 1:	#Cada 2 fases lanzamos un corazon sobre el psj
					objeto = Objeto(CORAZON, 'arcade_hearth_little.png', 'arcade_life.ogg')
					objeto.establecerPosicion( (self.jugador1.posicion[0] , 50) )
					self.grupoObjetos.add(objeto)
					self.grupoSpritesDinamicos.add(self.grupoObjetos)
					self.grupoSprites.add(self.grupoObjetos)
				#self.round = self.time + self.level*5 Mu Largo

		Fase.update(self, tiempo)
		self.channel_bso.set_volume(float(self.time)/200.)		
		

	def dibujar(self, pantalla):
		Fase.dibujar(self,pantalla)

		###Tiempo GUI###
		tiempo = self.time
		tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 24)
		texto = tipoLetra.render("Time: " + str(self.time), True, (255,0,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 50)
		pantalla.blit(texto, rect)

		texto = tipoLetra.render("Goal: " + str(self.nivel), True, (255,100,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 75)
		pantalla.blit(texto, rect)

		###Puntuacion###
		tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 18)

		texto = tipoLetra.render("Score: " + str(self.score), True, (100,255,0))
		pantalla.blit(texto, (ANCHO_PANTALLA/1.2, 25))

		texto = tipoLetra.render("Round: " + str(self.level), True, (100,255,0))
		pantalla.blit(texto, (ANCHO_PANTALLA/1.2, 50))

		texto = tipoLetra.render("Max S.: " + str(self.max_score ), True, (255,20,255))
		pantalla.blit(texto, (ANCHO_PANTALLA/1.2, 100))

		texto = tipoLetra.render("Max R.: " + str(self.max_round ), True, (255,0,255))
		pantalla.blit(texto, (ANCHO_PANTALLA/1.2, 125))



