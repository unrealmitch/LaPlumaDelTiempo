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
# Clase Piratas

class Piratas_Arcade(EscenaPygame):
	def __init__(self, director):

		EscenaPygame.__init__(self, director)

		#Cargamos la configuracion
		self.teclasConfig = {ARRIBA: GestorRecursos.getConfigParam('ARRIBA'), ABAJO: GestorRecursos.getConfigParam('ABAJO'), 
		IZQUIERDA: GestorRecursos.getConfigParam('IZQUIERDA'), DERECHA: GestorRecursos.getConfigParam('DERECHA'), 
		ATAQUE1: GestorRecursos.getConfigParam('ATAQUE1')}

		self.nivel = 0
		self.nivel_max = GestorRecursos.getConfigParam('PIRATAS_ARCADE')

		#Atenuado
		self.fade = 250
		self.time_fade = pygame.time.get_ticks()
		self.clock_start = pygame.time.get_ticks()

		### ESCENARIO ###
		if DEBUG:
			self.background = StaticScenario('pirata_fondo.png',(0.3,0))
		else:
			self.background = DynamicScenario("animations/pirata_fondo",21,0,(0.3,0))

		self.decorado = StaticScenario('pirata_escenario.png',(1,1))
		self.capaEscenario = Capa(self.background)
	
		###SCROLL### Que parte del decorado estamos visualizando
		self.scroll = (1100*ESCALA,0.)
		self.virtual_scroll = (0.,0.)
		self.scroll_waves = 0.01

		### JUGADORES ###
		self.jugador1 = Jugador(PLAYER_PIRATA)
		self.jugador1.establecerPosicion((1820*ESCALA, 400*ESCALA))
		self.grupoJugadores = pygame.sprite.Group( self.jugador1 )
		self.lifebar = LifeBar()

		### ENEMIGOS ###
		self.grupoEnemigos = pygame.sprite.Group()
		self.lastEnemy = 0
		self.nextEnemy = 0

		### PLATAFORMAS ###
		file_plataformas = GestorRecursos.CargarMapaPlataformas("pirata_plataform.txt")
		plataformas = []
		self.grupoPlataformas = pygame.sprite.Group()

		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], elem[1], elem[2], elem[3]),elem[4]))

		#Grupos cojnutos de sprites
		self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)

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
		sound_bso = GestorRecursos.CargarSonido('arcade_bso.ogg')
		sound_ambient = GestorRecursos.CargarSonido('pirata_ambient.ogg')
		pygame.mixer.stop();
		self.channel_bso = sound_bso.play(-1)
		self.channel_bso.set_volume(0.5)
		self.channel_ambient = sound_ambient.play(-1)

	def salir(self):
		pygame.time.delay(3000)	#Retardo para terminar el audio
		pygame.mixer.stop();
		self.director.salirEscena();

	def addEnemy(self):
		if pygame.time.get_ticks() > self.nextEnemy:
			random.seed()

			dificultad = (self.nivel / 10) + 1

			nextTime = 10000/dificultad
			nextTime = random.randint(nextTime, nextTime*2)
			if nextTime < 200: nextTime = 200
			self.nextEnemy = pygame.time.get_ticks() + nextTime

			if random.randint(0,100) >= 101-1*dificultad:
				pirata = Enemigo(EPIRATA3, True)
			if random.randint(0,100) >= 100-5*dificultad:
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
		self.background.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(self.virtual_scroll)

		self.capaEscenario.establecerPosicionPantalla(self.virtual_scroll)

	def update(self, tiempo):
		#Contador de tiempo
		self.nivel = (pygame.time.get_ticks() - self.clock_start) / 1000

		self.addEnemy()
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
		self.background.establecerPosicionPantalla(self.virtual_scroll)

		#Cuando hacemos el fundido a negro (Salímos)

		if(not self.jugador1.alive()):
			if(self.fade == 0): 
				self.fade = -250
				GestorRecursos.CargarSonido('game_over.ogg').play()
				GestorRecursos.setConfigParam('PIRATAS_ARCADE', self.nivel + 1)

		if(self.fade < 0):
			self.channel_bso.set_volume(-self.fade/300)
			self.channel_ambient.set_volume(-self.fade/300)

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
		self.jugador1.draw(pantalla)

		'''
		# Vida enemigos
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

		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)

		for animacion in self.animacionOlas:
			animacion.dibujar(pantalla)

		##GUI
		self.lifebar.draw(pantalla)

		#Tiempo
		tiempo = self.nivel
		tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 18)
		texto = tipoLetra.render("Time: " + str(tiempo), True, (255,0,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 50)
		
		pantalla.blit(texto, rect)
		texto = tipoLetra.render("Goal: " + str(self.nivel_max), True, (255,0,0))
		rect = texto.get_rect()
		rect.center = (ANCHO_PANTALLA/2, 75)
		pantalla.blit(texto, rect)

		#Efecto fundido, para entrar a la escena, y para terminarla
		if(self.fade != 0):
			time = pygame.time.get_ticks()
			if(time > self.time_fade + 1):
				self.time_fade = time
				black = pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
				black.fill((0,0,0))

				if(self.fade>0):
					self.fade-=10
					black.set_alpha(self.fade)
					pantalla.blit(black, (0,0))
					self.clock_start = pygame.time.get_ticks()

				else:	#Cuando se hace el fundido a negro por si pasamos la mision o morimos
					if(self.fade < -10):
						self.fade+=8
					else:
						self.fade=-1

					if(self.jugador1.alive()):
						image = GestorRecursos.CargarImagen("complete.png",-1)
					else:
						image = GestorRecursos.CargarImagen("game_over.png",-1)

					rect = image.get_rect()
					rect.centerx = ANCHO_PANTALLA/2
					rect.centery = ALTO_PANTALLA/2

					image.set_alpha(300+self.fade)
					black.set_alpha(300+self.fade)

					pantalla.blit(black, (0,0))
					pantalla.blit(image,rect)
					#pygame.draw.rect(pantalla,(255,255,255, ), (0,0,ANCHO_PANTALLA,ALTO_PANTALLA))

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.jugador1.vida = 0;
					self.jugador1.kill()
					self.fade = -200;
				if evento.key == K_F11:
					pygame.display.toggle_fullscreen()
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		if(self.fade == 0):
			teclasPulsadas = pygame.key.get_pressed()
			self.jugador1.mover(teclasPulsadas, self.teclasConfig)

