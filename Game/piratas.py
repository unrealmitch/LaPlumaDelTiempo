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

class Piratas(Escena):
	def __init__(self, director):

		Escena.__init__(self, director)

		#Atenuado
		self.fade = 250
		self.time_fade = pygame.time.get_ticks()

		### ESCENARIO ###
		if DEBUG:
			self.background = StaticScenario('pirata_fondo.png',(0.3,0))
		else:
			self.background = DynamicScenario("animations/pirata_fondo",21,0,(0.3,0))

		self.decorado = StaticScenario('pirata_escenario.png',(1,1))
		
		self.capaEscenario = Capa(self.background)
		
		# autonomeSprite(image, (startX, startY, maxX, maxY, velX, velY), (startScaleX, startScaleY, maxScaleX, maxScaley, velScaleX, velScaleY), (velScrollX, velScrollY))
		#self.capaEscenario.add(autonomeSprite('pirata_barco2.png',(1000,150,2000,0,0.01,0),(0.8,0.8,1,1,0,0),(0.3,0.25)))
		
		self.capaEscenario.add(autonomeSprite('pirata_barco2_2.png',(ANCHO_PANTALLA/2,280,4000,0,0.0001,0),(0.3,0.3,1,1,0,0),(0.1,0.1)))

		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(700,200,2000,0,0.002,0.001),(0.15,0.15,0.25,0.25,0.000001,0.000001),(0.3,0.25)))
		self.capaEscenario.add(autonomeSprite('pirata_barco1.png',(100,50,3000,0,0.01,-0.005),(0.25,0.25,0.5,0.5,0.000005,0.000005),(0.3,-0.5)))

		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5400,240,0,0,0,0),(0.7,0.7,0,0,0,0),(0.86,0.86)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5300,250,0,0,0,0),(0.75,0.75,0,0,0,0),(0.88,0.88)))
		self.capaEscenario.add(autonomeSprite('pirata_barco3.png',(5200,250,0,0,0,0),(0.8,0.8,0,0,0,0),(0.9,0.9)))

		# Que parte del decorado estamos visualizando
		self.scroll = (0,0.)
		self.virtual_scroll = (0.,0.)
		self.scroll_waves = 0.01

		### JUGADORES ###
		self.jugador1 = Jugador()
		self.jugador1.establecerPosicion((0, 555*ESCALA))
		self.grupoJugadores = pygame.sprite.Group( self.jugador1 )
		self.lifebar = LifeBar()

		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("pirata_plataform.txt")
		plataformas = []
		self.grupoPlataformas = pygame.sprite.Group()

		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], elem[1], elem[2], elem[3]),elem[4]))
		
		### ENEMIGOS ###
		enemigo1 = Pirata()
		enemigo1.establecerPosicion((1500*ESCALA, 555*ESCALA))
		enemigo2 = Pirata()
		enemigo2.establecerPosicion((2500*ESCALA, 555*ESCALA))
		enemigo3 = Pirata()
		enemigo3.establecerPosicion((3500*ESCALA, 500*ESCALA))
		enemigo4 = Pirata()
		enemigo4.establecerPosicion((5200*ESCALA, 720*ESCALA))

		# Creamos un grupo con los enemigos
		self.grupoEnemigos = pygame.sprite.Group( enemigo1, enemigo2, enemigo3, enemigo4 )

		
		self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)
		self.grupoSpritesDinamicos.add()

		self.grupoSprites = pygame.sprite.Group( self.jugador1 )
		self.grupoSprites.add(self.grupoEnemigos)
		self.grupoSprites.add(self.grupoPlataformas)

		### ANIMACIONES ###
		self.animacionOlas = []
		for i in range(int(ANCHO_PANTALLA/(400*ESCALA))):
			animacionOla = AnimacionOlas()
			pyganim.PygAnimation.scale(animacionOla, (int(510*ESCALA), int(390*ESCALA)))
			animacionOla.posicionx = 509*i*ESCALA
			animacionOla.posiciony = 420*ESCALA
			self.animacionOlas.append(animacionOla)
		
		for elem in self.animacionOlas:
			elem.play()

		### Sonido ###
		sound_bso = GestorRecursos.CargarSonido('pirata_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('pirata_ambient.ogg')
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0)
		self.channel_ambient = sound_ambient.play(-1)

	def salir(self,complete):
		pygame.mixer.stop();
		#if(complete):
		self.director.salirEscena();

	def actualizarScrollOrdenados(self, jugador):
		if (jugador.rect.left<MINIMO_X_JUGADOR):
			desplazamiento = (MINIMO_X_JUGADOR - jugador.rect.left)

			if self.scroll[0] <= 0:
				self.scroll = (0, self.scroll[1])
				jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] - desplazamiento, self.scroll[1])
				return True;

		if (jugador.rect.right >MAXIMO_X_JUGADOR):
			desplazamiento = (jugador.rect.right - MAXIMO_X_JUGADOR)

			if (self.scroll[0]*ESCALA + ANCHO_PANTALLA) >= self.decorado.rect.right:
				if self.fade == 0: self.fade = -250
				if self.jugador1.rect.centerx > ANCHO_PANTALLA + 100: self.salir(True)
				self.channel_bso.set_volume(float(self.fade)/-250.0)
				#self.scroll = (self.decorado.rect.right*ESCALA - ANCHO_PANTALLA, self.scroll[1])
				#jugador.establecerPosicion((self.scroll[0]*ESCALA + MAXIMO_X_JUGADOR*ESCALA, jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] + desplazamiento, self.scroll[1]);
				return True;

		return False;


	def actualizarScroll(self, jugador):

		if (self.scroll[1] > 1 or self.scroll[1] < 0):
			self.scroll_waves = -self.scroll_waves

		self.scroll = (self.scroll[0], self.scroll[1] + self.scroll_waves)
		self.virtual_scroll = (int(self.scroll[0]), int(math.sin(self.scroll[1]) * 30))

		cambioScroll = self.actualizarScrollOrdenados(jugador)

		self.decorado.establecerPosicionPantalla(self.virtual_scroll)
		self.background.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(self.virtual_scroll)

		self.capaEscenario.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(self.virtual_scroll)

		if(self.fade == 0):
			sound_lvl = float(self.scroll[0])/float(self.background.rect.width)/2
			self.channel_bso.set_volume(sound_lvl)

	def update(self, tiempo):

		self.capaEscenario.update(tiempo)
		self.decorado.update(tiempo)
		# Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
		for enemigo in iter(self.grupoEnemigos):
			enemigo.mover_cpu(self.jugador1)
		
		self.grupoSpritesDinamicos.update(self.grupoPlataformas,tiempo)

		#Miramos todas las colision de los enemios con los jugadores, si uno de ellos está atacando, daña al otro
		collitions = pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)
		for player,enemys in collitions.items():
			for enemy in enemys:
				if enemy.posturas[P_ATACANDO1] == True: 
					player.actualizarVida()
					vida = self.jugador1.actualizarVida()
					self.lifebar.actualizarVida(vida)
				if player.posturas[P_ATACANDO1] == True : enemy.actualizarVida() 
			
		
		self.actualizarScroll(self.jugador1)
		self.background.establecerPosicionPantalla(self.virtual_scroll)

		if (self.jugador1.rect.bottom > ALTO_PANTALLA): self.salir(True)

		
	def dibujar(self, pantalla):
		pantalla.fill((0,0,0))

		self.capaEscenario.draw(pantalla)
		self.decorado.draw(pantalla)
		# Luego los Sprites
		self.grupoSprites.draw(pantalla)

		if(self.jugador1.alive()):
			self.jugador1.draw(pantalla)
		else:
			if(self.fade == 0):
				self.fade = -250
			elif(self.fade >= -1):
				self.salir(False)
		#screen.blit(self.lifebar.image, self.lifebar.rect)
		self.lifebar.draw(pantalla)
		
		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)

		for animacion in self.animacionOlas:
			animacion.dibujar(pantalla)

		#Efecto fundido, para entrar a la escena, y para terminarla
		if(self.fade != 0):
			time = pygame.time.get_ticks()
			if(time > self.time_fade + 1):
				self.time_fade = time

				s = pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
				s.fill((0,0,0))

				if(self.fade>0):
					self.fade-=10
					s.set_alpha(self.fade)
					pantalla.blit(s, (0,0))
				else:
					if(self.fade < -10):
						self.fade+=8
					else:
						self.fade=-1
					s.set_alpha(255+self.fade)
					pantalla.blit(s, (0,0))
					#pygame.draw.rect(pantalla,(255,255,255, ), (0,0,ANCHO_PANTALLA,ALTO_PANTALLA))

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.director.salirPrograma()
				if evento.key == K_F1:
					pygame.display.toggle_fullscreen()
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		if(self.fade == 0):
			teclasPulsadas = pygame.key.get_pressed()
			teclasConfig = {ARRIBA: K_UP, ABAJO: K_DOWN, IZQUIERDA: K_LEFT, DERECHA: K_RIGHT, ATAQUE1: K_SPACE}
			self.jugador1.mover(teclasPulsadas, teclasConfig)
		else:
			if(self.fade < 0):
				self.jugador1.avanzar()
