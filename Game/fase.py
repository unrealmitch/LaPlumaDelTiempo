# -*- coding: utf-8 -*-

import random,math
import pygame, escena

from escena import *
from personajes import *
from objetos import *
from escenario import *
from capa import *
from gui import *
from pygame.locals import *
from animacionesPygame import *
import mando


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
DEBUG = False
MANDO = False
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

		#Control por mando de la xbox 360
		if MANDO:
			#self.mando = xbox360_controller.Controller(0)
			self.mando = mando.Mando(0)

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
		
		#Atenuado [Valor reutilizado para terminar la fase: Cuando es <0, se está terminando la fase, y atenuandola]
		self.fade = 250
		self.time_fade = pygame.time.get_ticks()

		#Atenuado Vida [Para destello rojo tras ser herido, valor de atenuado]
		self.hurt = 0

		###SCROLL### Que parte del decorado estamos visualizando
		self.scroll = (0,0.)
		self.virtual_scroll = (0.,0.)	#Variable auxiliar para guardar el scroll de las olas
		self.scrolly_speed = 0.03
		self.scrolly_amplitude = 30

		### JUGADORES ###
		self.jugador1 = None
		self.gui = Gui(6,0)
		self.final = None
		self.playerDrunk = False

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

		#Otros
		self.score = 0

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
		#Actualizamos todos los grupos de sprites
		self.grupoJugadores.add(self.jugador1)
		self.grupoSpritesDinamicos.add(self.grupoObjetos)
		self.grupoSpritesDinamicos.add(self.grupoJugadores)
		self.grupoSpritesDinamicos.add(self.grupoEnemigos)

		self.grupoSprites.add(self.grupoSpritesDinamicos)
		self.grupoSprites.add(self.grupoPlataformas)

	###FUNCIONES DE ACCION###
	def salir(self):
		#Salimos de la fase [Escena]
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
		#Actualizamos el scroll de la pantalla segun donde esté el jugador

		if (jugador.rect.left<MINIMO_X_JUGADOR):	#Max a la izq
			desplazamiento = (MINIMO_X_JUGADOR - jugador.rect.left)

			if self.scroll[0] <= 0:
				self.scroll = (0, self.scroll[1])
				if jugador.rect.left < 0: jugador.establecerPosicion((0 , jugador.posicion[1]))
				return False;
			else:
				self.scroll = (self.scroll[0] - desplazamiento, self.scroll[1])
				return True;

		if (jugador.rect.right > MAXIMO_X_JUGADOR):	#Max a la der pantalla
			desplazamiento = (jugador.rect.right - MAXIMO_X_JUGADOR)

			if self.scroll[0]*ESCALA + ANCHO_PANTALLA + 10 >= self.max_x:	#Max a la der del escenario
				#if self.fade == 0: self.fade = -250
				#if self.jugador1.rect.centerx > ANCHO_PANTALLA + 100: self.salir(True)

				if self.fade == 0:	#Si la fase no esta teminando, no deja sobrepasar a la derecha
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
		#Actualizamos el scroll de todos los elementos
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
			if(self.final != None): self.channel_bso.set_volume(sound_lvl)

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
					player.quitarVida(0)
					enemy.quitarVida(0)
				else:
					if enemy.posturas[P_ATACANDO1]: 
						if player.quitarVida(enemy.ataque): self.hurt = 150
						self.gui.actualizarVida(player.vida)
						
					if player.posturas[P_ATACANDO1]:
						if enemy.quitarVida(player.ataque) and enemy.vida <= 0: self.score += enemy.tipo 

		#Comprobamos si el prota coge un objeto. Lo elimina y hace el efecto de dicho objeto
		objetos = pygame.sprite.spritecollide(self.jugador1, self.grupoObjetos, False)
		for objeto in objetos:
			GestorRecursos.CargarSonido(objeto.sound_pick).play()
			objeto.kill()
			if objeto.tipo == CORAZON:
				vida = self.jugador1.addVida()
				self.gui.actualizarVida(vida)
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
			else:
				if objeto.tipo == ESPADA: self.jugador1.subirAtaque(1)
				if objeto.tipo == BOTAS: self.jugador1.subirVel(0.01)
				if objeto.tipo == MUELLE: self.jugador1.subirSalto(0.01)
				self.gui.actualizarPsj(self.jugador1)

		self.check_end()
				
	def dibujar_fundido(self, pantalla):
		#Efecto fundido, para entrar a la escena, o para terminarla
		if(self.hurt > 0):	#Efecto para cuando hieren al personaje
			red = pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
			red.fill((255,0,0))
			red.set_alpha(self.hurt)
			pantalla.blit(red, (0,0))
			self.hurt -= 30

		if(self.fade != 0):	#Si se está haciendo fundido [Entrando o saliendo de la escena]
			time = pygame.time.get_ticks()
			if(time > self.time_fade + 1):
				self.time_fade = time

				black = pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
				black.fill((0,0,0))

				if(self.fade>0): #Si estamos entrando a la fase, vamos quitando el fundido
					self.fade-=10
					black.set_alpha(self.fade)
					pantalla.blit(black, (0,0))
				else:	#Cuando se hace el fundido a negro por si pasamos la mision o morimos
					if(self.fade < -10):
						self.fade+=8
					else:
						self.fade=-1

					if(self.jugador1.alive()):	#Si ganamos
						image = GestorRecursos.CargarImagen("complete.png",-1)
					else:	#Si morimos
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

		
		#Modo debug para dibujar tb las plataformas
		if DEBUG:
			for elem in self.grupoPlataformas.sprites():
				elem.draw(pantalla)
		
		#Dibujamos la capa frontal, la gui y finalmente el fundido de haberlo
		self.dibujar_frontal(pantalla)
		self.gui.draw(pantalla)
		self.dibujar_fundido(pantalla)
					
	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					#Salimos de la fase matando al personaje
					GestorRecursos.CargarSonido('game_over.ogg').play()
					self.jugador1.vida = 0;
					self.jugador1.kill()
					self.fade = -200;
				if evento.key == K_F11:
					pygame.display.toggle_fullscreen()
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		# Las teclas se cargan al prinipio de la configuracion guardada
		if(self.fade == 0):
			teclasPulsadas = pygame.key.get_pressed()
			self.jugador1.mover(teclasPulsadas, self.teclasConfig)

			if MANDO:
				movimientos = {}
				pulsado = self.mando.get_buttons()
				pad = self.mando.get_pad()
				mov = self.mando.get_stick_izquierdo()

				if pad[0] or pulsado[0] or mov[1] > 0.5: movimientos.update({ARRIBA: True})
				if pad[2]: movimientos.update({ABAJO: True})

				if pad[1] or mov[0] > 0.5: movimientos.update({DERECHA: True})
				if pad[3] or mov[0] < -0.5: movimientos.update({IZQUIERDA: True})
				
				if pulsado[1] or pulsado[4] or pulsado[5] or abs(self.mando.get_gatillos())> 0.4: movimientos.update({ATAQUE1: True})
					
				if pulsado[6]:
					#Salimos de la fase matando al personaje
					GestorRecursos.CargarSonido('game_over.ogg').play()
					self.jugador1.vida = 0;
					self.jugador1.kill()
					self.fade = -200;

				self.jugador1.mover_mando(movimientos)