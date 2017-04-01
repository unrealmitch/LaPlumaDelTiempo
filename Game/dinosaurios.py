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
DEBUG = False
MINIMO_X_JUGADOR = (ANCHO_PANTALLA  / 3)
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Dinosaurios

class Dinosaurios(Escena):
	def __init__(self, director):

		Escena.__init__(self, director)

		#Atenuado
		self.fade = 250
		self.time_fade = pygame.time.get_ticks()

		### ESCENARIO ###
		### ESCENARIO ###
		if DEBUG:
			self.background = StaticScenario('dino_fondo.png',(0.3,0))
		else:
			self.background = DynamicScenario("animations/dino_fondo",21,0,(0.3,0))
		

		self.background2 = StaticScenario('dino_fondo2.png',(0.6,0))
		self.decorado = StaticScenario('dino_escenario.png',(1,0))
		
		self.capaEscenario = Capa(self.background)
		self.capaEscenario.add(self.background2)

		
		# Que parte del decorado estamos visualizando
		self.scroll = (0,0.)
		self.virtual_scroll = (0.,0.)
		self.scroll_waves = 0.01

		### JUGADORES ###
		self.jugador1 = Jugador(PLAYER_DINO)
		self.jugador1.establecerPosicion((0, 300*ESCALA))
		self.grupoJugadores = pygame.sprite.Group( self.jugador1 )
		self.lifebar = LifeBar()

		### ENEMIGOS ###
		random.seed()
		self.grupoEnemigos = pygame.sprite.Group()

		n_enemigos=5
		dist_enemigos = self.decorado.rect.width/(n_enemigos+1)
		dinos = []

		for i in range(0,n_enemigos):
			#piratas.append((dist_enemigos*ESCALA*(i+1) + random.randint(-dist_enemigos/2, dist_enemigos/2), 500*ESCALA))
			dinos.append((dist_enemigos*(i+1) + random.randint(-50, 50), 500*ESCALA))

		for posicion in dinos:
			if random.randint(0,100) > 90:
				dino = Enemigo(10)
			elif random.randint(0,100) > 60:
				dino = Enemigo(10)
			else:
				dino = Enemigo(10)

			dino.establecerPosicion(posicion)
			self.grupoEnemigos.add(dino)

		self.final = Enemigo(EPIRATA4)
		self.final.establecerPosicion((5100*ESCALA, 400))
		self.grupoEnemigos.add(self.final)
		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("dino_plataform.txt")
		plataformas = []
		self.grupoPlataformas = pygame.sprite.Group()

		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], elem[1]+295, elem[2], elem[3]),elem[4]))

		#Grupos cojnutos de sprites
		self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)

		self.grupoSprites = pygame.sprite.Group( self.jugador1 )
		self.grupoSprites.add(self.grupoEnemigos)
		self.grupoSprites.add(self.grupoPlataformas)

		### ANIMACIONES ###
		self.animacionLava = []
		for i in range(int(ANCHO_PANTALLA/(400*ESCALA))):
			animacionLava = AnimacionLava()
			pyganim.PygAnimation.scale(animacionLava, (int(512*ESCALA), int(256*ESCALA)))
			animacionLava.posicionx = 512*i*ESCALA
			animacionLava.posiciony = 600*ESCALA
			self.animacionLava.append(animacionLava)
		
		for elem in self.animacionLava:
			elem.play()

		### Sonido ###
		sound_bso = GestorRecursos.CargarSonido('dino_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('dino_ambient.ogg')
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0)
		self.channel_ambient = sound_ambient.play(-1)

	def salir(self):
		pygame.mixer.stop();
		self.director.salirEscena();

	def actualizarScrollOrdenados(self, jugador):
		if (jugador.rect.left<MINIMO_X_JUGADOR):
			desplazamiento = (MINIMO_X_JUGADOR - jugador.rect.left)

			if self.scroll[0] <= 0:
				self.scroll = (0, self.scroll[1])
				if jugador.rect.left < 0: jugador.establecerPosicion((0 , jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] - desplazamiento, self.scroll[1])
				return True;

		if (jugador.rect.right > MAXIMO_X_JUGADOR):
			desplazamiento = (jugador.rect.right - MAXIMO_X_JUGADOR)

			if self.scroll[0]*ESCALA + ANCHO_PANTALLA + 10 >= self.decorado.rect.right:
				#if self.fade == 0: self.fade = -250
				#if self.jugador1.rect.centerx > ANCHO_PANTALLA + 100: self.salir(True)
				if self.fade == 0:
					if jugador.posicion[0] > self.decorado.rect.right-jugador.rect.width:
						jugador.establecerPosicion((self.decorado.rect.right-jugador.rect.width, jugador.posicion[1]))

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
		self.background2.establecerPosicionPantalla(self.virtual_scroll)
		self.background.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla((self.virtual_scroll[0], 0))

		self.capaEscenario.establecerPosicionPantalla(self.virtual_scroll)

		if(self.fade == 0):
			sound_lvl = float(self.jugador1.posicion[0])/float(self.background.rect.width)
			self.channel_bso.set_volume(sound_lvl)

	def update(self, tiempo):

		self.capaEscenario.update(tiempo)
		self.decorado.update(tiempo)
		# Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
		for enemigo in iter(self.grupoEnemigos):
			enemigo.mover_cpu(self.jugador1, self.grupoPlataformas)
		
		self.grupoSpritesDinamicos.update(self.grupoPlataformas,tiempo)

		#Miramos todas las colision de los enemios con los jugadores, si uno de ellos está atacando, daña al otro
		collitions = pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)
		for player,enemys in collitions.items():
			for enemy in enemys:
				if (enemy.posturas[P_ATACANDO1] and player.posturas[P_ATACANDO1]):
					self.jugador1.quitarVida(0)
					enemy.quitarVida(0)
				else:
					if enemy.posturas[P_ATACANDO1]: 
						vida = self.jugador1.quitarVida(1)
						self.lifebar.actualizarVida(vida)
					if player.posturas[P_ATACANDO1]: enemy.quitarVida(1)
			
		
		self.actualizarScroll(self.jugador1)

		#Cuando hacemos el fundido a negro

		if(not self.jugador1.alive()):
			if(self.fade == 0): self.fade = -250

		if ( not self.final.alive() ):
			if self.fade == 0: self.fade = -250

		if(self.fade < 0):
			self.channel_bso.set_volume(self.channel_bso.get_volume()-0.01)
			if(self.jugador1.alive()):
				self.jugador1.avanzar(self.grupoPlataformas)

			if(self.fade>-10):
				self.salir()
				
	def dibujar(self, pantalla):
		pantalla.fill((0,0,0))

		self.capaEscenario.draw(pantalla)
		self.decorado.draw(pantalla)
		# Luego los Sprites
		self.grupoSprites.draw(pantalla)

		# Vida enemigos


		self.jugador1.draw(pantalla)

		'''
		corazon_img = GestorRecursos.CargarImagen("corazon.png")
		corazon_rect = corazon_img.get_rect()
		for enemigo in self.grupoEnemigos:
			for i in range(enemigo.vida):
				corazon_rect.top = enemigo.rect.top + corazon_rect.height
				corazon_rect.left = i*(corazon_rect.width*2)
				pantalla.blit(corazon_img, corazon_rect)
		'''

		if(self.jugador1.alive()):
			self.jugador1.draw(pantalla)
		else:
			if(self.fade == 0): self.fade = -250

		#screen.blit(self.lifebar.image, self.lifebar.rect)
		self.lifebar.draw(pantalla)
		
		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)

		for animacion in self.animacionLava:
			animacion.posiciony = 600*ESCALA + self.virtual_scroll[1]
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

