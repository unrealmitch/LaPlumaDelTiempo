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
DEBUG = False
MINIMO_X_JUGADOR = (ANCHO_PANTALLA  / 3)
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Piratas

class Fase(EscenaPygame):
	def __init__(self, director, nivel):

		EscenaPygame.__init__(self, director)

		#Cargamos la configuracion
		self.teclasConfig = {ARRIBA: GestorRecursos.getConfigParam('ARRIBA'), ABAJO: GestorRecursos.getConfigParam('ABAJO'), 
		IZQUIERDA: GestorRecursos.getConfigParam('IZQUIERDA'), DERECHA: GestorRecursos.getConfigParam('DERECHA'), 
		ATAQUE1: GestorRecursos.getConfigParam('ATAQUE1')}

		self.clave_nivel = nivel
		self.nivel = GestorRecursos.getConfigParam(self.clave_nivel)

		#Intercambiamos teclas apra aumentar dificultad
		if self.nivel > 3:
			tmp = self.teclasConfig[IZQUIERDA]
			self.teclasConfig[IZQUIERDA] = self.teclasConfig[DERECHA]
			self.teclasConfig[DERECHA] = tmp
			if self.nivel > 5:
				tmp = self.teclasConfig[ARRIBA]
				self.teclasConfig[ARRIBA] = self.teclasConfig[ATAQUE1]
				self.teclasConfig[ATAQUE1] = tmp

		##Escenario [Máxima distancia x]
		self.max_x = 0
		
		#Atenuado [Valor reutilizado para terminar la fase]
		self.fade = 250
		self.time_fade = pygame.time.get_ticks()
		#Atenuado Vida
		self.hurt = 0

		###SCROLL### Que parte del decorado estamos visualizando
		self.scroll = (0,0.)
		self.virtual_scroll = (0.,0.)
		self.scrolly_speed = 0.03
		self.scrolly_amplitude = 30

		### JUGADORES ###
		self.jugador1 = None
		self.lifebar = LifeBar(6,0)
		self.final = None

		### Grupos Sprites y Capas ###
		self.capaEscenario = Capa()
		self.grupoJugadores = pygame.sprite.Group()
		self.grupoEnemigos = pygame.sprite.Group()
		self.grupoObjetos = pygame.sprite.Group()
		self.grupoPlataformas = pygame.sprite.Group()
		self.grupoSpritesDinamicos = pygame.sprite.Group()
		self.grupoSprites = pygame.sprite.Group()

		self.animacion = []

		### Sonido ###
		self.channel_bso = None
		self.channel_ambient = None

		# Configuramos la fase #
		self.setEscenario()
		self.setPlataformas()
		self.setJugador()
		self.setEnemigos()
		self.setAnim()
		self.setAudio()
		self.refreshSprites()

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
		self.grupoSpritesDinamicos.add(self.grupoObjetos)
		self.grupoSpritesDinamicos.add(self.grupoJugadores)
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)

		self.grupoSprites.add(self.grupoSpritesDinamicos)
		self.grupoSprites.add(self.grupoPlataformas)

	###FUNCIONES DE ACCION###
	def salir(self):
		pygame.time.delay(3000)	#Retardo para terminar el audio
		pygame.mixer.stop();
		self.director.salirEscena();

	def check_end(self):
		#Cuando hacemos el fundido a negro (Salímos) [Si morimos o muere el jefe final]
		if(not self.jugador1.alive()):
			if(self.fade == 0): 
				self.fade = -250
				GestorRecursos.CargarSonido('game_over.ogg').play()

		if ( not self.final.alive()):
			if self.fade == 0: 
				self.fade = -250
				GestorRecursos.CargarSonido('mision_complete_long.ogg').play()

		#Si estamos saliendo de la escena:
		if(self.fade < 0):
			self.channel_bso.set_volume(-self.fade/300)
			self.channel_ambient.set_volume(-self.fade/300)
			if(self.jugador1.alive()):
				self.jugador1.avanzar(self.grupoPlataformas)
				GestorRecursos.setConfigParam(self.clave_nivel, self.nivel + 1)

			if(self.fade>-10):
				self.salir()

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

			if self.scroll[0]*ESCALA + ANCHO_PANTALLA + 10 >= self.max_x:
				#if self.fade == 0: self.fade = -250
				#if self.jugador1.rect.centerx > ANCHO_PANTALLA + 100: self.salir(True)

				if self.fade == 0:
					if jugador.posicion[0] > self.max_x-jugador.rect.width:
						jugador.establecerPosicion((self.max_x-jugador.rect.width, jugador.posicion[1]))
				

				#self.scroll = (self.decorado.rect.right*ESCALA - ANCHO_PANTALLA, self.scroll[1])
				#jugador.establecerPosicion((self.scroll[0]*ESCALA + MAXIMO_X_JUGADOR*ESCALA, jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] + desplazamiento, self.scroll[1]);
				return True;

		return False;


	def actualizarScroll(self, jugador):
		if (self.scroll[1] > 1 or self.scroll[1] < 0):
			self.scrolly_speed = -self.scrolly_speed

		self.scroll = (self.scroll[0], self.scroll[1] + self.scrolly_speed)
		self.virtual_scroll = (int(self.scroll[0]), int(math.sin(self.scroll[1]) * self.scrolly_amplitude))

		cambioScroll = self.actualizarScrollOrdenados(jugador)

		self.capaEscenario.establecerPosicionPantalla(self.virtual_scroll)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla(self.virtual_scroll)

		if(self.fade == 0):
			sound_lvl = float(self.scroll[0])/float(self.max_x)
			self.channel_bso.set_volume(sound_lvl)

	def update(self, tiempo):
		#Actualizaciar el mapa y el scroll
		self.capaEscenario.update(tiempo)
		self.actualizarScroll(self.jugador1)

		#Se mueven los objetos
		for objeto in iter(self.grupoObjetos):
			objeto.mover(self.grupoPlataformas)

		#IA -> Se indican que hacen los enemigos
		if self.fade == 0:
			for enemigo in iter(self.grupoEnemigos):
				enemigo.mover_cpu(self.jugador1, self.grupoPlataformas)

		self.grupoSpritesDinamicos.update(self.grupoPlataformas,tiempo)

		#Miramos todas las colision de los enemios con los jugadores, si uno de ellos está atacando, daña al otro
		collitions = pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)
		#podría hacerse mejor con el parametro collided
		for player,enemys in collitions.items():
			for enemy in enemys:
				if (enemy.posturas[P_ATACANDO1] and player.posturas[P_ATACANDO1]):
					self.jugador1.quitarVida(0)
					enemy.quitarVida(0)
				else:
					if enemy.posturas[P_ATACANDO1]: 
						vida = self.jugador1.quitarVida(1)
						self.lifebar.actualizarVida(vida)
						self.hurt = 150
					if player.posturas[P_ATACANDO1]: enemy.quitarVida(1)

		self.check_end()
				
	def dibujar_fundido(self, pantalla):
		#Efecto fundido, para entrar a la escena, y para terminarla
		if(self.hurt > 0):
			red = pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
			red.fill((255,0,0))
			red.set_alpha(self.hurt)
			pantalla.blit(red, (0,0))
			self.hurt -= 30

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

	def dibujar_frontal(self, pantalla):
		for animacion in self.animacion:
			animacion.dibujar(pantalla)

	def dibujar(self, pantalla):
		pantalla.fill((0,0,0))

		#Dibujamos el fondo y luego los sprites
		self.capaEscenario.draw(pantalla)
		self.grupoSprites.draw(pantalla)

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

		
		
		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)
		
		self.dibujar_frontal(pantalla)
		self.lifebar.draw(pantalla)
		self.dibujar_fundido(pantalla)
					
	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					GestorRecursos.CargarSonido('game_over.ogg').play()
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

